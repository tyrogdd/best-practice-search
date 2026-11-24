#!/usr/bin/env python3
"""Zero-dependency CLI helper for public no-login search APIs.

Supported sources:
  - hn        Hacker News (Algolia public API)
  - arxiv     arXiv papers (Atom XML API + HTML URL)
  - hf        Hugging Face Hub (models, datasets, papers)
  - lobsters  Lobste.rs (public tag/feed JSON with keyword filter)
  - se        Stack Exchange network (Stack Overflow, TeX, Stats, Unix, etc.)
  - wikimedia Wikimedia Commons (MediaWiki API with license & author metadata)

Uses only Python 3 standard library. Does not bypass authentication or rate limits.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

USER_AGENT = (
    "best-practice-search/1.0 "
    "(https://github.com/tyrogdd/best-practice-search; Python-urllib)"
)


def strip_html(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"<[^>]+>", " ", text)
    cleaned = html.unescape(cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def ts_to_date(ts: int | float | None) -> str:
    if not ts:
        return "unknown"
    return dt.datetime.fromtimestamp(int(ts), tz=dt.timezone.utc).strftime("%Y-%m-%d")


def iso_to_date(value: str | None) -> str:
    if not value:
        return "unknown"
    return value[:10] if len(value) >= 10 else value


def http_get(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, application/atom+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            "Accept-Encoding": "gzip",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding", "").lower() == "gzip" or raw[:2] == b"\x1f\x8b":
                raw = gzip.decompress(raw)
            return raw
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            err_raw = exc.read()
            if err_raw[:2] == b"\x1f\x8b":
                err_raw = gzip.decompress(err_raw)
            body = err_raw.decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        raise RuntimeError(f"HTTP {exc.code} fetching {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error fetching {url}: {exc.reason}") from exc


def http_get_json(url: str, timeout: int = 20) -> Any:
    return json.loads(http_get(url, timeout=timeout).decode("utf-8"))


# ---------------------------------------------------------------------------
# 1. Hacker News (Algolia API)
# ---------------------------------------------------------------------------
def search_hn(args: argparse.Namespace) -> list[dict[str, Any]]:
    endpoint = (
        "https://hn.algolia.com/api/v1/search_by_date"
        if args.sort == "date"
        else "https://hn.algolia.com/api/v1/search"
    )
    params: dict[str, Any] = {
        "query": args.query,
        "tags": args.tags,
        "hitsPerPage": args.limit,
    }
    numeric_filters: list[str] = []
    if args.since:
        since_dt = dt.datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        numeric_filters.append(f"created_at_i>{int(since_dt.timestamp())}")
    if args.min_points is not None:
        numeric_filters.append(f"points>={args.min_points}")
    if numeric_filters:
        params["numericFilters"] = ",".join(numeric_filters)

    url = f"{endpoint}?{urllib.parse.urlencode(params)}"
    data = http_get_json(url, timeout=args.timeout)
    items: list[dict[str, Any]] = []
    for hit in data.get("hits", []):
        oid = hit.get("objectID") or hit.get("story_id")
        title = hit.get("title") or hit.get("story_title") or norm_space(strip_html(hit.get("comment_text", "")))[:120]
        items.append(
            {
                "source": "hacker-news",
                "title": norm_space(title),
                "date": iso_to_date(hit.get("created_at")),
                "points": hit.get("points"),
                "comments": hit.get("num_comments"),
                "author": hit.get("author"),
                "discussion_url": f"https://news.ycombinator.com/item?id={oid}" if oid else "",
                "url": hit.get("url") or hit.get("story_url") or "",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 2. arXiv (Atom XML API)
# ---------------------------------------------------------------------------
def build_arxiv_query(raw_query: str) -> str:
    q = raw_query.strip()
    if any(tok in q for tok in ("ti:", "au:", "abs:", "cat:", "all:", " AND ", " OR ")):
        return q
    terms = [t for t in q.split() if t]
    if not terms:
        return "all:*"
    return " AND ".join(f"all:{t}" for t in terms)


def search_arxiv(args: argparse.Namespace) -> list[dict[str, Any]]:
    sort_map = {
        "relevance": "relevance",
        "submitted": "submittedDate",
        "updated": "lastUpdatedDate",
    }
    params = {
        "search_query": build_arxiv_query(args.query),
        "start": 0,
        "max_results": args.limit,
        "sortBy": sort_map[args.sort],
        "sortOrder": "descending",
    }
    url = f"https://export.arxiv.org/api/query?{urllib.parse.urlencode(params)}"
    raw = http_get(url, timeout=args.timeout)
    root = ET.fromstring(raw)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    items: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ns):
        abs_url = norm_space(entry.findtext("atom:id", default="", namespaces=ns))
        if abs_url.startswith("http://arxiv.org/"):
            abs_url = "https://" + abs_url[len("http://"):]
        arxiv_id = abs_url.rsplit("/abs/", 1)[-1] if "/abs/" in abs_url else abs_url
        authors = [
            norm_space(a.findtext("atom:name", default="", namespaces=ns))
            for a in entry.findall("atom:author", ns)
        ]
        author_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else ""
        html_url = f"https://arxiv.org/html/{arxiv_id}" if arxiv_id else ""
        summary = norm_space(entry.findtext("atom:summary", default="", namespaces=ns))
        items.append(
            {
                "source": "arxiv",
                "id": arxiv_id,
                "title": norm_space(entry.findtext("atom:title", default="", namespaces=ns)),
                "published": iso_to_date(entry.findtext("atom:published", default="", namespaces=ns)),
                "updated": iso_to_date(entry.findtext("atom:updated", default="", namespaces=ns)),
                "authors": author_str,
                "url": abs_url,
                "html_url": html_url,
                "pdf_url": pdf_url,
                "summary": summary[:260] + ("..." if len(summary) > 260 else ""),
            }
        )
    return items


# ---------------------------------------------------------------------------
# 3. Hugging Face Hub API
# ---------------------------------------------------------------------------
def search_hf(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.kind == "papers":
        url = f"https://huggingface.co/api/papers/search?{urllib.parse.urlencode({'q': args.query})}"
        data = http_get_json(url, timeout=args.timeout)
        items: list[dict[str, Any]] = []
        for row in data[: args.limit]:
            paper = row.get("paper") or row
            pid = paper.get("id", "")
            items.append(
                {
                    "source": "huggingface-papers",
                    "id": pid,
                    "title": norm_space(paper.get("title", "")),
                    "date": iso_to_date(paper.get("publishedAt") or row.get("publishedAt")),
                    "upvotes": paper.get("upvotes"),
                    "url": f"https://huggingface.co/papers/{pid}" if pid else "",
                    "arxiv_url": f"https://arxiv.org/abs/{pid}" if pid else "",
                    "summary": norm_space(paper.get("summary", ""))[:240],
                }
            )
        return items

    base = "https://huggingface.co/api/datasets" if args.kind == "datasets" else "https://huggingface.co/api/models"
    params = {
        "search": args.query,
        "sort": args.sort,
        "direction": -1,
        "limit": args.limit,
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    data = http_get_json(url, timeout=args.timeout)
    items = []
    for row in data:
        repo_id = row.get("id", "")
        tags = row.get("tags") or []
        licenses = [t.split(":", 1)[1] for t in tags if t.startswith("license:")]
        prefix = "datasets/" if args.kind == "datasets" else ""
        items.append(
            {
                "source": f"huggingface-{args.kind}",
                "id": repo_id,
                "date": iso_to_date(row.get("lastModified") or row.get("createdAt")),
                "downloads": row.get("downloads"),
                "likes": row.get("likes"),
                "license": ", ".join(licenses) if licenses else "check-card",
                "task": row.get("pipeline_tag") or "",
                "url": f"https://huggingface.co/{prefix}{repo_id}",
                "readme_raw": f"https://huggingface.co/{prefix}{repo_id}/raw/main/README.md",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 4. Lobste.rs (Public tag/feed JSON)
# ---------------------------------------------------------------------------
def search_lobsters(args: argparse.Namespace) -> list[dict[str, Any]]:
    terms = [t.lower() for t in (args.query or "").split() if t]
    pages = args.pages if terms else 1
    results: list[dict[str, Any]] = []
    seen: set[str] = set()

    for page in range(1, pages + 1):
        if args.tag:
            path = f"/t/{urllib.parse.quote(args.tag)}"
        else:
            path = f"/{args.feed}"
        suffix = f"/page/{page}.json" if page > 1 else ".json"
        url = f"https://lobste.rs{path}{suffix}"
        rows = http_get_json(url, timeout=args.timeout)
        if not rows:
            break
        for row in rows:
            sid = row.get("short_id", "")
            if sid in seen:
                continue
            haystack = " ".join(
                [
                    row.get("title", ""),
                    " ".join(row.get("tags") or []),
                    row.get("description_plain") or row.get("description") or "",
                    row.get("url") or "",
                ]
            ).lower()
            if terms and not all(t in haystack for t in terms):
                continue
            seen.add(sid)
            results.append(
                {
                    "source": "lobsters",
                    "title": norm_space(row.get("title", "")),
                    "date": iso_to_date(row.get("created_at")),
                    "score": row.get("score"),
                    "comments": row.get("comment_count"),
                    "tags": row.get("tags") or [],
                    "discussion_url": row.get("short_id_url") or row.get("comments_url") or "",
                    "url": row.get("url") or "",
                }
            )
            if len(results) >= args.limit:
                return results
    return results


# ---------------------------------------------------------------------------
# 5. Stack Exchange (API v2.3)
# ---------------------------------------------------------------------------
def search_se(args: argparse.Namespace) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "order": "desc",
        "sort": args.sort,
        "q": args.query,
        "site": args.site,
        "pagesize": args.limit,
    }
    if args.tagged:
        params["tagged"] = args.tagged
    if args.accepted:
        params["accepted"] = "True"

    url = f"https://api.stackexchange.com/2.3/search/advanced?{urllib.parse.urlencode(params)}"
    data = http_get_json(url, timeout=args.timeout)
    items: list[dict[str, Any]] = []
    for row in data.get("items", []):
        items.append(
            {
                "source": f"stackexchange-{args.site}",
                "title": norm_space(html.unescape(row.get("title", ""))),
                "created": ts_to_date(row.get("creation_date")),
                "active": ts_to_date(row.get("last_activity_date")),
                "score": row.get("score"),
                "answers": row.get("answer_count"),
                "answered": bool(row.get("is_answered")),
                "tags": row.get("tags") or [],
                "url": row.get("link") or "",
            }
        )
    return items


# ---------------------------------------------------------------------------
# 6. Wikimedia Commons (MediaWiki API)
# ---------------------------------------------------------------------------
def search_wikimedia(args: argparse.Namespace) -> list[dict[str, Any]]:
    q = args.query.strip()
    if args.svg_only and "filetype:" not in q:
        q = f"{q} filetype:drawing"
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": 6,
        "gsrsearch": q,
        "gsrlimit": args.limit,
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "format": "json",
    }
    url = f"https://commons.wikimedia.org/w/api.php?{urllib.parse.urlencode(params)}"
    data = http_get_json(url, timeout=args.timeout)
    pages = (data.get("query") or {}).get("pages") or {}
    ordered = sorted(pages.values(), key=lambda p: p.get("index", 9999))

    items: list[dict[str, Any]] = []
    for page in ordered:
        infos = page.get("imageinfo") or []
        info = infos[0] if infos else {}
        meta = info.get("extmetadata") or {}
        mime = info.get("mime", "")
        if args.svg_only and mime != "image/svg+xml":
            continue
        license_name = strip_html((meta.get("LicenseShortName") or {}).get("value", "")) or "check-file-page"
        artist = strip_html((meta.get("Artist") or {}).get("value", ""))[:120] or "check-file-page"
        date_str = strip_html((meta.get("DateTimeOriginal") or meta.get("DateTime") or {}).get("value", ""))
        direct_url = (info.get("url") or "").split("?", 1)[0]
        items.append(
            {
                "source": "wikimedia-commons",
                "title": page.get("title", ""),
                "date": iso_to_date(date_str) if date_str else "unknown",
                "mime": mime,
                "size": f"{info.get('width', '?')}x{info.get('height', '?')}",
                "license": license_name,
                "artist": artist,
                "file_page": info.get("descriptionurl") or "",
                "direct_url": direct_url,
            }
        )
    return items


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------
def render_markdown(source: str, query: str, items: list[dict[str, Any]]) -> str:
    today = dt.datetime.now(tz=dt.timezone.utc).strftime("%Y-%m-%d")
    lines = [f"### `{source}` 检索结果（查询：`{query or '(feed)'}` · 检索日：{today} UTC · 共 {len(items)} 条）", ""]
    if not items:
        lines.append("_未返回匹配结果。可尝试简化关键词、放宽时间或切换排序。_")
        return "\n".join(lines)

    for idx, it in enumerate(items, 1):
        if source == "hn":
            lines.append(
                f"{idx}. **{it['title']}** · 日期：`{it['date']}` · {it['points']} pts / {it['comments']} comments"
            )
            lines.append(f"   - HN 讨论：{it['discussion_url']}")
            if it["url"]:
                lines.append(f"   - 原文链接：{it['url']}")
        elif source == "arxiv":
            lines.append(
                f"{idx}. **{it['title']}** (`{it['id']}`) · 发布：`{it['published']}` · 更新：`{it['updated']}`"
            )
            lines.append(f"   - 作者：{it['authors']}")
            lines.append(f"   - 摘要页：{it['url']} · HTML 版：{it['html_url']}")
            if it["summary"]:
                lines.append(f"   - 摘要：{it['summary']}")
        elif source == "hf":
            if it["source"] == "huggingface-papers":
                lines.append(f"{idx}. **{it['title']}** (`{it['id']}`) · 日期：`{it['date']}` · upvotes：{it['upvotes']}")
                lines.append(f"   - HF 论文页：{it['url']} · arXiv：{it['arxiv_url']}")
            else:
                lines.append(
                    f"{idx}. **{it['id']}** · 更新：`{it['date']}` · 许可：`{it['license']}` · downloads：{it['downloads']} / likes：{it['likes']}"
                )
                lines.append(f"   - 主页：{it['url']} · README 原文：{it['readme_raw']}")
        elif source == "lobsters":
            tags = ", ".join(it["tags"])
            lines.append(
                f"{idx}. **{it['title']}** · 日期：`{it['date']}` · {it['score']} pts / {it['comments']} comments · tags: `{tags}`"
            )
            lines.append(f"   - Lobste.rs 讨论：{it['discussion_url']}")
            if it["url"]:
                lines.append(f"   - 原文链接：{it['url']}")
        elif source == "se":
            status = "已采纳/有解" if it["answered"] else "未标记解决"
            lines.append(
                f"{idx}. **{it['title']}** · 提问：`{it['created']}` · 活跃：`{it['active']}` · score：{it['score']} / {it['answers']} 回答（{status}）"
            )
            lines.append(f"   - 链接：{it['url']}")
        elif source == "wikimedia":
            lines.append(
                f"{idx}. **{it['title']}** · 格式：`{it['mime']}` ({it['size']}) · 许可：`{it['license']}` · 日期：`{it['date']}`"
            )
            lines.append(f"   - 作者：{it['artist']}")
            lines.append(f"   - 文件页（核对许可）：{it['file_page']}")
            if it["direct_url"]:
                lines.append(f"   - 源文件直链：{it['direct_url']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--limit", type=int, default=5, help="Max items to return (default: 5)")
    common.add_argument("--format", choices=["md", "json"], default="md", help="Output format (default: md)")
    common.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds (default: 20)")

    parser = argparse.ArgumentParser(
        prog="public_search.py",
        description="Zero-dependency public API search helper for best-practice-search skill.",
    )
    sub = parser.add_subparsers(dest="source", required=True)

    p_hn = sub.add_parser("hn", parents=[common], help="Search Hacker News via Algolia API")
    p_hn.add_argument("query", help="Search query")
    p_hn.add_argument("--sort", choices=["relevance", "date"], default="relevance")
    p_hn.add_argument("--tags", default="story", help="Algolia tags (default: story; e.g. comment, show_hn, ask_hn)")
    p_hn.add_argument("--since", help="Filter results after YYYY-MM-DD (UTC)")
    p_hn.add_argument("--min-points", type=int, help="Minimum HN points filter (e.g. 30)")
    p_hn.set_defaults(func=search_hn)

    p_arxiv = sub.add_parser("arxiv", parents=[common], help="Search arXiv papers via Atom API")
    p_arxiv.add_argument("query", help="Search query (supports arXiv field prefixes like ti:, au:, cat:)")
    p_arxiv.add_argument("--sort", choices=["relevance", "submitted", "updated"], default="relevance")
    p_arxiv.set_defaults(func=search_arxiv)

    p_hf = sub.add_parser("hf", parents=[common], help="Search Hugging Face Hub (models/datasets/papers)")
    p_hf.add_argument("query", help="Search query")
    p_hf.add_argument("--kind", choices=["models", "datasets", "papers"], default="models")
    p_hf.add_argument("--sort", choices=["downloads", "likes", "lastModified"], default="downloads")
    p_hf.set_defaults(func=search_hf)

    p_lob = sub.add_parser("lobsters", parents=[common], help="Fetch/filter Lobste.rs public JSON feeds")
    p_lob.add_argument("query", nargs="?", default="", help="Optional space-separated keywords (AND match)")
    p_lob.add_argument("--tag", help="Lobste.rs tag (e.g. rust, databases, practices, ai)")
    p_lob.add_argument("--feed", choices=["hottest", "newest", "active"], default="hottest")
    p_lob.add_argument("--pages", type=int, default=3, help="Max feed pages to scan when filtering by query (default: 3)")
    p_lob.set_defaults(func=search_lobsters)

    p_se = sub.add_parser("se", parents=[common], help="Search Stack Exchange network via API v2.3")
    p_se.add_argument("query", help="Search query")
    p_se.add_argument("--site", default="stackoverflow", help="SE site slug (e.g. stackoverflow, tex, stats, unix)")
    p_se.add_argument("--sort", choices=["relevance", "votes", "creation", "activity"], default="relevance")
    p_se.add_argument("--tagged", help="Semicolon-separated tags (e.g. python;matplotlib)")
    p_se.add_argument("--accepted", action="store_true", help="Only questions with an accepted answer")
    p_se.set_defaults(func=search_se)

    p_wm = sub.add_parser("wikimedia", parents=[common], help="Search Wikimedia Commons files + license metadata")
    p_wm.add_argument("query", help="Search query (English terms recommended)")
    p_wm.add_argument("--svg-only", action="store_true", help="Restrict results to SVG vector drawings")
    p_wm.set_defaults(func=search_wikimedia)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        items = args.func(args)
    except Exception as exc:
        print(f"ERROR [{args.source}]: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(args.source, getattr(args, "query", ""), items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

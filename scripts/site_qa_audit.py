#!/usr/bin/env python3
"""Reusable production link and conversion-risk crawler for insurancy.com.

Uses only the Python standard library so the audit is easy to rerun.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0 Safari/537.36 InsurancyConversionQA/1.0"
)
PLACEHOLDER_RE = re.compile(
    r"\b(coming soon|under construction|page not found|404 error|not found)\b",
    re.IGNORECASE,
)
SKIP_EXTENSIONS = {
    ".avif",
    ".css",
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".svg",
    ".txt",
    ".webp",
    ".woff",
    ".woff2",
    ".xml",
    ".zip",
}


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def normalize_url(url: str, base_url: str) -> str | None:
    absolute = urllib.parse.urljoin(base_url, url)
    parsed = urllib.parse.urlsplit(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if any(path.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
        return None
    # Drop fragments and tracking-only query parameters.
    query_items = [
        (key, value)
        for key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith(("utm_", "gclid", "fbclid"))
    ]
    return urllib.parse.urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            urllib.parse.urlencode(query_items),
            "",
        )
    )


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self.forms: list[dict[str, str]] = []
        self.controls: list[dict[str, str | bool]] = []
        self.images: list[dict[str, str]] = []
        self.labels_for: set[str] = set()
        self._title_depth = 0
        self._h1_depth = 0
        self._title_parts: list[str] = []
        self._h1_parts: list[str] = []
        self._anchor: dict[str, str] | None = None
        self._anchor_parts: list[str] = []
        self._button: dict[str, str | bool] | None = None
        self._button_parts: list[str] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): (value or "") for key, value in attrs}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attr = self._attrs(attrs)
        tag = tag.lower()
        if tag == "title":
            self._title_depth += 1
        elif tag == "h1":
            self._h1_depth += 1
        elif tag == "a" and attr.get("href"):
            self._anchor = {
                "href": attr["href"],
                "aria_label": attr.get("aria-label", ""),
                "target": attr.get("target", ""),
            }
            self._anchor_parts = []
        elif tag == "form":
            self.forms.append(
                {
                    "action": attr.get("action", ""),
                    "method": attr.get("method", "get").lower(),
                    "id": attr.get("id", ""),
                }
            )
        elif tag == "label" and attr.get("for"):
            self.labels_for.add(attr["for"])
        elif tag in {"input", "select", "textarea"}:
            control_type = attr.get("type", tag).lower()
            self.controls.append(
                {
                    "tag": tag,
                    "type": control_type,
                    "id": attr.get("id", ""),
                    "name": attr.get("name", ""),
                    "aria_label": attr.get("aria-label", ""),
                    "aria_labelledby": attr.get("aria-labelledby", ""),
                    "placeholder": attr.get("placeholder", ""),
                    "hidden": control_type == "hidden"
                    or "hidden" in attr
                    or attr.get("aria-hidden") == "true",
                }
            )
        elif tag == "button":
            self._button = {
                "tag": "button",
                "type": attr.get("type", "submit").lower(),
                "id": attr.get("id", ""),
                "name": attr.get("name", ""),
                "aria_label": attr.get("aria-label", ""),
                "aria_labelledby": attr.get("aria-labelledby", ""),
                "placeholder": "",
                "hidden": "hidden" in attr or attr.get("aria-hidden") == "true",
            }
            self._button_parts = []
        elif tag == "img":
            self.images.append(
                {
                    "src": attr.get("src", ""),
                    "alt": attr.get("alt", ""),
                    "aria_hidden": attr.get("aria-hidden", ""),
                }
            )

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._title_depth = max(0, self._title_depth - 1)
        elif tag == "h1":
            self._h1_depth = max(0, self._h1_depth - 1)
        elif tag == "a" and self._anchor is not None:
            self._anchor["text"] = clean_text(" ".join(self._anchor_parts))
            self.links.append(self._anchor)
            self._anchor = None
            self._anchor_parts = []
        elif tag == "button" and self._button is not None:
            self._button["text"] = clean_text(" ".join(self._button_parts))
            self.controls.append(self._button)
            self._button = None
            self._button_parts = []

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self._title_parts.append(data)
        if self._h1_depth:
            self._h1_parts.append(data)
        if self._anchor is not None:
            self._anchor_parts.append(data)
        if self._button is not None:
            self._button_parts.append(data)

    @property
    def title(self) -> str:
        return clean_text(" ".join(self._title_parts))

    @property
    def h1(self) -> str:
        return clean_text(" ".join(self._h1_parts))

    def unlabeled_controls(self) -> list[dict[str, str | bool]]:
        findings: list[dict[str, str | bool]] = []
        for control in self.controls:
            if control["hidden"]:
                continue
            if control["tag"] == "button" and (
                control.get("text") or control.get("aria_label")
            ):
                continue
            if (
                control.get("aria_label")
                or control.get("aria_labelledby")
                or control.get("id") in self.labels_for
            ):
                continue
            findings.append(control)
        return findings


@dataclass
class PageResult:
    url: str
    status: int | None
    final_url: str | None
    elapsed_ms: int
    content_type: str
    bytes: int
    title: str = ""
    h1: str = ""
    error: str = ""
    links: list[dict[str, str]] = field(default_factory=list)
    forms: list[dict[str, str]] = field(default_factory=list)
    unlabeled_controls: list[dict[str, str | bool]] = field(default_factory=list)
    missing_alt_images: list[dict[str, str]] = field(default_factory=list)
    placeholder_match: str = ""


def fetch_page(url: str, timeout: float) -> PageResult:
    started = time.monotonic()
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    status: int | None = None
    final_url: str | None = None
    content_type = ""
    body = b""
    error = ""
    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=ssl.create_default_context()
        ) as response:
            status = response.status
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            body = response.read(2_000_000)
    except urllib.error.HTTPError as exc:
        status = exc.code
        final_url = exc.geturl()
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        try:
            body = exc.read(500_000)
        except Exception:
            body = b""
        error = f"HTTP {exc.code}"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    elapsed_ms = round((time.monotonic() - started) * 1000)
    result = PageResult(
        url=url,
        status=status,
        final_url=final_url,
        elapsed_ms=elapsed_ms,
        content_type=content_type,
        bytes=len(body),
        error=error,
    )
    if "html" not in content_type.lower() or not body:
        return result

    text = body.decode("utf-8", errors="replace")
    parser = PageParser()
    try:
        parser.feed(text)
    except Exception as exc:
        result.error = (result.error + "; " if result.error else "") + (
            f"HTML parse: {type(exc).__name__}: {exc}"
        )
    result.title = parser.title
    result.h1 = parser.h1
    result.links = parser.links
    result.forms = parser.forms
    result.unlabeled_controls = parser.unlabeled_controls()
    result.missing_alt_images = [
        image
        for image in parser.images
        if not image.get("alt") and image.get("aria_hidden") != "true"
    ][:25]
    page_signal = f"{result.title} {result.h1}"
    placeholder = PLACEHOLDER_RE.search(page_signal)
    if placeholder:
        result.placeholder_match = placeholder.group(0)
    return result


def sitemap_urls(sitemap_url: str, timeout: float) -> list[str]:
    request = urllib.request.Request(
        sitemap_url, headers={"User-Agent": USER_AGENT, "Accept": "application/xml"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        root = ET.fromstring(response.read())
    urls = []
    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            urls.append(element.text.strip())
    return urls


def chunks(values: list[str], size: int) -> Iterable[list[str]]:
    for index in range(0, len(values), size):
        yield values[index : index + size]


def crawl(args: argparse.Namespace) -> dict:
    base = normalize_url(args.base_url, args.base_url)
    if base is None:
        raise ValueError("base URL must be HTTP(S)")
    primary_host = urllib.parse.urlsplit(base).netloc
    seeds = sitemap_urls(args.sitemap, args.timeout)
    if base not in seeds:
        seeds.insert(0, base)

    queue: deque[str] = deque()
    queued: set[str] = set()
    for seed in seeds:
        normalized = normalize_url(seed, base)
        if normalized and urllib.parse.urlsplit(normalized).netloc == primary_host:
            queue.append(normalized)
            queued.add(normalized)

    pages: dict[str, PageResult] = {}
    if args.resume:
        resume_payload = json.loads(Path(args.resume).read_text())
        for record in resume_payload.get("pages", []):
            result = PageResult(**record)
            pages[result.url] = result
        queued.update(pages)
        queue = deque(url for url in queue if url not in pages)

    external_targets: dict[str, list[dict[str, str]]] = defaultdict(list)
    internal_edges: list[dict[str, str]] = []

    # Reconstruct the frontier and edge inventory from resumed page records.
    for result in pages.values():
        for link in result.links:
            target = normalize_url(link.get("href", ""), result.final_url or result.url)
            if not target:
                continue
            edge = {
                "source": result.url,
                "target": target,
                "text": link.get("text", ""),
            }
            if urllib.parse.urlsplit(target).netloc == primary_host:
                internal_edges.append(edge)
                if target not in queued and len(queued) < args.max_pages * 3:
                    queued.add(target)
                    queue.append(target)
            else:
                external_targets[target].append(edge)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        while queue and len(pages) < args.max_pages:
            batch_size = min(args.workers * 2, args.max_pages - len(pages))
            batch = [queue.popleft() for _ in range(min(batch_size, len(queue)))]
            futures = {
                executor.submit(fetch_page, url, args.timeout): url for url in batch
            }
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                pages[result.url] = result
                for link in result.links:
                    target = normalize_url(link.get("href", ""), result.final_url or result.url)
                    if not target:
                        continue
                    edge = {
                        "source": result.url,
                        "target": target,
                        "text": link.get("text", ""),
                    }
                    if urllib.parse.urlsplit(target).netloc == primary_host:
                        internal_edges.append(edge)
                        if target not in queued and len(queued) < args.max_pages * 3:
                            queued.add(target)
                            queue.append(target)
                    else:
                        external_targets[target].append(edge)

    # One-hop availability check for every unique HTTP(S) destination linked from
    # the crawled pages. These destinations are not recursively crawled.
    external_results: dict[str, PageResult] = {}
    external_urls = sorted(external_targets)[: args.max_external]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        for batch in chunks(external_urls, args.workers * 2):
            futures = {
                executor.submit(fetch_page, url, args.timeout): url for url in batch
            }
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                external_results[result.url] = result

    broken_edges = []
    for edge in internal_edges:
        target_result = pages.get(edge["target"])
        if target_result is None:
            continue
        if target_result.status is None or target_result.status >= 400:
            broken_edges.append(
                {
                    **edge,
                    "status": target_result.status,
                    "error": target_result.error,
                }
            )

    external_failures = []
    for target, sources in external_targets.items():
        target_result = external_results.get(target)
        if target_result is None:
            continue
        if target_result.status is None or target_result.status >= 400:
            external_failures.append(
                {
                    "target": target,
                    "status": target_result.status,
                    "error": target_result.error,
                    "sources": sources[:10],
                }
            )

    page_records = [asdict(result) for result in pages.values()]
    external_records = [asdict(result) for result in external_results.values()]
    status_counts = Counter(
        "error" if page.status is None else str(page.status) for page in pages.values()
    )
    missing_titles = sorted(
        page.url
        for page in pages.values()
        if page.status == 200 and "html" in page.content_type.lower() and not page.title
    )
    missing_h1s = sorted(
        page.url
        for page in pages.values()
        if page.status == 200 and "html" in page.content_type.lower() and not page.h1
    )
    placeholder_pages = sorted(
        [
            {
                "url": page.url,
                "status": page.status,
                "title": page.title,
                "h1": page.h1,
                "match": page.placeholder_match,
            }
            for page in pages.values()
            if page.placeholder_match
        ],
        key=lambda item: item["url"],
    )
    unlabeled = sorted(
        [
            {"url": page.url, "controls": page.unlabeled_controls}
            for page in pages.values()
            if page.unlabeled_controls
        ],
        key=lambda item: item["url"],
    )
    missing_alt = sorted(
        [
            {"url": page.url, "images": page.missing_alt_images}
            for page in pages.values()
            if page.missing_alt_images
        ],
        key=lambda item: item["url"],
    )
    slowest = sorted(
        [
            {"url": page.url, "status": page.status, "elapsed_ms": page.elapsed_ms}
            for page in pages.values()
        ],
        key=lambda item: item["elapsed_ms"],
        reverse=True,
    )[:25]

    return {
        "generated_at_epoch": int(time.time()),
        "base_url": base,
        "sitemap_url": args.sitemap,
        "sitemap_seed_count": len(seeds),
        "scope": {
            "max_pages": args.max_pages,
            "max_external": args.max_external,
            "timeout_seconds": args.timeout,
            "workers": args.workers,
        },
        "summary": {
            "pages_fetched": len(pages),
            "status_counts": dict(sorted(status_counts.items())),
            "internal_link_instances": len(internal_edges),
            "unique_internal_targets": len({edge["target"] for edge in internal_edges}),
            "broken_internal_link_instances": len(broken_edges),
            "external_targets_checked": len(external_results),
            "external_failures_or_blocks": len(external_failures),
            "placeholder_pages": len(placeholder_pages),
            "pages_with_unlabeled_controls": len(unlabeled),
            "pages_with_missing_alt_images": len(missing_alt),
            "missing_title_pages": len(missing_titles),
            "missing_h1_pages": len(missing_h1s),
        },
        "broken_internal_links": broken_edges,
        "external_failures_or_blocks": external_failures,
        "placeholder_pages": placeholder_pages,
        "pages_with_unlabeled_controls": unlabeled,
        "pages_with_missing_alt_images": missing_alt,
        "missing_title_pages": missing_titles,
        "missing_h1_pages": missing_h1s,
        "slowest_pages": slowest,
        "pages": sorted(page_records, key=lambda page: page["url"]),
        "external_targets": sorted(
            external_records, key=lambda result: result["url"]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="https://insurancy.com/")
    parser.add_argument("--sitemap", default="https://insurancy.com/sitemap.xml")
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--max-external", type=int, default=500)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument(
        "--resume",
        help="Existing audit JSON to resume without refetching completed pages",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = crawl(args)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 1 if report["broken_internal_links"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

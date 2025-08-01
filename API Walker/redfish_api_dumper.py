#!/usr/bin/env python3
"""
redfish_api_dumper.py (stdlib, multithread, Py≥3.6)
=================================================
Walk a Redfish‑style REST API beginning at ``/redfish/v1`` and write a
Markdown dump of every JSON payload discovered via ``@odata.id`` links.

Features
~~~~~~~~
* **Pure standard library** – no external packages or internet access
  needed.
* **Multithreaded crawler** – configurable number of worker threads
  (default 8) dramatically accelerates large trees.
* **Text progress bar** – shows endpoints visited vs. total discovered
  and the URL most recently fetched.
* **TLS verification disabled by default** (equivalent to ``curl -k``).
  Pass ``--verify`` to enforce certificate checks.

Usage example
-------------
::

   $ python redfish_api_dumper.py \
         --host 10.15.100.50 \
         --username admin \
         --password admin \
         --outfile redfish_dump.md \
         --workers 16          # optional, default 8

"""

import argparse
import base64
import json
import ssl
import sys
import threading
import time
import urllib.parse
import urllib.request
from collections import deque
from queue import Queue
from typing import Any, Dict, List, Set, Tuple, Union

# -----------------------------------------------------------------------------
# Typing helpers (compatible with Python <3.10)
# -----------------------------------------------------------------------------
Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

# -----------------------------------------------------------------------------
# Utility functions – Redfish link discovery
# -----------------------------------------------------------------------------

def _odata_link(obj: Json) -> str:
    return obj.get("@odata.id") if isinstance(obj, dict) and "@odata.id" in obj else None  # type: ignore[attr-defined]


def _collect_links(node: Json) -> Set[str]:
    links: Set[str] = set()
    if isinstance(node, dict):
        link = _odata_link(node)
        if link:
            links.add(link)
        for v in node.values():
            links.update(_collect_links(v))
    elif isinstance(node, list):
        for item in node:
            links.update(_collect_links(item))
    return links

# -----------------------------------------------------------------------------
# Minimal session wrapper around urllib.request
# -----------------------------------------------------------------------------
class StdLibSession:
    def __init__(self, username: str, password: str, verify: bool):
        auth_bytes = f"{username}:{password}".encode()
        self._auth_header = {
            "Authorization": f"Basic {base64.b64encode(auth_bytes).decode()}"
        }
        self._ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()  # type: ignore[attr-defined]

    def get_json(self, url: str) -> Json:
        req = urllib.request.Request(url, headers={
            **self._auth_header,
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, context=self._ctx) as resp:  # nosec B310
            charset = resp.headers.get_content_charset() or "utf-8"
            return json.loads(resp.read().decode(charset))

# -----------------------------------------------------------------------------
# Thread‑safe crawler
# -----------------------------------------------------------------------------
class ConcurrentCrawler:
    _BAR_WIDTH = 40

    def __init__(self, session: StdLibSession, workers: int):
        self.session = session
        self.workers = max(1, workers)
        self.queue: "Queue[Tuple[str,int]]" = Queue()
        self.visited: Set[str] = set()
        self.visited_lock = threading.Lock()
        self.output_lock = threading.Lock()
        self.md_lines: List[str] = ["# Redfish API Dump", ""]
        self.done = 0
        self.bar_lock = threading.Lock()
        self.stop_event = threading.Event()

    # ---------------- progress ----------------
    def _print_bar(self, current: str):
        with self.bar_lock:
            done = self.done
            remaining = self.queue.qsize()
            total = done + remaining if (done + remaining) else 1
            filled = int(self._BAR_WIDTH * done / total)
            bar = "#" * filled + "-" * (self._BAR_WIDTH - filled)
            short = (current[:57] + "…") if len(current) > 60 else current
            sys.stdout.write(f"\r[{bar}] {done}/{total} nodes | last {short:<60}")
            sys.stdout.flush()

    # ---------------- worker ------------------
    def _worker(self):
        while not self.stop_event.is_set():
            try:
                url, depth = self.queue.get(timeout=0.2)
            except Exception:
                # queue empty
                if self.queue.empty():
                    return
                continue
            try:
                payload = self.session.get_json(url)
            except Exception as exc:
                with self.output_lock:
                    sys.stdout.write(f"\n⚠️  Error fetching {url}: {exc}\n")
                with self.visited_lock:
                    self.done += 1
                self.queue.task_done()
                self._print_bar(url)
                continue

            # append markdown
            header_level = min(depth + 2, 6)
            with self.output_lock:
                self.md_lines.append("#" * header_level + " " + url)
                self.md_lines.append("")
                self.md_lines.append("```json")
                self.md_lines.append(json.dumps(payload, indent=2, sort_keys=True))
                self.md_lines.append("```")
                self.md_lines.append("")

            # enqueue new links
            new_links = _collect_links(payload)
            with self.visited_lock:
                for link in sorted(new_links):
                    abs_url = urllib.parse.urljoin(url, link)
                    if abs_url not in self.visited:
                        self.visited.add(abs_url)
                        self.queue.put((abs_url, depth + 1))
                self.done += 1

            self.queue.task_done()
            self._print_bar(url)

    # ------------- public crawl ---------------
    def crawl(self, entry_url: str):
        self.visited.add(entry_url)
        self.queue.put((entry_url, 0))

        threads = [threading.Thread(target=self._worker, daemon=True) for _ in range(self.workers)]
        for t in threads:
            t.start()

        try:
            self.queue.join()
        finally:
            self.stop_event.set()
            for t in threads:
                t.join()
            sys.stdout.write("\n")  # finish progress line

        return self.md_lines, len(self.visited)

# -----------------------------------------------------------------------------
# Entry‑point
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Multithreaded Redfish crawler → Markdown (stdlib‑only).")
    parser.add_argument("--host", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--outfile", default="redfish_dump.md")
    parser.add_argument("--scheme", choices=["http", "https"], default="https")
    parser.add_argument("--workers", type=int, default=8, help="Number of fetch threads (default 8)")
    parser.add_argument("--verify", action="store_true", help="Enable TLS certificate verification (OFF by default)")
    args = parser.parse_args()

    base_url = f"{args.scheme}://{args.host}/redfish/v1"

    session = StdLibSession(args.username, args.password, verify=args.verify)
    crawler = ConcurrentCrawler(session, args.workers)

    md_lines, total = crawler.crawl(base_url)

    with open(args.outfile, "w", encoding="utf-8") as fp:
        fp.write("\n".join(md_lines))

    print(f"✅ Finished. Dumped {total} endpoints to {args.outfile}.")


if __name__ == "__main__":
    main()

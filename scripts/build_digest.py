#!/usr/bin/env python3
"""Create a research-only digest from public RSS feeds."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from email.utils import parsedate_to_datetime
import html, re, xml.etree.ElementTree as ET

FEEDS = [
    ("Variety", "https://variety.com/feed/"),
    ("The Hollywood Reporter", "https://www.hollywoodreporter.com/feed/"),
    ("Deadline", "https://deadline.com/feed/"),
]
OUT = Path("content/drafts")

def clean(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\\s+", " ", html.unescape(value)).strip()

def parse_feed(name, url):
    req = Request(url, headers={"User-Agent": "KatMoviesWorldResearchBot/1.0"})
    with urlopen(req, timeout=20) as response:
        root = ET.fromstring(response.read())
    channel = root.find("channel")
    if channel is None:
        return []
    rows = []
    for item in channel.findall("item")[:8]:
        title, link = clean(item.findtext("title")), clean(item.findtext("link"))
        if title and link:
            rows.append((name, title, link, clean(item.findtext("description"))[:350], clean(item.findtext("pubDate"))))
    return rows

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, errors = [], []
    for name, url in FEEDS:
        try:
            rows.extend(parse_feed(name, url))
        except Exception as exc:
            errors.append(f"- {name}: {type(exc).__name__}")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# Entertainment research digest — {stamp}", "",
             "> Research notes only. Verify facts independently and write original coverage before publishing.", ""]
    for source, title, link, description, pub_date in rows:
        lines += [f"## {title}", f"- Source: {source}", f"- Link: {link}"]
        if pub_date: lines.append(f"- Published: {pub_date}")
        if description: lines.append(f"- Feed summary (verify): {description}")
        lines += ["- Editorial follow-up: Verify with primary sources and add original context.", ""]
    if errors: lines += ["## Feed errors", *errors, ""]
    if not rows: lines += ["No feed entries retrieved. Check workflow logs and feed availability.", ""]
    path = OUT / f"entertainment-research-{stamp}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(rows)} research items to {path}")

if __name__ == "__main__":
    main()

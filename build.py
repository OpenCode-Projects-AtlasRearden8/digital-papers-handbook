#!/usr/bin/env python3
"""Build the Digital Papers Handbook site.

Converts the markdown pages in docs/ into a small, self-contained static
site in site/. No third-party dependencies: only the Python standard
library is used.

Usage:
    python3 build.py            # build site/ from docs/
    python3 build.py --out DIR  # build into a different directory
    python3 build.py --check    # build, then fail if any internal link is broken
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

PAGES = [
    "index.md",
    "keep-or-toss.md",
    "retention.md",
    "scanning.md",
    "folders-naming.md",
    "find-anything.md",
    "ai-filing.md",
    "shredding.md",
    "yearly-cleanup.md",
    "glossary.md",
]

CSS = """\
:root{--ink:#1f2430;--paper:#fbf8f3;--accent:#2a6f61;--accent-soft:#e3efec;--muted:#6b7280;--line:#e5e1d8}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:16px/1.65 Georgia,'Times New Roman',serif;color:var(--ink);background:var(--paper)}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--accent-soft)}
a:hover{border-bottom-color:var(--accent)}
.container{max-width:960px;margin:0 auto;padding:0 20px;display:flex;gap:36px;align-items:flex-start}
header.site{background:var(--accent);color:#fff;padding:14px 0}
header.site .container{display:block}
header.site strong{font-size:18px}
header.site span{font-size:13px;opacity:.85;display:block}
nav.sidebar{position:sticky;top:20px;width:210px;flex:0 0 210px;padding:18px 0;font-size:14px}
nav.sidebar a{display:block;padding:4px 10px;border:0;border-left:2px solid var(--line);color:var(--ink)}
nav.sidebar a:hover{background:var(--accent-soft)}
nav.sidebar a.current{border-left-color:var(--accent);font-weight:bold;color:var(--accent)}
main{flex:1;min-width:0;padding:28px 0 40px}
h1,h2,h3{line-height:1.25;font-family:'Segoe UI',system-ui,sans-serif}
h1{font-size:30px;margin:0 0 6px}
p.jumpline{color:var(--muted);font-style:italic;margin-top:0}
h2{font-size:22px;margin-top:34px;border-bottom:1px solid var(--line);padding-bottom:4px}
h3{font-size:18px;margin-top:24px}
pre{background:#2b2b33;color:#f4f4f4;padding:14px 16px;border-radius:8px;overflow-x:auto;font-size:13.5px;line-height:1.45}
code{font-family:ui-monospace,Consolas,monospace;font-size:.9em;background:var(--accent-soft);padding:1px 5px;border-radius:4px}
pre code{background:transparent;padding:0;color:inherit}
blockquote{margin:18px 0;padding:10px 18px;border-left:4px solid var(--accent);background:var(--accent-soft);border-radius:0 8px 8px 0}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px}
th,td{text-align:left;padding:8px 10px;border:1px solid var(--line);vertical-align:top}
th{background:var(--accent-soft);font-family:'Segoe UI',system-ui,sans-serif;font-size:14px}
tr:nth-child(even) td{background:rgba(0,0,0,.015)}
footer.site{border-top:1px solid var(--line);color:var(--muted);font-size:13.5px;padding:18px 0 30px}
footer.site .container{display:block}
@media(max-width:760px){.container{display:block}nav.sidebar{width:auto;position:static;padding-bottom:0}main{padding-top:10px}}
"""


def slug_page(md_name: str) -> str:
    return md_name[:-3] + ".html"


# --------------------------------------------------------------------------
# Markdown -> HTML
# --------------------------------------------------------------------------

def _inline(md: str) -> str:
    """Convert inline markdown (code, links, bold, italic) to HTML."""
    md = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    stash: list[str] = []

    def _stash(html: str) -> str:
        stash.append(html)
        return "\x00%d\x00" % (len(stash) - 1)

    # Inline code first, protected from everything else.
    md = re.sub(r"`([^`]+)`", lambda m: _stash("<code>%s</code>" % m.group(1)), md)
    # Links next: [text](url). Internal *.md targets point at site pages.
    def _link(m: "re.Match[str]") -> str:
        url = m.group(2)
        if url.endswith(".md"):
            url = slug_page(url)
        return _stash('<a href="%s">%s</a>' % (url, m.group(1)))

    md = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, md)
    md = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"(?<!\*)\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", md)
    md = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], md)
    return md


def markdown_to_html(md: str) -> str:
    """Convert the subset of markdown used in docs/ to HTML.

    Supports: headings, paragraphs, bullet/numbered lists, pipe tables,
    fenced code blocks, blockquotes, horizontal rules, and inline styles.
    """
    lines = md.splitlines()
    out: list[str] = []
    i = 0

    def flush_paragraph(buf: list[str]) -> None:
        if buf:
            out.append("<p>%s</p>" % _inline(" ".join(buf)).strip())

    para: list[str] = []
    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            flush_paragraph(para)
            para = []
            code: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            body = "\n".join(code).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append("<pre><code>%s</code></pre>" % body)
            continue

        stripped = line.strip()

        # Heading
        m = re.match(r"(#{1,4})\s+(.*)", stripped)
        if m:
            flush_paragraph(para)
            para = []
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2)), level))
            i += 1
            continue

        if not stripped:
            flush_paragraph(para)
            para = []
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flush_paragraph(para)
            para = []
            out.append("<hr>")
            i += 1
            continue

        # Table: a row with pipes, then a separator row of --- cells
        if stripped.startswith("|") and i + 1 < len(lines) and re.fullmatch(
            r"\|(\s*:?-{3,}:?\s*\|)+", lines[i + 1].strip()
        ):
            flush_paragraph(para)
            para = []

            def cells(row: str) -> list[str]:
                parts = row.strip().strip("|").split("|")
                return [c.strip() for c in parts]

            header = cells(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = ["<table>", "<thead>", "<tr>"]
            t += ["<th>%s</th>" % _inline(h) for h in header]
            t += ["</tr>", "</thead>"]
            if rows:
                t.append("<tbody>")
                for r in rows:
                    t.append("<tr>")
                    t += ["<td>%s</td>" % _inline(c) for c in r]
                    t.append("</tr>")
                t.append("</tbody>")
            t.append("</table>")
            out.append("\n".join(t))
            continue

        # Blockquote
        if stripped.startswith(">"):
            flush_paragraph(para)
            para = []
            quote: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].lstrip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>" % _inline(" ".join(quote)))
            continue

        # Bullet list
        if re.match(r"[-*]\s+", stripped):
            flush_paragraph(para)
            para = []
            items: list[str] = []
            while i < len(lines) and re.match(r"[-*]\s+", lines[i].strip()):
                items.append("<li>%s</li>" % _inline(re.sub(r"[-*]\s+", "", lines[i].strip(), count=1)))
                i += 1
            out.append("<ul>\n%s\n</ul>" % "\n".join(items))
            continue

        # Numbered list
        if re.match(r"\d+\.\s+", stripped):
            flush_paragraph(para)
            para = []
            nums: list[str] = []
            while i < len(lines) and re.match(r"\d+\.\s+", lines[i].strip()):
                nums.append(
                    "<li>%s</li>" % _inline(re.sub(r"\d+\.\s+", "", lines[i].strip(), count=1))
                )
                i += 1
            out.append("<ol>\n%s\n</ol>" % "\n".join(nums))
            continue

        # Continuation of a paragraph
        para.append(stripped)
        i += 1

    flush_paragraph(para)
    return "\n".join(out)


def page_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html)
    return re.sub(r"<[^>]+>", "", m.group(1)) if m else "Untitled"


def slugify(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s]+", "-", s.strip())


def add_heading_ids(html: str) -> str:
    def _id(m: "re.Match[str]") -> str:
        level, text = m.group(1), m.group(2)
        return '<h%s id="%s">%s</h%s>' % (level, slugify(text), text, level)

    return re.sub(r"<h([23])>(.*?)</h\1>", _id, html)


def split_title_and_body(html: str) -> tuple[str, str]:
    m = re.search(r"<h1[^>]*>(.*?)</h1>\n?(.*)", html, re.S)
    if not m:
        return "Untitled", html
    return m.group(1), m.group(2)


PAGE_NAV = [
    ("index.html", "Home"),
    ("keep-or-toss.html", "Keep or Toss"),
    ("retention.html", "Retention Table"),
    ("scanning.html", "Scan With Your Phone"),
    ("folders-naming.html", "Folders and Naming"),
    ("find-anything.html", "Find Anything"),
    ("ai-filing.html", "AI Filing (optional)"),
    ("shredding.html", "Shredding Rules"),
    ("yearly-cleanup.html", "Yearly Cleanup"),
    ("glossary.html", "Glossary"),
]

CREDIT = "Asdale Dynamics, LLC"


def render_page(name: str, html: str, current: str) -> str:
    title, body = split_title_and_body(html)
    body = add_heading_ids(body)
    nav = "\n".join(
        '<a href="%s" class="current">%s</a>' % (href, label)
        if href == current
        else '<a href="%s">%s</a>' % (href, label)
        for href, label in PAGE_NAV
    )
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>%s — The Digital Papers Handbook</title>\n"
        "<style>%s</style>\n</head>\n<body>\n"
        '<header class="site"><div class="container"><strong>The Digital Papers Handbook</strong>'
        "<span>Taming paper and digital documents — one hour a year.</span></div></header>\n"
        '<div class="container">\n<nav class="sidebar">%s</nav>\n<main>%s\n</main>\n</div>\n'
        '<footer class="site"><div class="container"><p>%s · '
        'An MIT-licensed handbook from <a href="https://dylanasdale.github.io/">dylanasdale.github.io</a> · '
        "Education only — not legal, tax, or financial advice.</p></div></footer>\n"
        "</body>\n</html>\n" % (title, CSS, nav, body, CREDIT)
    )


def check_links(html: str, available: set[str], page: str) -> list[str]:
    errors: list[str] = []
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http:", "https:", "mailto:")):
            continue
        target = urlparse(href).path or href
        if target in ("", "#"):
            continue
        if target not in available:
            errors.append("%s: broken internal link -> %s" % (page, href))
    return errors


def build(out_dir: Path) -> list[str]:
    """Build the site. Returns a list of problems found (empty = clean)."""
    if not DOCS.is_dir():
        return ["docs/ directory not found next to build.py"]

    problems: list[str] = []
    missing = [p for p in PAGES if not (DOCS / p).is_file()]
    problems += ["missing docs page: %s" % p for p in missing]
    if missing:
        return problems

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    html_pages: dict[str, str] = {}
    for md_name in PAGES:
        md = (DOCS / md_name).read_text(encoding="utf-8")
        body = markdown_to_html(md)
        html_pages[slug_page(md_name)] = body

    available = set(html_pages)  # pages exist even if links are broken
    for page, body in html_pages.items():
        full = render_page(page, body, page)
        problems += check_links(full, available | set(PAGE_NAV), page)
        (out_dir / page).write_text(full, encoding="utf-8")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "site"), help="output directory")
    parser.add_argument("--check", action="store_true", help="fail with a nonzero exit code if problems are found")
    args = parser.parse_args(argv)

    out_dir = ROOT / args.out
    problems = build(out_dir)

    pages = sorted(p.name for p in out_dir.glob("*.html")) if out_dir.is_dir() else []
    print("Built %d pages into %s" % (len(pages), out_dir))
    for p in pages:
        print("  site/%s" % p)
    if problems:
        for p in problems:
            print("PROBLEM: %s" % p, file=sys.stderr)
        return 1
    if args.check:
        print("Link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

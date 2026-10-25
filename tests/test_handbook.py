"""Tests for the Digital Papers Handbook.

Covers four families of checks:

1. Markdown converter behavior (build.py::markdown_to_html)
2. Build output: every page exists and is structurally sound HTML
3. Content guarantees: decision tree, retention table, glossary, links
4. Hygiene: no secrets, no personal data, required credit lines
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

SITE = ROOT / "site"


def html_of(md_name: str) -> str:
    """Render a docs page through the converter and wrap it as a page."""
    md = (build.DOCS / md_name).read_text(encoding="utf-8")
    body = build.markdown_to_html(md)
    return build.render_page(build.slug_page(md_name), body, build.slug_page(md_name))


class ConverterTests(unittest.TestCase):
    def test_headings(self):
        h = build.markdown_to_html("# T\n## S\n### U")
        self.assertIn("<h1>T</h1>", h)
        self.assertIn("<h2>S</h2>", h)
        self.assertIn("<h3>U</h3>", h)

    def test_lists(self):
        h = build.markdown_to_html("- one\n- two\n\n1. a\n2. b")
        self.assertEqual(h.count("<li>"), 4)
        self.assertIn("<ul>", h)
        self.assertIn("<ol>", h)
        self.assertLess(h.index("</ul>"), h.index("<ol>"))

    def test_table(self):
        h = build.markdown_to_html(
            "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        )
        self.assertIn("<table>", h)
        self.assertIn("<th>A</th>", h)
        self.assertIn("<td>2</td>", h)
        self.assertEqual(h.count("<tr>"), 3)

    def test_code_fence_escapes_html(self):
        h = build.markdown_to_html("```\n<div>& stuff\n```")
        self.assertNotIn("<div>", h)
        self.assertIn("&lt;div&gt;", h)

    def test_inline_styles(self):
        h = build.markdown_to_html("**b** and *i* and `c`")
        self.assertIn("<strong>b</strong>", h)
        self.assertIn("<em>i</em>", h)
        self.assertIn("<code>c</code>", h)

    def test_links_rewritten_and_escaped(self):
        h = build.markdown_to_html("[x](retention.md) & <tag>")
        self.assertIn('href="retention.html"', h)
        self.assertIn("&amp;", h)
        self.assertIn("&lt;tag&gt;", h)

    def test_blockquote_and_hr(self):
        h = build.markdown_to_html("> wise words\n\n---\nTail")
        self.assertIn("<blockquote><p>", h)
        self.assertIn("<hr>", h)

    def test_heading_ids_added(self):
        h = build.render_page("t.html", build.markdown_to_html("## A Real Heading"), "t.html")
        self.assertIn('<h2 id="a-real-heading">', h)


class BuildTests(unittest.TestCase):
    """Run the real build into a temp dir and inspect the output."""

    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp(prefix="site-test-"))
        cls.problems = build.build(cls.out)

    @classmethod
    def tearDownClass(cls):
        import shutil

        shutil.rmtree(cls.out, ignore_errors=True)

    def test_build_reports_no_problems(self):
        self.assertEqual(self.problems, [])

    def test_every_page_built(self):
        for name in build.PAGES:
            page = self.out / build.slug_page(name)
            self.assertTrue(page.is_file(), f"missing {page}")

    def test_pages_are_structurally_sound(self):
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("<!DOCTYPE html>"), page.name)
            self.assertIn("</html>", text)
            self.assertEqual(text.count("<main>"), 1, page.name)
            self.assertLess(text.index("<nav"), text.index("<main>"), page.name)
            self.assertIn("<title>", text)
            self.assertIn('lang="en"', text)

    def test_sidebar_navigates_to_all_pages(self):
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            for href, _label in build.PAGE_NAV:
                self.assertIn(f'href="{href}"', text, f"{page.name} missing nav {href}")

    def test_footer_credit_present(self):
        for page in self.out.glob("*.html"):
            self.assertIn("Asdale Dynamics, LLC", page.read_text(encoding="utf-8"))

    def test_markdown_sources_have_no_broken_internal_links(self):
        problems = build.build(self.out)  # rerun and surface anything new
        self.assertEqual(problems, [])


class ContentTests(unittest.TestCase):
    pages = {build.slug_page(name): html_of(name) for name in build.PAGES}

    def test_decision_tree_is_present(self):
        tree = self.pages["keep-or-toss.html"]
        self.assertIn("<pre><code>", tree)
        self.assertIn("Would it cost me real money", tree)
        self.assertIn("Sentimental", tree)

    def test_retention_table_core_rows(self):
        table = self.pages["retention.html"]
        for needle in ("Tax returns", "Insurance policies", "7 years", "Bank statements"):
            self.assertIn(needle, table)
        self.assertEqual(table.count("<table>"), 1)
        self.assertGreaterEqual(table.count("<tr>"), 15)

    def test_glossary_terms(self):
        g = self.pages["glossary.html"]
        for term in ("Local-first", "OCR", "Ctrl+F", "Shred", "Retention period"):
            self.assertIn(term, g)
        self.assertGreaterEqual(g.count("<p>"), 10)

    def test_ai_filing_mentions_local_tool_and_local_first(self):
        a = self.pages["ai-filing.html"]
        self.assertIn("local-file-organizer-cli", a)
        self.assertIn("Ollama", a)

    def test_crumb_links_point_to_real_pages(self):
        for name, h in self.pages.items():
            self.assertIn('href="index.html"', h, f"{name} missing home link")

    def test_yearly_cleanup_has_hourly_plan(self):
        y = self.pages["yearly-cleanup.html"]
        self.assertEqual(y.count("<table>"), 1)
        self.assertIn("10", y)

    def test_disclaimer_present(self):
        i = self.pages["index.html"]
        self.assertIn("not legal, tax, or financial advice", i)


class HygieneTests(unittest.TestCase):
    SECRET_PATTERNS = [
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"AKIA[0-9A-Z]{16}",
        r"sk-[A-Za-z0-9-]{20,}",
        r"ghp_[A-Za-z0-9]{36}",
        r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]{16,}",
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN-shaped numbers
        r"\b(?:4\d{12}|5[1-5]\d{14}|3[47]\d{13})\b",  # cc-shaped numbers
    ]

    def test_no_secrets_anywhere(self):
        offenders: list[str] = []
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or "site" in path.relative_to(ROOT).parts:
                continue
            if path.suffix not in {".md", ".py", ".html", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in self.SECRET_PATTERNS:
                for m in re.finditer(pattern, text):
                    offenders.append(f"{path.name}: {pattern}: {m.group(0)[:12]}...")
        self.assertEqual(offenders, [])

    def test_license_copyright_line_exact(self):
        lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", lic)
        self.assertTrue(lic.startswith("MIT License"))

    def test_readme_credits_llc(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("MIT", readme)

    def test_build_py_has_no_dependencies_beyond_stdlib(self):
        src = (ROOT / "build.py").read_text(encoding="utf-8")
        imports = set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", src, re.M))
        stdlib = {
            "argparse", "re", "shutil", "sys", "pathlib", "__future__",
            "urllib.parse",
        }
        self.assertTrue(imports <= stdlib, f"unexpected imports: {imports - stdlib}")


class SiteOutputTests(unittest.TestCase):
    """If site/ has been built (repo checkout), sanity-check committed output too."""

    def setUp(self):
        if not SITE.is_dir():
            self.skipTest("site/ not built yet — run build.py first")

    def test_site_pages_match_doc_page_count(self):
        built = sorted(p.name for p in SITE.glob("*.html"))
        expected = sorted(build.slug_page(n) for n in build.PAGES)
        self.assertEqual(built, expected)


if __name__ == "__main__":
    unittest.main()

# STATUS.md — The Digital Papers Handbook

Last updated: 2026-10-25

## What was built

A complete, local-first manual for taming paper and digital documents:

- **10 markdown chapters in `docs/`** — homepage, keep-or-toss decision tree, retention table (taxes/insurance/bills and 20+ document types), phone scanning guide, folder-and-naming system, Ctrl+F "find anything in five seconds" skills, optional AI-assisted filing with `local-file-organizer-cli`, shredding rules, the yearly one-hour cleanup, and a plain-English glossary.
- **`build.py`** — a dependency-free (stdlib-only) markdown → static HTML site generator. Converts all docs into a styled, navigable static site in `site/`, rewrites internal `.md` links to `.html`, adds heading anchors, a sticky sidebar nav, and an LLC credit footer. `--check` mode fails on broken internal links; `--out` builds elsewhere.
- **`site/`** — the generated static site (10 pages, no server needed; open `site/index.html` in a browser).
- **`tests/test_handbook.py`** — 26 unittest checks across converter behavior, build output integrity, content guarantees (decision tree, retention rows, glossary terms, AI-filing tool coverage), internal-link resolution, no-secrets/no-personal-data scanning, and LICENSE/README credit verification.
- **`LICENSE`** — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.
- **`README.md`** — run instructions, layout, design principles, and credit to Asdale Dynamics, LLC.

## How to run it

```bash
python3 build.py                            # build the static site into site/
python3 build.py --check                    # build + fail on broken internal links
python3 -m unittest discover -s tests -v    # run the test suite
```

Requires Python 3.10+ only — no packages to install, nothing leaves your machine.
To read the site: open `site/index.html` in any browser.

## Verification results (all pass)

- `python3 build.py --check` → built 10 pages, **link check passed**.
- `python3 -m unittest discover -s tests` → **26/26 OK**, covering:
  - converter: headings, lists, tables, code-fence escaping, inline styles, `.md`→`.html` link rewrite, blockquotes/HR, heading IDs
  - build: every page exists, valid HTML skeleton, sidebar nav on all pages, footer credit present, zero broken internal links
  - content: decision tree present, retention table has ≥15 rows incl. tax/insurance/bank rows, glossary terms present, `local-file-organizer-cli` + local-first covered in AI-filing chapter, disclaimer present
  - hygiene + output: no secrets/personal data patterns in any source file, exact LICENSE copyright line, README credits the LLC, post-build `site/` matches the page list
- Rendered-HTML artifact scan: zero stray `**`, raw markdown links, or leaked `<h4>` tags in output.

## Known gaps / honest limitations

- **Guidance, not legal advice.** Retention periods reflect widely repeated US-general-practice rules (7-year tax cushion, etc.); state and personal situations vary, and the handbook says so on every page that needs to.
- **Converter covers the handbook's markdown subset** — headings, tables, lists, code fences, blockquotes, inline styles, links. It is intentionally not a full CommonMark parser; exotic markdown would need extending `build.py`.
- **`site/` is generated output** — it is not the source of truth; rerun `build.py` after editing `docs/` (a test skips rather than fails if `site/` isn't present).
- **`local-file-organizer-cli` chapter** documents the *pattern* of safe local AI filing (point it at your folder tree, confirm before moves, back up first) rather than pinning flaky version numbers; readers are pointed at the tool's own README for exact install lines.
- **No search across the finished site** — the handbook teaches file Ctrl+F skills, but the static site itself relies on browser-native Ctrl+F, which is in keeping with its own advice.
- No CI configured (this was built to run locally); everything above was verified by running the commands listed.

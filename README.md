# The Digital Papers Handbook

Decide what to keep, scan the rest with your phone, name files so search finds them in five seconds, shred safely, and spend one hour a year keeping it that way.

A plain-English, ADHD-friendly manual for taming paper and digital documents — built to be read, not admired. Everything is local-first: your files stay on your computer, with cloud syncing welcome as *backup*, never as the master copy.

**Contents:**

| Page | What it answers |
|---|---|
| [Keep or Toss](site/keep-or-toss.html) | The decision tree: digital vs paper vs shredder |
| [Retention Table](site/retention.html) | How long to keep taxes, insurance, bills, records |
| [Scan With Your Phone](site/scanning.html) | Clean digital copies in two minutes |
| [Folders and Naming](site/folders-naming.html) | Nine folders, one naming rule |
| [Find Anything in Five Seconds](site/find-anything.html) | Ctrl+F skills that replace browsing |
| [AI-Assisted Filing (Optional)](site/ai-filing.html) | `local-file-organizer-cli` and friends, done safely |
| [Shredding Rules](site/shredding.html) | What gets shredded vs recycled |
| [Yearly Cleanup](site/yearly-cleanup.html) | The entire maintenance plan, in 60 minutes |
| [Glossary](site/glossary.html) | Every term, in plain English |

## Run it

Requirements: Python 3.10+ (standard library only — nothing to install).

```bash
python3 build.py          # builds the static site into site/
python3 build.py --check  # also fail on broken internal links
python3 -m unittest discover -s tests -v   # run the test suite
```

Read the markdown directly in [docs/](docs/), or open `site/index.html` in a browser after building.

## Repository layout

```
docs/       10 markdown chapters (the handbook itself)
build.py    dependency-free markdown → static HTML site generator
tests/      unittest suite: converter, build output, link check, no-secrets scan
site/       generated static site (not committed source of truth; rebuild anytime)
```

## Design principles

1. **Local-first.** All content and tooling runs on your machine. The site is static HTML you can open from a folder — no server, no accounts, no telemetry.
2. **Plain and warm.** Step-by-step, never condescending. If a rule has an exception, the exception is stated.
3. **Tested.** The build output is checked by an automated test suite: every page builds, every internal link resolves, the retention table and decision tree are present, and no file contains secrets or personal data.

## Found a gap?

These chapters reflect widely repeated guidance, not legal advice — tax, insurance, and property rules vary by state and by situation. When in doubt, ask a qualified professional, or simply keep the paper a bit longer. Corrections and improvements are welcome: this handbook is MIT licensed.

## License & credit

The Digital Papers Handbook is an open-source project by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and practical tools from [dylanasdale.github.io](https://dylanasdale.github.io/). Licensed under the [MIT License](LICENSE); see LICENSE for the full text.

Education only — never legal, tax, or financial advice.

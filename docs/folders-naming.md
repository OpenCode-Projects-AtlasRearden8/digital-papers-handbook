# Folders and Naming: A System You'll Actually Use

*Filing fails when it's too clever. This system has maybe nine folders and one naming rule. It survives being ignored for months.*

---

## The folder tree

Create this once, in your Documents folder (and, if you like, mirror inside your synced drive):

```
Documents/
├── Papers/
│   ├── 01-Taxes/
│   ├── 02-Insurance/
│   ├── 03-Home/
│   ├── 04-Vehicles/
│   ├── 05-Money/
│   ├── 06-Health/
│   ├── 07-Purchases/
│   ├── 08-People/
│   └── 09-Archive/
```

That's the whole system. Numbered prefixes keep the order in every file browser, and the numbers are few enough that "which number is insurance?" becomes muscle memory within a week.

What lives where:

| Folder | Contents |
|---|---|
| 01-Taxes | Tax returns and anything that supports them |
| 02-Insurance | Policies, claim paperwork, coverage letters |
| 03-Home | Deed, mortgage, inspection reports, leases, home improvement receipts |
| 04-Vehicles | Titles, registration, maintenance, insurance cards |
| 05-Money | Bank and credit statements, loan payoff letters |
| 06-Health | Medical bills, EOBs, records |
| 07-Purchases | Receipts, warranties, manuals — one subfolder per big purchase |
| 08-People | Documents about specific people (kids' school records, etc.) |
| 09-Archive | Completed chapters: the 2023 taxes before next spring, closed-out warranties |

Subfolders go **one level deep**, by year where it helps:

```
01-Taxes/
├── 2024/
└── 2025/
07-Purchases/
└── 2026-05-Laptop/
```

If you catch yourself making a subfolder with fewer than three files in it — you don't need that subfolder. Naming handles it. See below.

## The one naming rule

> **Year-Month-Shorthand-Version**, e.g. `2025-11-Electric-Bill-Nov.pdf`

Broken down:

- **Year-Month first** (`2025-11`) — files sort themselves chronologically everywhere, forever.
- **Short plain shorthand** (`Electric-Bill-Nov`) — "what is this?" answered in the filename. You should never again open a file just to find out what it is.
- **Version only when versions exist** (`-v2` only if a document truly changes).

## Examples for common documents

| What it is | Name |
|---|---|
| November 2025 electric bill, $84.12, paid | `2025-11-Electric-Bill-Nov-Paid.pdf` |
| Auto insurance policy renewing Nov 1, 2026 | `2026-Auto-Insurance-Policy.pdf` |
| Home insurance claim after a January 2025 storm | `2025-01-Home-Insurance-Claim.pdf` |
| 2024 tax return with supporting documents | `2025-04-Tax-Return-2024.pdf` |
| Receipt for a laptop purchased May 2026 | `2026-05-Laptop-Receipt.pdf` |
| Mortgage statement, October 2025 | `2025-10-Mortgage-Statement.pdf` |
| Warranties, car bought June 2026 | `2026-06-Car-Purchase.pdf` |

(You don't need dollar amounts in filenames — the document has that. "Paid" / "Unpaid" is worth including if unpaid bills are ever a thing you track.)

## The two habits that keep it working

1. **Name at the moment of saving or scanning.** Renaming later is a chore; naming now is two seconds. If it slips through unnamed, the [yearly cleanup](yearly-cleanup.md) catches it.
2. **When in doubt, put it in 09-Archive with a good name.** An archived file with a good name is findable forever with [Ctrl+F](find-anything.md). A beautifully-organized file you can't find is not.

## If your files are currently... chaos

Don't reorganize the existing pile folder-by-folder. Instead:

1. Create the tree above, right now.
2. Use it going forward, starting today. New files land properly named in the right folders.
3. Fold old files into the system *opportunistically* — when you happen to touch an old folder, sort what's in it. Ten files a week beats a reorganization weekend that never happens.

Next: making everything findable in five seconds — [Find Anything in Five Seconds](find-anything.md).

[Back to the handbook index](index.md)

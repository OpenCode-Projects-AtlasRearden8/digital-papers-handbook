# AI-Assisted Filing (Optional)

*A local command-line tool can suggest where each new file belongs, based on your own folder system. This is genuinely optional — the manual system works forever — but if you enjoy having a helper, here's the friendly version.*

---

## What this chapter is

This chapter shows how to use an AI filing helper that runs **on your own computer** to:

1. Look at a new file's name (and, in some cases, its content),
2. Suggest which of your existing folders it belongs in,
3. Move it there when you say yes.

It's the "auto-pilot" version of [Folders and Naming](folders-naming.md) — the folders and the naming rule stay exactly the same; the helper just does the two seconds of thinking for you.

## What to look for in a filing helper

Whatever tool you pick (including the `local-file-organizer-cli` mentioned below), check for the same three things this handbook requires of every tool:

- **Runs locally.** Your file names and documents stay on your machine. The helper should work offline or send nothing Telemetry-able. If a tool requires uploading your papers to someone's server, skip it.
- **Suggests, then asks.** You want a tool that proposes a destination and waits for a yes — not one that shuffles files silently.
- **Knows your folders.** If it can't see (or be taught) your `Papers/` tree, it can't file into your system.

## Meet `local-file-organizer-cli`

`local-file-organizer-cli` is a small open-source command-line tool that watches a folder (or processes files you pass to it), uses a local model (like Ollama) to guess what each file is, proposes a destination folder, and moves it on your confirmation. Nothing leaves your computer: the model runs on your own hardware.

### Setup (one evening, once)

1. **Install Ollama** (the local model runner) from `ollama.com` for your platform. Test with `ollama pull llama3.2` — a small model is plenty for filing.
2. **Install the tool** — with Python installed, it's typically:

   ```
   pip install local-file-organizer-cli
   ```

   (Check the project's own README for the current install line — this handbook deliberately doesn't reproduce version numbers that drift.)
3. **Point it at your folder system.** Most organizer tools of this kind want two things: a source folder (where unsorted files land, e.g. `Downloads/Paper-Inbox/`) and a destination tree (your `Documents/Papers/` folders from [Folders and Naming](folders-naming.md)).

### The daily-flow version

- Unsorted files drop into your **paper inbox** folder (just a folder — call it `Paper-Inbox`).
- Once a day (or whenever you feel like it — low-energy friendly), run the organizer on that folder.
- It lists each file with a proposed destination: *"2026-05-Laptop-Receipt.pdf → 07-Purchases — confirm?"* You press Y/N.
- Approvals get moved; your inbox stays clear.

### If AI filing sounds like too much

That's a legitimate answer, not a failure. The manual system on [Folders and Naming](folders-naming.md) is complete without it, and the [yearly cleanup](yearly-cleanup.md) covers the slippage. Tools like this shine after your folder system has existed for a few months, when there's a clear pattern for them to learn or follow. Add it then, if ever.

## A gentle note on AI and your documents

Keep sensitive originals sensible: don't point a filing helper at a folder of anything you wouldn't paste into a chat window — local-first tools keep things on your machine, but you're the one who decides what they get to read. That judgment is the same one from [Keep or Toss](keep-or-toss.md), applied to software.

And one caution for any filing tool (AI or otherwise): **back up before big moves.** A tool that moves hundreds of files with a single command deserves a folder that's synced or copied somewhere first. [Shredding Rules](shredding.md) apply to digital files too — an accidental destruction is still a destruction.

[Back to the handbook index](index.md)

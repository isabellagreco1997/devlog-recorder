---
name: devlog-recorder
description: Keep a video-ready record of a session while it happens, whatever the session is. Building something, researching a topic, reading articles and threads, comparing tools, debugging, planning, learning. Every prompt, every output, screenshots of what was looked at, produced assets, short clips of anything that moves, the sources and the exact quotes, in order, with the user's words verbatim. Use whenever the user is doing something over several turns that they might want to show or retell later (a devlog video, a write-up, a talk, a bug report, a decision record). Works with any agent that can run shell commands.
---

# devlog-recorder — the agent's playbook

You are doing something with a person: building, researching, reading, deciding, debugging, learning. Later they will want to tell the story of it, and the story lives in the details nobody remembers a week on: what they asked, what came back, the ugly first attempt, the article that changed their mind, the tweet that started it, the moment it broke, the fix, the number. Your job on top of the actual work: **record it as it happens**, in a form a script writer (or you, later) can turn straight into a video with a picture for every beat.

Tool: the `devlog` CLI in this repo (`pip install -e .`, `npm install` for the Chrome capture, `ffmpeg` on the PATH). One folder per session under `devlog/<name>/`: `log.md` (readable), `timeline.json` (data), `assets/`, `clips/`, `sheets/`, `brief.md`.

## 1. Start

* When the user starts something that will take more than one turn, or says "keep a devlog": `devlog init <short-name>`. Say one line: "I'm keeping a devlog in devlog/<name>/ as we go." The log itself needs no permission; capturing the screen of anything outside the work (their desktop, other apps, a private tab) does.
* Reopening later: `devlog init` with the same name reattaches. One journal per thing, never two.

## 2. Every turn, log the turn

After a message that moved things forward, before you stop:

```
devlog note --user "<what they said, verbatim, trimmed to the part about the work>" \
            --agent "<what you did and what came out, one or two sentences, plain>" \
            --tags <see below> --files <any file you produced this turn>
```

* **Verbatim.** Their words are the script. "make her legs closer together", "is this guy even right?", "ok that's enough for today" stay exactly that. Never paraphrase into something stronger or tidier, never invent sentiment.
* **What happened, not what you intended.** "Rendered the walk; her feet cover a third of the ground she travels, she skates" beats "Improved the walk". "The article says X, the thread says the opposite, the numbers in the paper support the thread" beats "Did research".
* **Tags that make the brief write itself:** `fail` (came out wrong), `bug` (errored), `surprise` (not what anyone expected), `fix`, `rule` (a lesson that became a rule), `decision` (the user chose), `win` (the user liked it), `milestone`, `aside` (a joke or detour worth keeping).
* Log the misses and the dead ends. A devlog with only wins is a brochure; the fails and the surprises are the video.

## 3. Capture the evidence at the moment it exists

The picture that shows a beat has to be taken **when that state exists**, because the next turn overwrites it, the tab gets closed, the page changes.

**When the user is making something**
* Anything you produced (an image, a sheet, a chart, a diagram, a file, terminal output saved to .txt): `devlog add <file> --caption "..."`. Copied under a sequence number; the original may change later.
* A page or an HTML thing (a game, a dashboard, a rendered doc): `devlog shot index.html --caption "first playable"`; `--scroll "#section"` for a part.
* Anything that moves (a game, a GIF, an animation, a render): `devlog clip <target> --dur 6`. HTML/URL is recorded live in headless Chrome; give it input so something happens: `--keys "ArrowRight:0-2500,Space:800-900"`. A `.gif`/`.mp4` is trimmed. 4 to 8 seconds, one moment per clip.
* Every visual fix: `devlog compare old.png new.png --caption "tube legs vs real legs"`. The most useful frame a devlog holds.
* Sprites and pixel art: native size plus an upscaled copy, nearest-neighbour.

**When the user is finding something out**
* An article, a paper, a docs page, a tweet or thread, a search result, a product page: `devlog source <url> --quote "<the exact sentence that mattered>" --caption "..."`. One entry: screenshot, link, quote. `--scroll "#Reception"` to land on the paragraph. If the page can't be captured (login, paywall), the entry still records the link and the quote.
* What the user concluded from it: a `note` with `--tags decision` (or `surprise`). Their reasoning in their words.
* A comparison (tools, options, prices, claims): a `note` whose `--agent` text holds the actual numbers, side by side. Numbers in the log become counters and chips in the video.
* Something seen on their own screen (a desktop app, an email, a terminal): `devlog screen --caption "..."` (`--window` to pick one window on macOS). Ask first; crop or skip anything private.

**Always**
* Numbers the user might quote (a ratio, a price, a count, a time) go in the `--agent` text.
* A turning point deserves two captures: the state before and the state after.

## 4. Keep it honest and safe

* No secrets, tokens, passwords, `.env` contents, ever, even inside a screenshot: crop or skip.
* No absolute paths from the user's machine, no other people's names unless the user put them in the work, no client, customer or private-message content.
* Don't log chit-chat, only turns that changed the work. If in doubt, one line.
* Never edit or renumber earlier entries. If something was wrong, add a new entry that says so. The order is the story.

## 5. Milestones and the end

* At each milestone and whenever the user says they're done for now: `devlog sheet` (contact sheet of every asset) and `devlog brief` (writes `brief.md`: turning points, sources with quotes, every beat with its quote and its picture, and a script skeleton). Tell the user where it is.
* Hand-off to a video: `brief.md` is the shot plan. Each beat is one shot, its `show:` line is the picture, the quotes are the narration's raw material. The script-to-video skill (github.com/isabellagreco1997/script-to-video) builds the video from there.

## 6. Cadence that works

One `note` per turn that mattered, one capture per new state, one `source` per thing read, one `compare` per fix, one `clip` per thing that moves, `brief` at milestones. A one-hour session should leave 15 to 40 entries and a contact sheet that tells the story with no narration. If the sheet doesn't, you captured the wrong things: go back to rule 3.

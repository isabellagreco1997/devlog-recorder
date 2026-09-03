---
name: devlog-recorder
description: Keep a video-ready record of a build session while it happens. Every prompt, every output, screenshots, produced assets, short clips of anything that moves, in order, with the user's words verbatim. Use whenever the user is making something over several turns and might want to show the process later (a devlog video, a write-up, a talk, a bug report). Works with any agent that can run shell commands.
---

# devlog-recorder — the agent's playbook

You are building something with a person. Later they will want to tell the story of how it was built, and the story lives in the details nobody remembers a week on: what they asked, what came back, the ugly first attempt, the moment it broke, the fix. Your job on top of the actual work: **record it as it happens**, in a form a script writer (or you, later) can turn straight into a video with picture for every beat.

Tool: the `devlog` CLI in this repo (`pip install -e .`, `npm install` for the Chrome capture, `ffmpeg` on the PATH). One folder per project under `devlog/<name>/`: `log.md` (readable), `timeline.json` (data), `assets/`, `clips/`, `sheets/`, `brief.md`.

## 1. Start

* First time the user starts making something over more than one turn: `devlog init <project-name>`. Say one line: "I'm keeping a devlog in devlog/<name>/ as we go." Don't ask permission for the log itself; do ask before capturing the screen of anything outside the project (their desktop, other apps).
* Reopening a project later: `devlog init` with the same name reattaches. Never start a second journal for the same thing.

## 2. Every turn, log the turn

After you answer a message that moved the work forward, before you stop:

```
devlog note --user "<what they said, verbatim, trimmed to the part about the work>" \
            --agent "<what you did and what came out, one or two sentences, plain>" \
            --tags <see below> --files <any file you produced this turn>
```

* **Verbatim.** Their words are the script. "make her legs closer together" stays exactly that. Never paraphrase into something stronger or tidier, and never invent sentiment.
* **What happened, not what you intended.** "Rendered the walk cycle; her feet cover 1/3 of the ground she travels, she skates" beats "Improved the walk cycle."
* **Tags that make the brief write itself:** `fail` (it came out wrong), `bug` (it errored), `fix` (a fail resolved), `rule` (a lesson that became a rule/skill line), `win` (something the user liked), `milestone` (a stage done), `decision` (user chose between options), `aside` (a joke or a detour worth keeping).
* Log the misses. A devlog with only wins is a brochure; the fails are the video.

## 3. Capture the evidence, at the moment it exists

The picture that shows a beat must be taken **when that state exists**, because the next turn overwrites it. Rules of thumb:

* **Anything you produced** (an image, a sheet, a sprite, a chart, a diagram, terminal output saved to a .txt): `devlog add <file> --caption "..."`. It is copied under a sequence number; the original can change later.
* **A web page or an HTML thing** (a game, a dashboard, a rendered page): `devlog shot index.html --caption "first playable"`. For a specific part: `--scroll "#section"`.
* **Anything that moves** (a game, a GIF, an animation, a video render): `devlog clip <target> --dur 6`. HTML/URL is recorded live in headless Chrome; give it input so something happens: `--keys "ArrowRight:0-2500,Space:800-900"` (key, held from ms to ms). A `.gif` or `.mp4` is converted/trimmed. 4 to 8 seconds; one moment per clip, not a tour.
* **Before/after** whenever you fix something visual: `devlog compare old.png new.png --caption "tube legs vs real legs"`. This is the single most useful frame a devlog can hold.
* **Desktop apps, terminals, editors:** `devlog screen --caption "..."` (or `--window` to pick a window on macOS). Ask before grabbing anything that isn't the project.
* **Sprites and pixel art:** capture at native size, and also an upscaled copy (`--caption` it "8x") so the sheet is readable. Nearest-neighbour, never smoothed.
* **Numbers the user might quote** (a ratio, a cell size, a file count, a time): put them in the `--agent` text. Numbers in the log become counters and chips in the video.

## 4. Keep it honest and safe

* No secrets, tokens, passwords, or `.env` contents ever reach the log, even inside a screenshot: crop or skip.
* No absolute paths from the user's machine, no other people's names unless the user put them in the work, no client or customer data.
* Don't log chit-chat, only turns that changed the work. If in doubt, one line.
* Never edit or renumber earlier entries. If something was wrong, add a new entry that says so. The order is the story.

## 5. Milestones and the end

* At each milestone and whenever the user says they're done for now: `devlog sheet` (contact sheet of every asset) and `devlog brief` (writes `brief.md`: turning points, every beat with its quote and its picture, and a script skeleton). Tell the user where it is.
* Hand-off to a video: `brief.md` is the shot plan. Each beat is one shot; its `show:` line is the picture; the quotes are the narration's raw material. The script-to-video skill (github.com/isabellagreco1997/script-to-video) builds the video from there.

## 6. Cadence that works

One `note` per turn that mattered, one capture per new state, one `compare` per fix, one `clip` per thing that moves, `brief` at milestones. A one-hour session should leave 15 to 40 entries and a contact sheet that tells the story without a word of narration. If the sheet doesn't, you captured the wrong things: go back to rule 3.

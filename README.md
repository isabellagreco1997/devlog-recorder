# devlog-recorder

**Record what you do with an AI agent as a video-ready devlog.** Building a game, researching a topic, reading articles and threads, comparing tools, debugging, planning. Every prompt, every output, screenshots of what was looked at, produced assets, short clips of anything that moves, the sources and the exact quotes, in order, with your words kept verbatim. When you're done you have the whole story on one contact sheet and a beat-by-beat brief ready for a script.

Works with any agent that can run shell commands: Claude Code, Codex, Cursor, Gemini CLI, a person with a terminal.

<p align="center"><img src="examples/pong/devlog/pong/sheets/contact.jpg" width="100%"><br><sub>One session, one sheet: the Pong example below, five turns.</sub></p>

## Why

The devlog is the most watched format in indie game dev and the most useful format everywhere else, and its material is exactly what gets lost while you're doing the thing: the first ugly attempt, what you said when it broke, the article that changed your mind, the fix, the numbers. This makes the agent keep that material as a side effect of working, so the video, the write-up or the talk is a script away.

## Make it work with your agent

You don't write the log. The agent does, following `SKILL.md`. Three steps:

**1. Install the tool** (once, on the machine the agent works on)

```bash
git clone https://github.com/isabellagreco1997/devlog-recorder
cd devlog-recorder
pip install -e .        # Pillow only
npm install             # puppeteer-core, uses the Chrome you already have
brew install ffmpeg     # or apt / choco
```

**2. Give the agent the playbook**

* **Claude Code**: copy or symlink this folder into `~/.claude/skills/devlog-recorder`. The skill loads itself when a session looks like something worth recording.
* **Codex**: add to your `AGENTS.md`: `Read /path/to/devlog-recorder/SKILL.md and follow it for every multi-turn session.`
* **Cursor / Windsurf / Gemini CLI / anything with a rules or system-prompt file**: paste the contents of `SKILL.md` into it, or one line that points at the file.
* **Any chat agent with a shell**: start the session with "Read devlog-recorder/SKILL.md and keep a devlog of this session."

**3. Say the word**

"Keep a devlog of this" at the start, or nothing at all if the skill is installed. Then work as usual. At the end: "write the brief". Everything is in `devlog/<name>/`.

If you want to check what the agent is doing: `devlog status` lists the last entries, `log.md` is readable in any Markdown viewer with the images inline.

## What the agent runs

```bash
devlog init pong                                   # devlog/pong/, active in this folder
devlog note --user "make me a pong game in one html file" --agent "Wrote index.html: canvas, two paddles, AI on both sides" --tags milestone
devlog shot index.html --caption "first playable"
devlog clip index.html --dur 6 --keys "ArrowUp:0-1200,ArrowDown:1400-2600" --caption "left paddle on the arrows"
devlog add sprite.png --caption "the extracted sprite"
devlog compare v1.png v2.png --caption "tube legs vs real legs"
devlog source "https://en.wikipedia.org/wiki/Pong" --quote "Pong was the first commercially successful video game" --scroll "#History"
devlog screen --caption "the editor"                # desktop grab (asks you first)
devlog sheet                                       # sheets/contact.jpg
devlog brief                                       # brief.md
```

What you get, in `devlog/<name>/`:

```
log.md          readable, chronological, one section per entry, images inline, links and quotes
timeline.json   the same as data
assets/         001-first-playable.png, 004-wikipedia-pong.png, ...
clips/          003-left-paddle-on-the-arrows.mp4, ...
sheets/         contact.jpg
brief.md        turning points (fail / surprise / fix / decision / win), sources with quotes,
                every beat with its quote and its picture, a script skeleton
```

## The rules the agent follows

Written in full in [`SKILL.md`](SKILL.md). The short version:

1. One note per turn that changed the work. Your words verbatim, what happened in plain words, tags: `fail`, `bug`, `surprise`, `fix`, `rule`, `decision`, `win`, `milestone`, `aside`.
2. Capture the evidence at the moment it exists; the next turn overwrites it, the tab gets closed.
3. Everything read gets a `source` with the exact quote. Anything that moves gets a 4 to 8 second clip. Every visual fix gets a before/after.
4. Log the misses and the dead ends. They are the video.
5. No secrets, no machine paths, no other people's data. Never renumber the past.
6. At milestones: `sheet` and `brief`.

## From devlog to video

`brief.md` is a shot plan: each beat is a shot, its `show:` line is the picture, the quotes are the narration's raw material. [script-to-video](https://github.com/isabellagreco1997/script-to-video) turns a script plus those assets into the finished video.

## Examples

* [`examples/pong/`](examples/pong): a one-file Pong game and the devlog kept while making it (shots, two clips, a before/after).
* [`examples/research/`](examples/research): a reading session about one question, with sources, quotes and a decision.

Each has a `run_example.sh` that rebuilds its devlog from scratch.

## License

MIT.

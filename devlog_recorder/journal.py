"""The journal: one folder per project, one numbered entry per thing that happened.

devlog/<name>/
  log.md          human-readable, chronological, one section per entry
  timeline.json   the same entries as data (what a script builder reads)
  assets/         NNN-name.png|jpg|gif|txt  copies of what was produced or captured
  clips/          NNN-name.mp4              short clips of anything that moves
  sheets/         contact sheets
  brief.md        generated: the story so far, beats + quotes + artifacts
"""
import json, re, shutil, time
from datetime import datetime
from pathlib import Path

CONFIG = ".devlog.json"


def slug(s: str, n: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:n] or "item"


class Journal:
    def __init__(self, root: Path):
        self.root = Path(root); self.name = self.root.name
        for d in ("assets", "clips", "sheets", "tmp"): (self.root / d).mkdir(parents=True, exist_ok=True)
        self.tl = self.root / "timeline.json"; self.log = self.root / "log.md"
        if not self.tl.exists(): self.tl.write_text("[]")
        if not self.log.exists(): self.log.write_text(f"# {self.name} devlog\n\nStarted {datetime.now():%Y-%m-%d %H:%M}.\n")

    # ---------- locating the active journal
    @classmethod
    def active(cls, start: Path | None = None) -> "Journal":
        """The journal named in .devlog.json in the current directory or any parent, or DEVLOG env."""
        import os
        if os.environ.get("DEVLOG"): return cls(Path(os.environ["DEVLOG"]))
        p = (start or Path.cwd()).resolve()
        for d in [p, *p.parents]:
            c = d / CONFIG
            if c.exists(): return cls(Path(json.load(open(c))["journal"]))
        raise SystemExit("no active devlog here: run `devlog init <name>` first (or set DEVLOG=/path/to/devlog/<name>)")

    @classmethod
    def init(cls, name: str, base: str = "devlog") -> "Journal":
        root = Path(base).resolve() / slug(name, 60); j = cls(root)
        json.dump({"journal": str(root)}, open(CONFIG, "w")); return j

    # ---------- entries
    def entries(self) -> list[dict]: return json.loads(self.tl.read_text())

    def _next(self) -> int: return len(self.entries()) + 1

    def _save(self, e: dict):
        es = self.entries(); es.append(e); self.tl.write_text(json.dumps(es, indent=1, ensure_ascii=False))
        with open(self.log, "a") as f: f.write(self._md(e))

    def _md(self, e: dict) -> str:
        t = datetime.fromtimestamp(e["time"]).strftime("%H:%M")
        out = [f"\n## {e['n']:03d} · {t} · {e['kind']}"]
        if e.get("user"): out.append(f"\n**User said:** {e['user']}")
        if e.get("agent"): out.append(f"\n**What happened:** {e['agent']}")
        if e.get("caption"): out.append(f"\n{e['caption']}")
        if e.get("url"): out.append(f"\nSource: <{e['url']}>")
        if e.get("quote"): out.append(f"\n> {e['quote']}")
        for f in e.get("files", []):
            rel = Path(f).name; d = Path(f).parent.name
            out.append(f"\n![{rel}]({d}/{rel})" if rel.lower().endswith((".png", ".jpg", ".jpeg", ".gif")) else f"\n- `{d}/{rel}`")
        if e.get("tags"): out.append(f"\n_tags: {', '.join(e['tags'])}_")
        return "\n".join(out) + "\n"

    def note(self, user: str = "", agent: str = "", caption: str = "", tags=None, files=None, url: str = "", quote: str = "", kind: str = "note") -> dict:
        e = dict(n=self._next(), time=time.time(), kind=kind, user=user, agent=agent, caption=caption, tags=tags or [], files=[str(f) for f in (files or [])])
        if url: e["url"] = url
        if quote: e["quote"] = quote
        self._save(e); return e

    def add(self, src: str, caption: str = "", tags=None, kind: str = "asset", user: str = "", agent: str = "") -> dict:
        """Copy a produced file into assets/ (or clips/ for video) under a sequence number and record it."""
        s = Path(src); n = self._next(); sub = "clips" if s.suffix.lower() in (".mp4", ".mov", ".webm") else "assets"
        dst = self.root / sub / f"{n:03d}-{slug(caption or s.stem)}{s.suffix.lower()}"
        shutil.copy2(s, dst)
        e = dict(n=n, time=time.time(), kind=kind, user=user, agent=agent, caption=caption, tags=tags or [], files=[str(dst)])
        self._save(e); return e

    def record(self, kind: str, files: list, caption: str = "", tags=None, user: str = "", agent: str = "", url: str = "", quote: str = "") -> dict:
        e = dict(n=self._next(), time=time.time(), kind=kind, user=user, agent=agent, caption=caption, tags=tags or [], files=[str(f) for f in files])
        if url: e["url"] = url
        if quote: e["quote"] = quote
        self._save(e); return e

    def next_path(self, sub: str, name: str, ext: str) -> Path:
        return self.root / sub / f"{self._next():03d}-{slug(name)}{ext}"

    # ---------- the brief: what a script writer needs
    def brief(self) -> str:
        es = self.entries()
        if not es: return "# brief\n\n(empty devlog)\n"
        t0 = es[0]["time"]; t1 = es[-1]["time"]
        L = [f"# {self.name}: the story so far", "",
             f"{len(es)} entries over {(t1 - t0) / 3600:.1f} h ({datetime.fromtimestamp(t0):%Y-%m-%d %H:%M} to {datetime.fromtimestamp(t1):%H:%M}). "
             f"{sum(len(e.get('files', [])) for e in es)} artifacts, {sum(1 for e in es if e['kind'] == 'clip')} clips.", "",
             "Read this top to bottom and you have the beats of the video: what was asked, what came back, where it broke, what fixed it.",
             "Quotes are verbatim. Every beat names the picture or clip that shows it.", ""]
        T = lambda *ts: [e for e in es if any(t in e.get("tags", []) for t in ts)]
        fails, fixes, wins, srcs = T("fail", "bug", "surprise"), T("fix", "rule", "decision"), T("win", "milestone"), [e for e in es if e.get("url")]
        if fails or fixes or wins or srcs:
            L += ["## Turning points", ""]
            for lab, group in (("Went wrong / surprised", fails), ("Fixed / decided / became a rule", fixes), ("Worked", wins), ("Sources", srcs)):
                if group: L += [f"**{lab}:** " + "; ".join(f"#{e['n']:03d} {e.get('caption') or e.get('agent') or e.get('user') or e.get('url')}"[:90] for e in group), ""]
        L += ["## Beats", ""]
        for e in es:
            t = datetime.fromtimestamp(e["time"]).strftime("%H:%M"); head = e.get("caption") or e.get("agent") or e.get("user") or e["kind"]
            L.append(f"### #{e['n']:03d} {t} · {head[:80]}")
            if e.get("user"): L.append(f"> {e['user']}")
            if e.get("agent"): L.append(f"What happened: {e['agent']}")
            if e.get("url"): L.append(f"- source: {e['url']}")
            if e.get("quote"): L.append(f"- quote: \"{e['quote']}\"")
            for f in e.get("files", []): L.append(f"- show: `{Path(f).parent.name}/{Path(f).name}`")
            if e.get("tags"): L.append(f"- tags: {', '.join(e['tags'])}")
            L.append("")
        L += ["## Script skeleton (fill in)", "",
              "1. Hook: what was being attempted, found out, or decided, and why it is not obvious.",
              "2. First attempt: the earliest asset in `assets/`, and the first thing that went wrong or surprised.",
              "3. The loop: each `fail`/`surprise` beat followed by its `fix`/`rule`/`decision` beat, in order. Sources with their quotes are the receipts.",
              "4. Where it ended up: the last clip, side by side with the first.",
              "5. Verdict: the user's own words from the last notes.", "",
              "Build the video with script-to-video: every beat above is one shot, the `show:` line is its picture.", ""]
        out = "\n".join(L); (self.root / "brief.md").write_text(out); return out

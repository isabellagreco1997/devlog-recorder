"""devlog: record a build session as it happens.

  devlog init <name>                                   start (or reopen) devlog/<name> and make it active here
  devlog note --user "..." --agent "..." [--tags fail,fix] [--files a.png b.txt]
  devlog add <file> [--caption "..."] [--tags ...]      copy a produced file in (png/jpg/gif/txt/json/mp4...)
  devlog shot <url|file.html> [--caption] [--w --h --scroll SEL --full]
  devlog clip <url|file.html|file.gif|file.mp4> [--dur 6 --keys "ArrowRight:0-1500"] [--caption]
  devlog screen [--window] [--caption]                  grab the screen (desktop apps, terminals)
  devlog compare <a> <b> [--labels before after] [--caption]
  devlog sheet                                          contact sheet of everything so far
  devlog brief                                          write brief.md: beats, quotes, artifacts, script skeleton
  devlog status
"""
import argparse, sys
from pathlib import Path
from . import media
from .journal import Journal


def main(argv=None):
    p = argparse.ArgumentParser(prog="devlog", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("init"); a.add_argument("name"); a.add_argument("--dir", default="devlog")
    a = sub.add_parser("note"); a.add_argument("--user", default=""); a.add_argument("--agent", default=""); a.add_argument("--caption", default=""); a.add_argument("--tags", default=""); a.add_argument("--files", nargs="*", default=[])
    a = sub.add_parser("add"); a.add_argument("file"); a.add_argument("--caption", default=""); a.add_argument("--tags", default=""); a.add_argument("--user", default=""); a.add_argument("--agent", default="")
    a = sub.add_parser("shot"); a.add_argument("target"); a.add_argument("--caption", default=""); a.add_argument("--tags", default=""); a.add_argument("--w", type=int, default=1280); a.add_argument("--h", type=int, default=720); a.add_argument("--scroll"); a.add_argument("--full", action="store_true"); a.add_argument("--wait", type=float, default=1.0)
    a = sub.add_parser("clip"); a.add_argument("target"); a.add_argument("--caption", default=""); a.add_argument("--tags", default=""); a.add_argument("--dur", type=float, default=6.0); a.add_argument("--w", type=int, default=1280); a.add_argument("--h", type=int, default=720); a.add_argument("--keys", default=""); a.add_argument("--wait", type=float, default=0.8)
    a = sub.add_parser("screen"); a.add_argument("--caption", default=""); a.add_argument("--tags", default=""); a.add_argument("--window", action="store_true")
    a = sub.add_parser("compare"); a.add_argument("a"); a.add_argument("b"); a.add_argument("--labels", nargs=2, default=["before", "after"]); a.add_argument("--caption", default=""); a.add_argument("--tags", default="")
    sub.add_parser("sheet"); sub.add_parser("brief"); sub.add_parser("status")
    args = p.parse_args(argv)
    tags = lambda: [t.strip() for t in args.tags.split(",") if t.strip()] if hasattr(args, "tags") and args.tags else []

    if args.cmd == "init":
        j = Journal.init(args.name, args.dir); print("devlog:", j.root); return
    j = Journal.active()
    if args.cmd == "note":
        e = j.note(args.user, args.agent, args.caption, tags(), args.files); print(f"#{e['n']:03d} noted")
    elif args.cmd == "add":
        e = j.add(args.file, args.caption, tags(), user=args.user, agent=args.agent); print(f"#{e['n']:03d}", e["files"][0])
    elif args.cmd == "shot":
        out = j.next_path("assets", args.caption or Path(args.target).stem, ".png")
        media.shot(args.target, out, args.w, args.h, args.scroll, args.full, args.wait); e = j.record("shot", [out], args.caption, tags()); print(f"#{e['n']:03d}", out)
    elif args.cmd == "clip":
        out = j.next_path("clips", args.caption or Path(args.target).stem, ".mp4")
        media.clip(args.target, out, args.dur, args.w, args.h, args.keys, args.wait); e = j.record("clip", [out], args.caption, tags()); print(f"#{e['n']:03d}", out)
    elif args.cmd == "screen":
        out = j.next_path("assets", args.caption or "screen", ".png"); media.screen(out, args.window); e = j.record("shot", [out], args.caption, tags()); print(f"#{e['n']:03d}", out)
    elif args.cmd == "compare":
        out = j.next_path("assets", args.caption or "compare", ".png"); media.compare(args.a, args.b, out, tuple(args.labels)); e = j.record("compare", [out], args.caption, tags()); print(f"#{e['n']:03d}", out)
    elif args.cmd == "sheet":
        imgs = sorted(str(f) for f in (j.root / "assets").iterdir() if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif"))
        out = j.root / "sheets" / "contact.jpg"; media.sheet(imgs, out); print(out)
    elif args.cmd == "brief":
        print(j.brief()[:600] + "\n..."); print("->", j.root / "brief.md")
    elif args.cmd == "status":
        es = j.entries(); print(j.root, f"{len(es)} entries"); [print(f"  #{e['n']:03d} {e['kind']:8s} {(e.get('caption') or e.get('agent') or e.get('user'))[:70]}") for e in es[-8:]]


if __name__ == "__main__":
    main()

"""Capture: screenshots and short clips of web pages / HTML games via headless Chrome, screen grabs, gif/video to mp4, compares, sheets."""
import json, os, platform, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

ENGINE = Path(__file__).resolve().parent.parent / "engine"


def _node(job: dict):
    p = Path(job["out"]).parent / ".capture_job.json" if "out" in job else Path(job["out_dir"]) / ".capture_job.json"
    p.parent.mkdir(parents=True, exist_ok=True); json.dump(job, open(p, "w"))
    r = subprocess.run(["node", str(ENGINE / "capture.js"), str(p)], cwd=str(ENGINE.parent), capture_output=True, text=True)
    if r.returncode != 0: raise SystemExit("capture failed: " + (r.stderr or r.stdout)[-800:])
    p.unlink(missing_ok=True); return r.stdout


def _url(target: str) -> str:
    return target if target.startswith(("http://", "https://", "file://")) else Path(target).resolve().as_uri()


def shot(target: str, out: Path, w: int = 1280, h: int = 720, scroll: str | None = None, full: bool = False, wait: float = 1.0):
    """Screenshot a URL or a local HTML file."""
    _node(dict(mode="shot", url=_url(target), out=str(out), w=w, h=h, scroll=scroll, full=full, wait=wait)); return out


def clip(target: str, out: Path, dur: float = 6.0, w: int = 1280, h: int = 720, keys: str = "", wait: float = 0.8, fps_out: int = 30):
    """A short clip. target = URL / .html (recorded live in headless Chrome, optional key presses),
    or .gif / .mp4 / .mov / .webm (converted/trimmed with ffmpeg). keys: "ArrowRight:0-1500,Space:400-500" (ms windows)."""
    src = Path(target); tmp = out.parent.parent / "tmp" / (out.stem + "_frames"); tmp.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in (".gif", ".mp4", ".mov", ".webm") and src.exists():
        args = ["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", str(src)] if src.suffix.lower() == ".gif" else ["ffmpeg", "-y", "-v", "error", "-i", str(src)]
        args += ["-t", str(dur), "-vf", f"scale='min({w},iw)':-2:flags=neighbor,pad=ceil(iw/2)*2:ceil(ih/2)*2", "-r", str(fps_out), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out)]
        subprocess.run(args, check=True); return out
    kl = []
    for part in [k for k in keys.split(",") if k.strip()]:
        key, win = part.split(":"); a, b = win.split("-"); kl.append(dict(key=key.strip(), down=int(a), up=int(b)))
    _node(dict(mode="record", url=_url(target), out_dir=str(tmp), w=w, h=h, dur=dur, wait=wait, keys=kl))
    # frames were captured at whatever rate Chrome managed; the timestamps make the clip real-time
    ts = json.load(open(tmp / "times.json")); lines = []
    for i, t in enumerate(ts):
        d = (ts[i + 1] - t) if i + 1 < len(ts) else 1 / fps_out
        lines += [f"file 'f{i:05d}.png'", f"duration {max(d, 0.01):.4f}"]
    lines.append(f"file 'f{len(ts) - 1:05d}.png'"); (tmp / "list.txt").write_text("\n".join(lines))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-fps_mode", "cfr", "-r", str(fps_out),
                    "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-an", str(out)], check=True)
    for f in tmp.iterdir(): f.unlink()
    tmp.rmdir(); return out


def screen(out: Path, window: bool = False):
    """Grab the screen (macOS: screencapture; Linux: gnome-screenshot/scrot; Windows: PowerShell)."""
    s = platform.system()
    if s == "Darwin": subprocess.run(["screencapture", "-x"] + (["-w"] if window else []) + [str(out)], check=True)
    elif s == "Linux":
        for cmd in (["gnome-screenshot", "-f", str(out)], ["scrot", str(out)], ["import", "-window", "root", str(out)]):
            try: subprocess.run(cmd, check=True); break
            except Exception: continue
    else:
        ps = ("Add-Type -AssemblyName System.Windows.Forms,System.Drawing; $b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds; "
              "$bmp=New-Object Drawing.Bitmap $b.Width,$b.Height; $g=[Drawing.Graphics]::FromImage($bmp); $g.CopyFromScreen($b.Location,[Drawing.Point]::Empty,$b.Size); "
              f"$bmp.Save('{out}')")
        subprocess.run(["powershell", "-Command", ps], check=True)
    return out


def compare(a: str, b: str, out: Path, labels=("before", "after"), height: int = 720):
    """Two images side by side, same height, labelled. The single most useful picture in any devlog."""
    ims = [Image.open(p).convert("RGB") for p in (a, b)]
    ims = [im.resize((int(im.width * height / im.height), height), Image.NEAREST if im.width < 400 else Image.LANCZOS) for im in ims]
    gap = 24; W = sum(im.width for im in ims) + gap; sheet = Image.new("RGB", (W, height + 44), (18, 18, 20)); d = ImageDraw.Draw(sheet); x = 0
    for im, lab in zip(ims, labels):
        sheet.paste(im, (x, 44)); d.text((x + 10, 14), lab, fill=(240, 240, 240)); x += im.width + gap
    sheet.save(out); return out


def sheet(paths: list, out: Path, cols: int = 4, width: int = 420):
    """Contact sheet of every image, numbered, so a script writer sees the whole process on one page."""
    ims = []
    for p in paths:
        try: ims.append((Path(p).name, Image.open(p).convert("RGB")))
        except Exception: pass
    if not ims: raise SystemExit("no images to sheet")
    h = int(width * 9 / 16); rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * width, rows * (h + 22)), (18, 18, 20)); d = ImageDraw.Draw(S)
    for i, (name, im) in enumerate(ims):
        im = im.copy(); im.thumbnail((width - 8, h - 8)); x, y = (i % cols) * width, (i // cols) * (h + 22)
        S.paste(im, (x + 4, y + 4)); d.text((x + 6, y + h + 4), name[:52], fill=(220, 220, 220))
    S.save(out, quality=88); return out

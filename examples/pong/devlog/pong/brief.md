# pong: the story so far

9 entries over 0.0 h (2026-09-03 19:18 to 19:19). 5 artifacts, 2 clips.

Read this top to bottom and you have the beats of the video: what was asked, what came back, where it broke, what fixed it.
Quotes are verbatim. Every beat names the picture or clip that shows it.

## Turning points

**Went wrong:** #004 Reproduced it: the hit test only checked the ball centre, so at speed the ball skippe

**Fixed / became a rule:** #004 Reproduced it: the hit test only checked the ball centre, so at speed the ball skippe

**Worked:** #001 Wrote index.html: a 640x360 canvas, two paddles, a ball, both paddles driven by a laz; #003 it plays itself; #009 Stopped here. Sheet and brief written.

## Beats

### #001 19:18 · Wrote index.html: a 640x360 canvas, two paddles, a ball, both paddles driven by 
> make me a pong game in a single html file, nothing fancy
What happened: Wrote index.html: a 640x360 canvas, two paddles, a ball, both paddles driven by a lazy AI so it plays itself. 40 lines.
- tags: milestone

### #002 19:18 · first playable
- show: `assets/002-first-playable.png`

### #003 19:18 · it plays itself
- show: `clips/003-it-plays-itself.mp4`
- tags: win

### #004 19:18 · Reproduced it: the hit test only checked the ball centre, so at speed the ball s
> the ball goes through the paddle sometimes
What happened: Reproduced it: the hit test only checked the ball centre, so at speed the ball skipped the 10 px paddle in one frame. Fixed by widening the test to the paddle's full height and bouncing on the paddle's face.
- tags: fail, fix

### #005 19:18 · after the fix
- show: `assets/005-after-the-fix.png`

### #006 19:18 · before and after the hit test fix
- show: `assets/006-before-and-after-the-hit-test-fix.png`

### #007 19:18 · Yes: ArrowUp/ArrowDown move the left paddle, the AI takes over when no key is he
> can i control the left one with the arrows?
What happened: Yes: ArrowUp/ArrowDown move the left paddle, the AI takes over when no key is held.
- tags: decision

### #008 19:19 · left paddle on the arrow keys
- show: `clips/008-left-paddle-on-the-arrow-keys.mp4`

### #009 19:19 · Stopped here. Sheet and brief written.
> ok that's enough for today
What happened: Stopped here. Sheet and brief written.
- tags: milestone

## Script skeleton (fill in)

1. Hook: what was being attempted and why it is not obvious.
2. First attempt: the earliest asset in `assets/`, and the first thing that went wrong.
3. The loop: each `fail` beat followed by its `fix`/`rule` beat, in order.
4. Where it ended up: the last clip, side by side with the first.
5. Verdict: the user's own words from the last notes.

Build the video with script-to-video: every beat above is one shot, the `show:` line is its picture.

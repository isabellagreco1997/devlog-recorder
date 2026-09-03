#!/bin/sh
# Rebuilds the example devlog from scratch. Run from this folder: sh run_example.sh
set -e
rm -rf devlog .devlog.json
devlog init pong
devlog note --user "make me a pong game in a single html file, nothing fancy" --agent "Wrote index.html: a 640x360 canvas, two paddles, a ball, both paddles driven by a lazy AI so it plays itself. 40 lines." --tags milestone
devlog shot index.html --caption "first playable" --w 640 --h 360
devlog clip index.html --dur 5 --caption "it plays itself" --w 640 --h 360 --tags win
devlog note --user "the ball goes through the paddle sometimes" --agent "Reproduced it: the hit test only checked the ball centre, so at speed the ball skipped the 10 px paddle in one frame. Fixed by widening the test to the paddle's full height and bouncing on the paddle's face." --tags fail,fix
devlog shot index.html --caption "after the fix" --w 640 --h 360
devlog compare devlog/pong/assets/002-first-playable.png devlog/pong/assets/005-after-the-fix.png --caption "before and after the hit test fix" --labels "before" "after"
devlog note --user "can i control the left one with the arrows?" --agent "Yes: ArrowUp/ArrowDown move the left paddle, the AI takes over when no key is held." --tags decision
devlog clip index.html --dur 5 --caption "left paddle on the arrow keys" --w 640 --h 360 --keys "ArrowUp:0-1200,ArrowDown:1400-2600,ArrowUp:2800-4000"
devlog note --user "ok that's enough for today" --agent "Stopped here. Sheet and brief written." --tags milestone
devlog sheet
devlog brief

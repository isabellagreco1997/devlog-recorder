#!/bin/sh
# A research session, not a build: reading, quoting, deciding. Run from this folder: sh run_example.sh
set -e
rm -rf devlog .devlog.json
devlog init why-is-the-sky-blue
devlog note --user "why is the sky blue, and why is the sunset red then? i want the real answer not the kids one" --agent "Two candidate explanations to check: Rayleigh scattering (blue light scatters more) and ozone absorption. Reading the primary pages first." --tags milestone
devlog source "https://en.wikipedia.org/wiki/Rayleigh_scattering" --quote "The strong wavelength dependence of the scattering means that shorter (blue) wavelengths are scattered more strongly than longer (red) wavelengths" --caption "Rayleigh scattering, the mechanism" --scroll "#Cause_of_the_blue_color_of_the_sky"
devlog source "https://en.wikipedia.org/wiki/Diffuse_sky_radiation" --quote "the scattering of sunlight in the atmosphere is strongly wavelength dependent" --caption "why the sky is not violet" --scroll "#Why_the_sky_is_blue"
devlog note --user "wait so why isnt it violet then, violet is shorter" --agent "Three reasons, from the diffuse sky radiation page: the sun emits less violet than blue, the upper atmosphere absorbs some violet, and our eyes are far less sensitive to violet. The sum reads as blue." --tags surprise
devlog source "https://en.wikipedia.org/wiki/Sunset" --quote "the red hues are produced by the scattering of shorter wavelengths out of the line of sight" --caption "sunset: the same effect over a longer path" --scroll "#Colors"
devlog note --user "ok so sunsets are red because the blue already got scattered away before it reaches me" --agent "Yes. At sunset light crosses roughly 40 times more atmosphere than at noon, so most blue is scattered out of the direct beam before it arrives; what is left is orange and red. Ozone adds a little to the blue at twilight but is not the main cause." --tags decision
devlog note --user "good, thats the video" --agent "Stopped. Sheet and brief written." --tags milestone
devlog sheet
devlog brief

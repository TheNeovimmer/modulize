# modulize — 60s promo storyboard (canonical)

`modulize-60s.mp4` — 1280×720, 30 fps, exactly 60.0s, h264 + AAC.

**Regenerate** (from repo root):

```bash
python3 assets/promo/render_scenes.py   # 8 scene PNGs
python3 assets/promo/make_audio.py      # audio.wav
for i in 1 2 3 4 5 6 7 8; do ffmpeg -y -loop 1 -i scenes/0$i-*.png \
  -vf "scale=2560:1440,zoompan=z='1+0.08*on/225':d=225:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st=7.1:d=0.4,format=yuv420p" \
  -t 7.5 -r 30 -c:v libx264 -preset medium -crf 20 clip$i.mp4; done
# concat clip1..clip8 (7.5s each), mux audio.wav → modulize-60s.mp4
```

Or paste the eight shots into Veo 3 / Gemini with the prompts below — same order, same beats.

## Shots (each rendered as one 7.5s scene)

| # | Window | Card |
|---|---|---|
| 1 | 0:00–0:07 | The mess — *"One feature. Five folders by layer."* |
| 2 | 0:07–0:15 | Phase 0 · the safety net — clean tree, suite, checkpoint |
| 3 | 0:15–0:22 | Phase 2 · map — import graph + skeleton |
| 4 | 0:22–0:30 | Phase 3 · list — hidden / needless / surplus / special case |
| 5 | 0:30–0:37 | Phase 4 · redesign — the knot vs. the clean column |
| 6 | 0:37–0:45 | Phase 5 · fix — one registry, suite green |
| 7 | 0:45–0:52 | Phase 6 · verify — the loop, special cases 17 → 2 |
| 8 | 0:52–1:00 | Close — `modulize` · *Say goodbye to messy code.* · install line |

## Veo 3 prompts

**1 — The mess**
```text
Cinematic dark UI explainer video, 16:9. A glowing monolith of code on a dark
slate background. Thousands of lines tumble outward; white file-lines multiply
and knot together like a wire ball. Red labels flicker past: "if (special case)",
"TODO", "workaround", "sleep(100ms)", "duplicated". Camera pushes in slowly
toward the knot.
Audio: low room tone, rumble builds, restless static clicks, musical_stem=0.
```

**2 — Safety net**
```text
Same dark slate background. A clean terminal window fades in. White text types
out line by line: "$ git status — clean", "$ tests passed before change",
"$ git stash — safety net". A soft green checkmark appears beside each line as
it's typed.
Audio: faint keyboard taps, a tiny chime on each checkmark, musical_stem=0.
```

**3 — Map**
```text
Same dark background. A golden wireframe of the code monolith slowly rotates,
then dissolves into a clean skeleton map: thin white lines showing import
arrows between tidy module nodes. Three search rays sweep across the map and
pause on problem points.
Audio: soft data sweep, low pulse, musical_stem=0.
```

**4 — List**
```text
The map zooms into a list panel on the dark background. Problem entries appear
one by one in white monospace type, each with a small left-aligned tag: "HIDDEN
LINK", "NEEDLESS LINK", "SURPLUS", "SPECIAL CASE". The list grows to about
eight rows.
Audio: a short blip each time a row lands; musical_stem=0.
```

**5 — Redesign**
```text
Same dark background. A single bright white line sweeps horizontally across the
screen, left to right. As it passes, every red "special case" label glows for one
frame and dies. The tangled mass collapses into one clean column of deep
modules. Text fades in at the top: "One fix. Behind many problems."
Audio: a soft sweep whoosh as the line passes; clean silence; one warm tone at
the end, musical_stem=0.
```

**6 — Fix**
```text
Same dark background. A compact diff panel slides in from the left. A commit line
types out: "refactor: single registry for every action". A count rolls down from
"5 files touched" to "1 file" and turns green.
Audio: soft pop on each keystroke; a chime each time a change lands;
musical_stem=0.
```

**7 — Loop**
```text
The clean column of modules rotates slowly. Four small sweep beams circle it once
and dim, one after another. A counter reads "special cases: 17" and counts down
to "2".
Audio: four soft ticks as the beams pass; one chime at "2"; musical_stem=0.
```

**8 — Close**
```text
Clean dark slate background. A luminous logo mark forms in the center — lowercase
"modulize" in bold lettering. Three thin white line paths grow out from the mark
and lock into a tidy network, each with a tiny tick. Beneath, the tagline fades
in: "Say goodbye to messy code."
Audio: gentle pad swell resolving into a warm chord, final soft tick, fade.
musical_stem=0.
```

## Brand rules (never break)

- lowercase `modulize`, chalk-white on dark slate — same mark as `assets/modulize.svg`
- tagline exactly: **Say goodbye to messy code.**
- never state a star count or install total that isn't real and current
- the left-to-right white sweep + whoosh is the trademark — keep it identical everywhere it recurs

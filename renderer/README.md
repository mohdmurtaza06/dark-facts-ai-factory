# DARK FACTS cinematic renderer

A first isolated Remotion + Three.js prototype workspace. It does not replace the Python factory and does not upload videos.

## Requirements

- Node.js 20+
- npm
- FFmpeg
- Chromium dependencies required by Remotion on Linux

## Run locally

```bash
cd renderer
npm install
npm run studio
npm run render:pilot
```

The pilot now has a procedural elevator set, animated detective blocking, timed on-screen narration captions and an original 60-second script/shot plan in `content/the-last-elevator.md`. It is still a visual prototype: voice audio, sound design, the independent reflection reveal, true shot transitions and final visual QA are not complete. Treat it as an engine prototype, not a publishable Short.

## Composition

- ID: `DarkMysteryPilot`
- 1080 × 1920
- 30 fps
- 60 seconds

## Next steps

1. Add generated narration audio and word-level timing from the approved script.
2. Animate the reflection reveal independently from the detective.
3. Add real shot transitions, cinematic post-processing and original sound design.
4. Add contact-sheet and frame QA.
5. Run the Remotion typecheck and a complete Linux cloud render benchmark before setting a daily production schedule.

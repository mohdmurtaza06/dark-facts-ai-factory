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

The current pilot is a procedural visual/technical scaffold. It is not yet a finished 55–70 second story: narration, shot-level story beats, detailed character acting, sound design and visual QA still need to be added. Treat it as an engine smoke test, not a publishable Short.

## Composition

- ID: `DarkMysteryPilot`
- 1080 × 1920
- 30 fps
- 60 seconds

## Next steps

1. Replace placeholder environment and character acting with modular story-plan-driven components.
2. Add original narration and word timing.
3. Add cinematic post-processing and sound design.
4. Add contact-sheet and frame QA.
5. Benchmark a Linux cloud render before setting a daily production schedule.

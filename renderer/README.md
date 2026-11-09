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
python -m pip install edge-tts
npm run audio:pilot
npm run studio
npm run render:pilot
```

The pilot now has a procedural elevator set, detective blocking, an independent shadow/reflection reveal, timed captions, original narration text and a local audio-generation script. `npm run audio:pilot` uses Edge TTS for narration and synthesizes a low ambient bed locally; it requires network access for Edge TTS and FFmpeg. Generated audio is intentionally not committed. The composition references those generated files, so run the audio step before rendering. The current audio bed is a placeholder, not a finished sound design.

## Composition

- ID: `DarkMysteryPilot`
- 1080 × 1920
- 30 fps
- 60 seconds

## Next steps

1. Add real shot transitions, cinematic post-processing and original sound design.
2. Add word-level narration timing and sync captions to the generated voice.
3. Add contact-sheet and frame QA.
4. Run the Remotion typecheck and a complete Linux cloud render benchmark before setting a daily production schedule.

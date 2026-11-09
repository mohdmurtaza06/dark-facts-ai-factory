# Cinematic renderer port plan

## Decision
Use the MIT-licensed source project [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts) as the rendering-engine reference and code base for a dedicated Remotion/Three.js renderer. Preserve its MIT copyright and license notice in any copied or adapted files.

This is a renderer integration, not a Claude Code dependency. The production factory will generate original scripts, shot plans, character specifications, narration and audio; Remotion will render the authored scene plan.

## Target format
- Runtime: 55–70 seconds.
- Canvas: 1080 × 1920, 30 fps.
- Visual language: illustrated 2D characters inside stylized 3D environments, cinematic camera moves, lighting, depth of field and restrained ink outlines.
- Genre: dark mystery + comedy.
- Audio: original narration, synthesized/original music and sound effects.
- Output: MP4/H.264 with audio, validated before any publishing.

## Source components to port
Port selectively from the upstream repository's `templates/bridge/`:
- Three.js world construction and environment: `build.ts`, `world.ts`, `paint.ts`, `lights.ts`, `shade.ts`.
- Character drawing and animation: `toon.ts`, `cast.ts`, `cardshade.ts`.
- Camera and timeline: `story.ts`, redesigned around generated shot plans and a 55–70 s timeline.
- Post-processing: `ink.ts`, `lensblur.ts`, `grade.ts`, and the Remotion composition in `Bridge.tsx`.
- Audio helpers may be adapted after the visual renderer is working.

Do not copy upstream reference frames, contact sheets, private study material, the example bridge story, or its characters as production content. Create original characters, worlds, props, scripts and shot designs for DARK FACTS.

## Factory integration contract
1. Content planner emits a validated story package with a 55–70 s narration script, source notes for factual claims, scene list, character IDs, locations, dialogue, action beats, camera intent and audio cues.
2. Voice stage produces narration audio and word-level timing data.
3. Scene compiler maps the package to deterministic Remotion props and procedural scene modules.
4. Remotion renders the vertical composition at 30 fps.
5. Audio stage mixes narration, original score and sound effects; muxes final audio.
6. QA checks duration, resolution, frame rate, codecs, audio presence/loudness, black/white/frozen/pop frames, missing assets and scene coverage.
7. Only a passed and reviewed render may enter the YouTube upload queue.

## Cloud and cost constraints
The upstream project documents a large Remotion public asset bundle and local disk pressure. A cloud runner must be benchmarked for render time, RAM, disk, browser/WebGL availability and artifact size before promising five renders daily. GitHub Actions free allowance is not proof that five 2K renders per day will fit.

The ₹0 policy remains strict:
- No paid API or hosted GPU fallback.
- No billing-enabled generation call.
- No automatic upload while renderer and QA are unverified.
- If a free runner cannot complete a render, stop and report the blocker rather than falling back to the legacy Pillow motion graphics.

## Implementation stages
- [ ] Add a dedicated Remotion/Three.js renderer workspace without replacing the legacy Python factory.
- [ ] Port the minimum upstream engine files and preserve MIT notices.
- [ ] Replace bridge-specific story constants with a generic scene-plan schema.
- [ ] Create one original 55–70 s dark mystery/comedy pilot.
- [ ] Render and inspect stills/contact sheets; correct visual defects.
- [ ] Run a full cloud render benchmark and verify cost/runner limits.
- [ ] Connect the Python factory to the renderer only after the pilot passes.
- [ ] Enable scheduled production only after all production gates pass.

## Upstream source
- Repository: https://github.com/mromidev/claude-animated-shorts
- License: MIT (retain copyright and license notice).
- Upstream README says the reference frames are for style study only. They are not to be uploaded, distributed as our content, or copied into production.

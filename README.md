# DARK FACTS AI FACTORY

A cloud-first YouTube Shorts production system for original dark-mystery + comedy stories.

## Target production format

- **Runtime:** 55–70 seconds per Short.
- **Visual direction:** illustrated 2D characters inside cinematic stylized 3D environments.
- **Rendering target:** 1080 × 1920, 30 fps.
- **Audio:** original narration, music and sound effects.
- **Daily target:** five Shorts, subject to verified free compute capacity and quality gates.
- **Budget policy:** ₹0/month. No paid provider fallback or surprise charges.

## Current state

The existing V1 renderer creates Pillow/FFmpeg motion graphics. It is not the target cinematic renderer. The old daily publishing workflow remains paused.

The `cloud-automation-foundation` branch contains:
- Cloud readiness checks, currently not a production generation workflow.
- Technical MP4 quality gate and tests.
- An opt-in hosted video-provider adapter, not connected to the production pipeline.
- A documented port plan for the MIT-licensed Remotion + Three.js animated renderer from [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts).

## Important ₹0 limitation

Five cinematic 55–70 second renders every day are not yet proven on free cloud compute. The upstream renderer is a substantial Remotion/Three.js project and documents significant temporary disk use. We must benchmark the runner before promising unattended daily output.

**Do not enable unattended publishing yet.** The cinematic renderer port, original pilot, visual QA, cloud render benchmark, persistent deduplication and YouTube OAuth validation remain outstanding. The system must fail closed rather than silently use the legacy motion-graphics renderer.

## Documentation

- [Cloud automation architecture and provider contract](docs/CLOUD_AUTOMATION.md)
- [Production gates](docs/PRODUCTION_GATES.md)
- [Cinematic renderer port plan](docs/CINEMATIC_RENDERER_PORT.md)

## Existing V1 local commands

```bash
pip install -r requirements.txt
python -m factory.run --count 1 --output output --no-upload
```

These commands exercise the legacy Python renderer only. They do not produce the target cinematic animated format.

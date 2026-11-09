# DARK FACTS AI FACTORY

A cloud-first YouTube Shorts automation project.

## Current state

The existing V1 renderer creates Pillow/FFmpeg motion graphics. It does **not** create premium 3D animated scenes. The old daily publishing workflow remains paused.

The `cloud-automation-foundation` branch adds:
- A cloud readiness workflow with a daily schedule that stays dormant until explicitly enabled.
- A fail-closed technical MP4 quality gate and tests.
- Production requirements, publishing safeguards, and a clear provider integration contract.

## Important ₹0 limitation

GitHub Actions and the YouTube Data API can provide free orchestration/upload within their respective limits, but neither provides AI video-generation compute. Free hosted GPU services do not guarantee the capacity required for five premium 3D Shorts every day. This repository therefore does not pretend that the 5/day premium 3D target is already achieved.

**Do not enable unattended publishing yet.** A genuine hosted video-generation backend, credentials/quotas, YouTube OAuth secrets, persistent deduplication, and a successful quality-reviewed sample are still required. The system must fail closed rather than fall back to the legacy motion-graphics renderer.

## Documentation

- [Cloud automation architecture and provider contract](docs/CLOUD_AUTOMATION.md)
- [Production gates](docs/PRODUCTION_GATES.md)

## Existing V1 local commands

```bash
pip install -r requirements.txt
python -m factory.run --count 1 --output output --no-upload
```

The existing renderer is retained for legacy testing only. It is not the requested premium 3D production backend.

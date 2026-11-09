# Production gates

The cloud factory must not upload unless all gates pass.

- [ ] Five unique scripts and source records exist for the run.
- [ ] The selected visual backend is a genuine video-generation service, not a still-image pan/zoom fallback.
- [ ] Each render is 9:16, 1080x1920, H.264/AAC MP4, and 15–20 seconds.
- [ ] Each render contains both audio and video streams.
- [ ] Audio is not silent and peak/loudness levels are within configured bounds.
- [ ] Black/frozen-frame checks pass.
- [ ] No duplicate output hashes or reused scripts in the configured lookback window.
- [ ] Captions match the narration and remain inside mobile safe areas.
- [ ] Rights/provenance for music, sound effects, images, models, and generated footage are recorded.
- [ ] All five videos pass. Default batch policy is all-or-none publishing.
- [ ] YouTube OAuth is valid and privacy status is explicitly configured.
- [ ] Upload results and scheduled publish timestamps are recorded in the run manifest.

A missing provider, exhausted quota, invalid OAuth token, or failed quality check is a hard stop. Never fall back to the legacy motion-graphics renderer and never upload a placeholder.

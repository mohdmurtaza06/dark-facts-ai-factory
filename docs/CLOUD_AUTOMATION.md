# DARK FACTS AI FACTORY: Cloud Automation

## Target
Five original 15–20 second vertical Shorts per day, generated and assembled in cloud infrastructure, with automatic retries, quality checks, durable run records, and YouTube scheduling.

## Non-negotiable constraint
The current repository does **not** contain a premium 3D video-generation backend. Its current renderer is Pillow-based motion graphics. Do not label that output as premium 3D animation and do not publish it as a substitute.

At a ₹0 budget, there is no dependable, documented free hosted GPU/video-generation service that guarantees five production renders every day. Free Colab resources are dynamic, not guaranteed, and Google documents runtime termination for content-generation web UIs. A free quota may be used for experiments, never as a production dependency.

## Proposed cloud design
1. **Scheduler/orchestrator:** GitHub Actions, with a daily schedule and manual dispatch.
2. **Story service:** topic rotation, source URL, hook, narration, scene list, character bible, and metadata. Persist a content ledger to prevent duplicate topics/scripts.
3. **Visual provider adapter:** a separately configured hosted text/image-to-video provider. Must return a completed MP4 or a downloadable result URL. Provider must support idempotency keys and report job status. Never silently fall back to the legacy motion-graphics renderer.
4. **Voice/audio:** TTS with a retry policy, loudness normalization, music/SFX from assets with clear usage rights.
5. **Compositor:** FFmpeg vertical edit, captions, transitions, audio mix, and final MP4.
6. **Quality gate:** reject missing streams, wrong aspect ratio, duration outside target, silent audio, corrupt files, and black/frozen output. Failed items are retried a bounded number of times, then quarantined.
7. **Publisher:** YouTube Data API OAuth refresh token. Upload as private/unlisted during validation; only schedule public publishing after a successful review and explicit configuration.
8. **Observability:** manifest per run, job logs, artifact retention, failure summary, and a notification hook.

## Required configuration before unattended publishing
- `CLOUD_FACTORY_ENABLED=true` repository variable.
- A real hosted video-generation provider and its credentials, if required by that provider.
- TTS provider credentials only if the selected TTS service requires them.
- `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` repository secrets.
- `YT_PRIVACY_STATUS=private` or `unlisted` until channel ownership and output quality are verified.
- A persistent ledger (GitHub Actions cache is best-effort only; use a repository artifact or external durable store for reliable cross-run deduplication).

## Why the daily workflow is gated
The schedule is present but the production job is opt-in. This prevents the old motion-graphics renderer from being mistaken for the requested 3D output and prevents failed or placeholder videos from being uploaded. The readiness workflow can be run manually without credentials or publishing.

## Quality policy
A failed quality gate means **do not upload**. Retry transient provider/render errors at most twice with backoff. Do not retry permanent policy/authentication/credit errors indefinitely. If fewer than five videos pass, publish none by default and retain the successful files as artifacts for inspection.

## Cost reality
GitHub Actions is free for public repositories on standard GitHub-hosted runners, subject to platform limits. YouTube Data API uploads have a default daily upload quota, but the API itself does not supply video-generation compute. Hosted AI video generation is the missing cost/availability dependency. Therefore five premium 3D Shorts/day at ₹0 cannot currently be guaranteed.

## Hosted provider adapter (implemented, not activated)
The opt-in adapter lives in `factory/video_provider.py` and uses the Hugging Face `InferenceClient.text_to_video` interface. It writes one generated scene clip after validating that the response looks like MP4 data. The adapter is intentionally separate from the legacy renderer and is not called by the daily workflow.

Configuration for a deliberate provider experiment:
- `HF_TOKEN`: Hugging Face fine-grained token with Inference Providers permission.
- `VIDEO_MODEL`: exact text-to-video model ID supported by the selected provider.
- `VIDEO_PROVIDER`: provider name, defaulting to `fal-ai`.

**Billing warning:** Hugging Face Inference Providers routes requests to partner services and is pay-as-you-go. The adapter has no provider-side spend cap. Do not add a token or invoke generation under the ₹0 policy unless the account's available free credit and billing controls have been checked first. The Hugging Face docs currently show text-to-video support and the `InferenceClient.text_to_video` method, but that does not mean the requested five daily outputs are free or guaranteed.

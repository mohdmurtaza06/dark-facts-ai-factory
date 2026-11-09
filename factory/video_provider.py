"""Opt-in hosted text-to-video adapter.

This module is deliberately not called by the legacy renderer. A caller must
explicitly configure a provider and invoke generate_scene_clip().
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any


class VideoProviderConfigurationError(RuntimeError):
    """Raised when a hosted video provider is not explicitly configured."""


class VideoProviderError(RuntimeError):
    """Raised when a hosted provider fails or returns invalid video data."""


def generate_scene_clip(
    prompt: str,
    output_path: str | Path,
    *,
    client: Any | None = None,
    model: str | None = None,
    provider: str | None = None,
    token: str | None = None,
    seed: int | None = None,
) -> Path:
    """Generate one scene clip using Hugging Face Inference Providers.

    No network request is made unless this function is explicitly called.
    Provider usage may incur charges; this adapter does not claim a free quota
    or enforce a provider-side spending cap.
    """
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("prompt must not be empty")

    model = model or os.getenv("VIDEO_MODEL")
    provider = provider or os.getenv("VIDEO_PROVIDER", "fal-ai")
    token = token or os.getenv("HF_TOKEN")
    if not model or not token:
        raise VideoProviderConfigurationError(
            "Set VIDEO_MODEL and HF_TOKEN before requesting hosted generation."
        )

    if client is None:
        try:
            from huggingface_hub import InferenceClient
        except ImportError as exc:
            raise VideoProviderConfigurationError(
                "Install huggingface_hub to use the hosted video adapter."
            ) from exc
        client = InferenceClient(provider=provider, api_key=token)

    try:
        video_bytes = client.text_to_video(prompt, model=model, seed=seed)
    except Exception as exc:
        raise VideoProviderError(f"Hosted video generation failed: {exc}") from exc

    if not isinstance(video_bytes, (bytes, bytearray)) or len(video_bytes) < 1024:
        raise VideoProviderError("Provider returned an empty or implausibly small video.")

    # MP4 files commonly begin with an ISO BMFF ftyp box. Fail closed rather
    # than saving an HTML error page or an unexpected response as an MP4.
    if b"ftyp" not in video_bytes[:32]:
        raise VideoProviderError("Provider response is not recognisable MP4 data.")

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(video_bytes)
    return destination

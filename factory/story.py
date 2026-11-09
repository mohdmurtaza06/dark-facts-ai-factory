"""Cinematic storyboard for DARK FACTS V2."""
from __future__ import annotations
import copy, re

OCTOPUS_CHAR = {
    "id": "octo", "name": "Octo",
    "body_color": (0.55, 0.25, 0.70),
    "accent_color": (0.85, 0.40, 0.75),
    "eye_white": (0.98, 0.98, 1.0),
    "pupil_color": (0.05, 0.05, 0.1),
    "tentacle_count": 8,
}

OCTOPUS_STORY = {
    "title_hook": "Why does an octopus have THREE hearts?",
    "character": OCTOPUS_CHAR,
    "environment_theme": "deep_ocean",
    "scenes": [
        {
            "id": "mystery", "duration": 3.0,
            "narration": "Deep below the waves… something is watching.",
            "action": "diver_discovers",
            "camera": {"type": "dolly_in", "start": (0, -5, 1.5), "end": (0, -3, 1.3), "lens": 32},
            "objects": ["diver", "dark_silhouette"],
            "vfx": ["god_rays", "plankton"],
        },
        {
            "id": "reveal", "duration": 3.0,
            "narration": "An octopus. Eight arms. And a secret inside.",
            "action": "octopus_approaches",
            "camera": {"type": "push_in", "start": (0, -3.5, 1.2), "end": (0, -2.0, 1.1), "lens": 40},
            "objects": ["octopus_full"],
            "vfx": ["bubbles", "caustics"],
        },
        {
            "id": "swim", "duration": 4.0,
            "narration": "It glides through the reef… soft, silent, unstoppable.",
            "action": "octopus_swims",
            "camera": {"type": "side_track", "start": (-2.5, -2.0, 1.2), "end": (2.0, -2.0, 1.2), "lens": 35},
            "objects": ["octopus_full", "coral", "fish"],
            "vfx": ["bubbles", "caustics"],
        },
        {
            "id": "hearts_reveal", "duration": 4.0,
            "narration": "Look closer. One heart. Two hearts… THREE beating hearts!",
            "action": "anatomical_reveal",
            "camera": {"type": "dramatic_low", "pos": (0, -2.2, 0.5), "target": (0, 0, 1.0), "lens": 28},
            "objects": ["octopus_xray", "heart_1", "heart_2", "heart_3"],
            "vfx": ["heart_pulse", "rim_light"],
        },
        {
            "id": "explain", "duration": 3.0,
            "narration": "Two hearts pump blood to the gills. The third powers the body. When it swims, that main heart stops.",
            "action": "hearts_function",
            "camera": {"type": "orbit", "center": (0, 0, 1.0), "radius": 3.0, "lens": 40},
            "objects": ["octopus_xray", "heart_1", "heart_2", "heart_3"],
            "vfx": ["blood_flow"],
        },
        {
            "id": "hero", "duration": 3.0,
            "narration": "Three hearts. One legend. Nature is stranger than fiction.",
            "action": "hero_pose",
            "camera": {"type": "hero_orbit", "center": (0, 0, 1.0), "radius": 3.8, "lens": 35},
            "objects": ["octopus_full"],
            "vfx": ["volumetric_rays", "sparkles"],
        },
    ],
}

def build_storyboard(fact: dict) -> dict:
    t = copy.deepcopy(OCTOPUS_STORY)
    if fact.get("id") != "octopus-hearts":
        t["title_hook"] = fact.get("hook", t["title_hook"])
    total = sum(s["duration"] for s in t["scenes"])
    if abs(total - 20.0) > 0.5:
        scale = 20.0 / total
        for s in t["scenes"]:
            s["duration"] = round(s["duration"] * scale, 2)
    script = re.sub(r"\s+", " ", " ".join(s["narration"] for s in t["scenes"])).strip()
    return {
        "fact_id": fact["id"],
        "topic": fact.get("topic", ""),
        "hook": fact.get("hook", ""),
        "source": fact.get("source", ""),
        "short_fact": fact.get("short_fact", ""),
        "character": t["character"],
        "environment_theme": t["environment_theme"],
        "scenes": t["scenes"],
        "total_duration": sum(s["duration"] for s in t["scenes"]),
        "script": script,
        "title": "Why Does an Octopus Have THREE Hearts? 😳",
        "description": (
            f"{fact.get('short_fact', '')}\n\n"
            f"Source: {fact.get('source', '')}\n"
            "Follow DARK FACTS for more mind-blowing science."
        ),
        "hashtags": "#Shorts #DarkFacts #Octopus #ScienceFacts #MindBlowingFacts #3DAnimation",
    }

def storyboard_summary(sb: dict) -> str:
    lines = [f"Storyboard: {sb['fact_id']} ({sb['total_duration']:.1f}s) — {len(sb['scenes'])} scenes"]
    t = 0.0
    for i, s in enumerate(sb["scenes"], 1):
        lines.append(f"  {i}. [{t:4.1f}-{t+s['duration']:4.1f}s] {s['id']}: {s['action']}")
        t += s["duration"]
    return "\n".join(lines)

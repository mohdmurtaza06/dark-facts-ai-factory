"""Topic-aware six-scene storyboards for DARK FACTS.

The renderer consumes only generic scene primitives and a visual profile. No
single animal/topic is hard-coded into the narrative pipeline.
"""
from __future__ import annotations
import re

TOPIC_PROFILES = {
    "space": {"theme": "space", "palette": [(0.10,0.18,0.48),(0.38,0.18,0.62)], "subject": "planet"},
    "animals": {"theme": "nature", "palette": [(0.12,0.42,0.28),(0.72,0.42,0.16)], "subject": "creature"},
    "ocean": {"theme": "ocean", "palette": [(0.02,0.28,0.48),(0.10,0.62,0.66)], "subject": "creature"},
    "weather": {"theme": "storm", "palette": [(0.16,0.20,0.30),(0.44,0.48,0.62)], "subject": "energy"},
    "evolution": {"theme": "ancient", "palette": [(0.28,0.22,0.12),(0.56,0.38,0.18)], "subject": "fossil"},
    "extreme life": {"theme": "microscope", "palette": [(0.08,0.34,0.30),(0.22,0.62,0.48)], "subject": "microbe"},
}
DEFAULT_PROFILE = {"theme": "abstract", "palette": [(0.12,0.16,0.28),(0.38,0.22,0.52)], "subject": "object"}

def _profile(topic: str) -> dict:
    key = (topic or "").strip().lower()
    for label, profile in TOPIC_PROFILES.items():
        if label in key:
            return profile
    return DEFAULT_PROFILE

def build_storyboard(fact: dict) -> dict:
    title = (fact.get("hook") or fact.get("title") or "The world is stranger than you think.").strip()
    core = (fact.get("short_fact") or fact.get("fact") or "").strip()
    detail = (fact.get("fact") or core).strip()
    source = (fact.get("source") or "").strip()
    topic = (fact.get("topic") or "Curious science").strip()
    profile = _profile(topic)
    sentences = re.split(r"(?<=[.!?])\\s+", detail)
    detail_a = sentences[0] if sentences else core
    detail_b = sentences[1] if len(sentences) > 1 else "The explanation is stranger than the headline."
    narrations = [
        title,
        f"Here's the surprising part: {core}",
        detail_a,
        detail_b,
        f"And that's why this {topic.lower()} fact is so unexpected.",
        "Follow for more facts that sound impossible, but are real.",
    ]
    durations = [2.8, 3.4, 3.8, 3.8, 3.2, 3.0]
    actions = ["hook", "reveal", "zoom", "mechanism", "twist", "hero"]
    scenes = []
    for i, (sid, duration, narration, action) in enumerate(zip(
        ["hook","reveal","scale","explain","twist","hero"], durations, narrations, actions
    )):
        scenes.append({
            "id": sid, "duration": duration, "narration": narration,
            "action": action, "visual_profile": profile,
            "camera": {"type": "push_in" if i in (0,2,3) else "orbit",
                       "radius": 3.2 + i*0.12, "lens": 38},
            "objects": [profile["subject"], "data_orbit", "particles"],
            "on_screen_text": [title[:58], core[:86], topic.upper()][0 if i == 0 else (1 if i in (1,2,3) else 2)],
        })
    script = re.sub(r"\\s+", " ", " ".join(narrations)).strip()
    return {
        "fact_id": fact.get("id", "unknown"), "topic": topic, "hook": title,
        "source": source, "short_fact": core, "visual_profile": profile,
        "scenes": scenes, "total_duration": sum(durations), "script": script,
        "title": title[:95], "description": f"{core}\\n\\nSource: {source}\\n\\nFollow DARK FACTS for more.",
        "hashtags": "#Shorts #DarkFacts #Science #AmazingFacts",
    }

def storyboard_summary(sb: dict) -> str:
    lines = [f"Storyboard: {sb['fact_id']} | {sb['topic']} | {sb['total_duration']:.1f}s | {len(sb['scenes'])} scenes"]
    t = 0.0
    for i, scene in enumerate(sb["scenes"], 1):
        lines.append(f"  {i}. [{t:4.1f}-{t+scene['duration']:4.1f}s] {scene['id']}: {scene['action']}")
        t += scene["duration"]
    return "\\n".join(lines)

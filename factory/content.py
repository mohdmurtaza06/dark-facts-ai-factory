import json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTS = ROOT / "data" / "facts.json"
USED = ROOT / "data" / "used_facts.json"

def load_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def choose_facts(count=5):
    facts = load_json(FACTS, [])
    used = set(load_json(USED, []))
    pool = [f for f in facts if f["id"] not in used]
    if len(pool) < count:
        used.clear()
        pool = facts[:]
    if len(pool) < count:
        raise RuntimeError(f"Need at least {count} reviewed fact entries; found {len(pool)}.")
    random.shuffle(pool)
    selected = pool[:count]
    used.update(f["id"] for f in selected)
    USED.write_text(json.dumps(sorted(used), indent=2), encoding="utf-8")
    return selected

def build_package(fact):
    script = re.sub(r"\\s+", " ", f"{fact['hook']} {fact['fact']} The natural world is stranger than fiction.").strip()
    title = fact["hook"].rstrip(".!?") + " 😳"
    description = f"{fact['short_fact']}\\n\\nSource: {fact['source']}\\nFollow DARK FACTS for more science, nature and space mysteries."
    hashtags = "#Shorts #DarkFacts #MindBlowingFacts #ScienceFacts #DidYouKnow"
    return {"fact_id":fact["id"],"topic":fact["topic"],"title":title,
            "description":description,"hashtags":hashtags,"script":script,
            "source":fact["source"],"short_fact":fact["short_fact"]}

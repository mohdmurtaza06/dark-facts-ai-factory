import asyncio
from pathlib import Path
import edge_tts

async def _save(text, output_path):
    communicate = edge_tts.Communicate(text, "en-US-AndrewNeural", rate="+8%", volume="+0%")
    await communicate.save(str(output_path))

def generate_voice(text, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_save(text, output_path))

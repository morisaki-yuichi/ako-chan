#!/usr/bin/env python3
"""Generate audio for Ako-chan using en-GB Ryan (fixed voice).

Usage:
  python generate_audio.py s1            # Season 1, January
  python generate_audio.py s1 all        # Season 1, all months
  python generate_audio.py s1 01 02 03   # Season 1, specific months
  python generate_audio.py s2 all        # Season 2, all months
  python generate_audio.py s3 all        # Season 3, all episodes
  python generate_audio.py s3 1 2 3      # Season 3, specific parts

Outputs to: audio/{s1|s2|s3}/{date}.mp3   (S1/S2)
            audio/s3/ep-NNN.mp3           (S3)
"""

import asyncio
import re
import sys
from pathlib import Path

import edge_tts

SCRIPTS_DIR = Path(__file__).parent
ROOT = SCRIPTS_DIR.parent

VOICE = "en-GB-RyanNeural"
RATE  = "-10%"
PITCH = "-2Hz"

_TTS_REPLACEMENTS = [
    ("Ako-chan", "Ahko-chan"),
    ("Suke-san", "Sookay-san"),
    ("Pen-san",  "Pen-san"),
]


def preprocess(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    for src, dst in _TTS_REPLACEMENTS:
        text = text.replace(src, dst)
    return text


def build_narration(s: dict) -> str:
    if "ep" in s:
        header = f"Episode {s['ep']}. {s['title']}.\n\n"
    else:
        from datetime import datetime
        dt = datetime.strptime(s["date"], "%m-%d")
        header = f"{dt.strftime('%B')} {dt.day}. {s['title']}.\n\n"
    return header + s["text"]


async def generate_story(s: dict, out_dir: Path, retries: int = 3) -> None:
    slug = f"ep-{s['ep']:03d}" if "ep" in s else s["date"]
    out = out_dir / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 0:
        print(f"  {slug}  skip (exists)")
        return
    for attempt in range(1, retries + 1):
        try:
            communicate = edge_tts.Communicate(
                preprocess(build_narration(s)), VOICE, rate=RATE, pitch=PITCH
            )
            await communicate.save(str(out))
            size = out.stat().st_size // 1024
            print(f"  {slug}  {size} KB")
            return
        except Exception as e:
            if attempt < retries:
                print(f"  {slug}  retry {attempt}/{retries - 1} ({e})")
                await asyncio.sleep(5 * attempt)
            else:
                print(f"  {slug}  FAILED after {retries} attempts: {e}")


async def generate_month(prefix: str, stories, out_dir: Path) -> None:
    month_stories = [s for s in stories if s["date"].startswith(prefix)]
    print(f"\n{prefix}: {len(month_stories)} stories")
    for s in month_stories:
        await generate_story(s, out_dir)


async def generate_part(part_num: int, stories, out_dir: Path) -> None:
    part_stories = [s for s in stories if s.get("part") == part_num]
    print(f"\nPart {part_num}: {len(part_stories)} episodes")
    for s in part_stories:
        await generate_story(s, out_dir)


DATA_MODULES = {
    "s1": ("stories_data_s1", "STORIES_S1"),
    "s2": ("stories_data_s2", "STORIES_S2"),
    "s3": ("stories_data_s3", "STORIES_S3"),
}


async def main() -> None:
    sys.path.insert(0, str(SCRIPTS_DIR))
    import importlib

    args = sys.argv[1:]
    if not args or args[0] not in DATA_MODULES:
        print("Usage: python generate_audio.py <s1|s2|s3> [all | 01 02 ...]")
        sys.exit(1)

    season_key = args[0]
    month_args = args[1:] if len(args) > 1 else ["01"]

    mod_name, var_name = DATA_MODULES[season_key]
    mod = importlib.import_module(mod_name)
    stories = getattr(mod, var_name)

    out_dir = ROOT / "audio" / season_key
    out_dir.mkdir(parents=True, exist_ok=True)

    ep_based = bool(stories) and "ep" in stories[0]

    if ep_based:
        print(f"Voice: {VOICE}  Season: {season_key}  (ep format)")
        if month_args == ["all"]:
            print(f"\nAll episodes: {len(stories)} stories")
            for s in stories:
                await generate_story(s, out_dir)
        else:
            for p in month_args:
                await generate_part(int(p), stories, out_dir)
    else:
        if month_args == ["all"]:
            months = [f"{m:02d}" for m in range(1, 13)]
        else:
            months = month_args
        print(f"Voice: {VOICE}  Season: {season_key}  Months: {', '.join(months)}")
        for m in months:
            await generate_month(m, stories, out_dir)

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())

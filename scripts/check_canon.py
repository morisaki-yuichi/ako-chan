#!/usr/bin/env python3
"""Canon consistency helper.

Commands:
  character <name>         All stories where <name> appears (across all seasons)
  find <keyword>           All stories containing keyword, with snippet
  facts [s1|s2|s3]        List all written story dates and titles

Examples:
  python check_canon.py character Ako-chan
  python check_canon.py find "serial number"
  python check_canon.py facts s1
  python check_canon.py facts
"""

import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

_SEASON_MODULES = {
    "s1": ("stories_data_s1", "STORIES_S1"),
    "s2": ("stories_data_s2", "STORIES_S2"),
    "s3": ("stories_data_s3", "STORIES_S3"),
}


def load_stories(season_filter=None):
    keys = [season_filter] if season_filter else list(_SEASON_MODULES.keys())
    all_stories = []
    for key in keys:
        mod_name, var_name = _SEASON_MODULES[key]
        try:
            mod = importlib.import_module(mod_name)
            stories = getattr(mod, var_name)
            for s in stories:
                all_stories.append({**s, "_season": key})
        except Exception as e:
            print(f"  Warning: could not load {mod_name}: {e}")
    return all_stories


def cmd_character(name: str, season=None) -> None:
    stories = load_stories(season)
    found = [(s["_season"], s["date"], s["title"]) for s in stories
             if name.lower() in s["text"].lower() or name.lower() in s["title"].lower()]
    label = f" in {season}" if season else ""
    print(f"\n'{name}' appears in {len(found)} {'story' if len(found) == 1 else 'stories'}{label}:\n")
    for season_key, date, title in found:
        print(f"  [{season_key}] {date}  {title}")


def cmd_find(keyword: str, season=None) -> None:
    stories = load_stories(season)
    found = []
    for s in stories:
        idx = s["text"].lower().find(keyword.lower())
        if idx >= 0:
            snippet = s["text"][max(0, idx - 40):idx + 80].replace("\n", " ")
            found.append((s["_season"], s["date"], s["title"], snippet))
    label = f" in {season}" if season else ""
    print(f"\n'{keyword}' found in {len(found)} {'story' if len(found) == 1 else 'stories'}{label}:\n")
    for season_key, date, title, snippet in found:
        print(f"  [{season_key}] {date}  {title}")
        print(f"    ...{snippet}...\n")


def cmd_facts(season=None) -> None:
    stories = load_stories(season)
    label = f" ({season})" if season else " (all seasons)"
    print(f"\n{len(stories)} stories written{label}:\n")
    for s in stories:
        print(f"  [{s['_season']}] {s['date']}  {s['title']}")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        cmd_facts()
        return
    cmd = args[0]
    season = args[-1] if args and args[-1] in _SEASON_MODULES else None
    rest = [a for a in args[1:] if a not in _SEASON_MODULES]
    if cmd == "facts":
        cmd_facts(season)
    elif cmd == "character" and rest:
        cmd_character(" ".join(rest), season)
    elif cmd == "find" and rest:
        cmd_find(" ".join(rest), season)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()

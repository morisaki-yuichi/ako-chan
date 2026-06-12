# Part Reference

All seasons, all parts. Use this to locate the target file and episode range before writing.

**Status**: ⬜ written · ⬜ not yet written

---

## Season 1 — Ako-chan and the Robot Dog

| Part | Name | Episodes | Count | File | Status |
|---|---|---|---|---|---|
| 1 | England | ep 1–10 | 10 | `stories_s1_p01.py` | ✅ |
| 2 | Through Europe | ep 11–22 | 12 | `stories_s1_p02.py` | ✅ |
| 3 | Mediterranean | ep 23–41 | 19 | `stories_s1_p03.py` | ✅ |
| 4 | Japan | ep 42–49 | 8 | `stories_s1_p04.py` | ✅ |
| 5 | The North | ep 50–63 | 14 | `stories_s1_p05.py` | ✅ |
| 6 | South America | ep 64–78 | 15 | `stories_s1_p06.py` | ✅ |
| 7 | Toward the Ice | ep 79–89 | 11 | `stories_s1_p07.py` | ✅ |
| 8 | The Southern Signal | ep 90–101 | 12 | `stories_s1_p08.py` | ✅ |
| 9 | Obia's Confession | ep 102–114 | 13 | `stories_s1_p09.py` | ✅ |
| 10 | We Are Home | ep 115–120 | 6 | `stories_s1_p10.py` | ⬜ |

**Total: 120 episodes · 10 parts · Season complete**

### S1 Key files
- Arc: `planning/arc.md` → "Season 1" section
- Outlines: `scripts/story_outlines_s1.py`
- Canon: `canon/characters.md`, `canon/world.md`, `canon/timeline.md`

---

## Season 2 — Ako-chan and the Hidden Door

| Part | Name | Episodes | Count | File | Status |
|---|---|---|---|---|---|
| 1 | The Signal | ep 1–10 | 10 | `stories_s2_p01.py` | ⬜ |
| 2 | Gathering | ep 11–23 | 13 | `stories_s2_p02.py` | ⬜ |
| 3 | Into the Ice | ep 24–35 | 12 | `stories_s2_p03.py` | ⬜ |
| 4 | The First Challenges | ep 36–48 | 13 | `stories_s2_p04.py` | ⬜ |
| 5 | The Garden | ep 49–61 | 13 | `stories_s2_p05.py` | ⬜ |
| 6 | Governance | ep 62–72 | 11 | `stories_s2_p06.py` | ⬜ |
| 7 | Something Alive | ep 73–87 | 15 | `stories_s2_p07.py` | ⬜ |
| 8 | The Truth | ep 88–100 | 13 | `stories_s2_p08.py` | ⬜ |
| 9 | Through the Door | ep 101–108 | 8 | `stories_s2_p09.py` | ⬜ |

**Total: 108 episodes · 9 parts · Season complete**

### S2 Key files
- Arc: `planning/arc.md` → "Season 2" section
- Outlines: `scripts/story_outlines_s2.py`
- Canon: `canon_s2/characters.md`, `canon_s2/world.md`, `canon_s2/timeline.md`

---

## Season 3 — Ako-chan and the Boy with No Name

| Part | Name | Episodes | Count | File | Status |
|---|---|---|---|---|---|
| 1 | Tokyo | ep 1–7 | 7 | `stories_s3_p01.py` | ⬜ |
| 2 | Yokohama: First Meeting | ep 8–14 | 7 | `stories_s3_p02.py` | ⬜ |
| 3 | Tokyo: Second Meeting | ep 15–19 | 5 | `stories_s3_p03.py` | ⬜ |
| 4 | Yokohama: Pattern Classified | ep 20–24 | 5 | `stories_s3_p04.py` | ⬜ |
| 5 | Hokkaido | ep 25–34 | 10 | `stories_s3_p05.py` | ⬜ |
| 6 | Yokohama: Full Records | ep 35–39 | 5 | `stories_s3_p06.py` | ⬜ |
| 7 | Mediterranean | ep 40–49 | 10 | `stories_s3_p07.py` | ⬜ |
| 8 | Yokohama: The Protocol | ep 50–55 | 6 | `stories_s3_p08.py` | ⬜ |
| 9 | The Far South | ep 56–73 | 18 | `stories_s3_p09.py` | ⬜ |
| 10 | Yokohama: The Project | ep 74–87 | 14 | `stories_s3_p10.py` | ⬜ |
| 11 | Yokohama: Departure | ep 88–99 | 12 | `stories_s3_p11.py` | ⬜ |

**Total: 99 episodes · 11 parts · Season complete**

### S3 Key files
- Arc: `planning/arc.md` → "Season 3" section
- Outlines: `scripts/story_outlines_s3.py`
- Canon: `canon_s3/characters.md`, `canon_s3/world.md`, `canon_s3/timeline.md`
- S3 narrative rules: see `CLAUDE.md` → "S3 Narrative Notes"

---

## Adding a new part

If a part needs to be split or a new part added:

1. Create the new file (e.g. `stories_s1_p11.py`) with the correct variable name
2. Add it to `stories_data_s{N}.py`
3. Add the part entry to the `"parts"` list in `generate_stories.py`
4. Add a gradient entry in `"gradients"` for the new part number
5. Update the `"subtitle"` count in `generate_stories.py`
6. Update this file (`planning/parts.md`)

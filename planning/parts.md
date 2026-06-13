# Part Reference

All seasons, all parts. Use this to locate the target file and episode range before writing.

**Status**: ⬜ written · ⬜ not yet written

---

## Season 1 — Ako-chan and the Robot Dog

**※ 全話新規執筆版（再構築）。旧120話は破棄。**

| Part | Name | Episodes | Count | File | Status |
|---|---|---|---|---|---|
| 1 | England | ep 1–8 | 8 | `stories_s1_p01.py` | ⬜ |
| 2 | Through Europe | ep 9–18 | 10 | `stories_s1_p02.py` | ⬜ |
| 3 | New Friends | ep 19–28 | 10 | `stories_s1_p03.py` | ⬜ |
| 4 | Japan | ep 29–37 | 9 | `stories_s1_p04.py` | ⬜ |
| 5 | The Pacific | ep 38–48 | 11 | `stories_s1_p05.py` | ⬜ |
| 6 | South America | ep 49–57 | 9 | `stories_s1_p06.py` | ⬜ |
| 7 | Toward the Ice | ep 58–65 | 8 | `stories_s1_p07.py` | ⬜ |
| 8 | The White Land | ep 66–75 | 10 | `stories_s1_p08.py` | ✅ |
| 9 | The Truth | ep 76–85 | 10 | `stories_s1_p09.py` | ⬜ |
| 10 | Going Home | ep 86–95 | 10 | `stories_s1_p10.py` | ⬜ |

**Total: 95 episodes · 10 parts · 執筆中**

### S1 Key files
- Arc & キャラクター: `planning/s1_arc.md`
- エピソードアウトライン: `planning/s1_outline_new.md`
- 場所・環境詳細: `canon/world.md`

---

## Season 2 — Ako-chan and the Hidden Door

| Part | Name | Episodes | Count | File | Status |
|---|---|---|---|---|---|
| 1 | The Signal | ep 1–10 | 10 | `stories_s2_p01.py` | ⬜ |
| 2 | Gathering | ep 11–23 | 13 | `stories_s2_p02.py` | ⬜ |
| 3 | Into the Ice | ep 24–35 | 12 | `stories_s2_p03.py` | ✅ |
| 4 | The First Challenges | ep 36–48 | 13 | `stories_s2_p04.py` | ✅ |
| 5 | The Garden | ep 49–61 | 13 | `stories_s2_p05.py` | ⬜ |
| 6 | Governance | ep 62–72 | 11 | `stories_s2_p06.py` | ✅ |
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
| 1 | No Gaps | ep 1–7 | 7 | `stories_s3_p01.py` | ✅ |
| 2 | First Meeting | ep 8–14 | 7 | `stories_s3_p02.py` | ✅ |
| 3 | Second Meeting | ep 15–19 | 5 | `stories_s3_p03.py` | ⬜ |
| 4 | Pattern Classified | ep 20–24 | 5 | `stories_s3_p04.py` | ⬜ |
| 5 | Behavior Data Only | ep 25–34 | 10 | `stories_s3_p05.py` | ✅ |
| 6 | Full Records | ep 35–39 | 5 | `stories_s3_p06.py` | ✅ |
| 7 | Unrecordable | ep 40–49 | 10 | `stories_s3_p07.py` | ⬜ |
| 8 | The Protocol | ep 50–55 | 6 | `stories_s3_p08.py` | ⬜ |
| 9 | The Far South | ep 56–73 | 18 | `stories_s3_p09.py` | ✅ |
| 10 | The Project | ep 74–87 | 14 | `stories_s3_p10.py` | ✅ |
| 11 | Departure | ep 88–99 | 12 | `stories_s3_p11.py` | ✅ |

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

# Ako-chan

Three-season bedtime story series.
Published on GitHub Pages.

## Titles

- **Main**: Ako-chan
- **Season 1**: Ako-chan and the Robot Dog
- **Season 2**: Ako-chan and the Hidden Door
- **Season 3**: Ako-chan and the Boy with No Name

## Story Writing Standard: CEFR A1

All stories are written at **CEFR A1** level:
- Vocabulary drawn from the ~600 most common English words
- Simple sentence structure: Subject + Verb + Object
- Sentences of 8–12 words on average; occasional longer sentences are fine
- Target length: **~200 words** — this is a guide, not a strict limit
- Prioritise natural storytelling over word count
- If a story comes out under 150 words and feels complete, ask the user before adding more

**Do not use:**
- Subjunctive ("if I were", "should he ever")
- Passive voice (use sparingly if needed)
- Complex relative clauses
- Multi-clause sentences chained with "which", "whose", etc.
- Vocabulary beyond A1/A2 without strong narrative need

**Good A1 pattern:**
> Ako-chan opened the door. A small dog stood outside. It had big brown eyes.
> "Hello," said Ako-chan. "Are you lost?" The dog wagged its tail.

## S3 Narrative Notes

- Protagonist: "the boy" (no name until Ep 99 / Dec 17, when Ako-chan names him "Yu-chan")
- Faces appear as fog to the boy — he records everything in numbers
- Ako-chan understands this by Part 4 and quietly accepts it
- Notebook entries appear 0–1 times per story, only at failure/gap moments
- Animal recognition is perfect; faces are fog

## Directory Structure

```
├── index.html                 # Landing page (generated)
├── season1/                   # Season 1 HTML (generated)
│   ├── index.html
│   └── ep-NNN.html
├── season2/                   # Season 2 HTML (generated)
├── season3/                   # Season 3 HTML (generated)
├── audio/
│   ├── s1/                    # Season 1 MP3s (Ryan voice)
│   ├── s2/                    # Season 2 MP3s
│   └── s3/                    # Season 3 MP3s
├── canon/                     # Season 1 ground truth
│   ├── characters.md
│   ├── world.md
│   └── timeline.md
├── canon_s2/                  # Season 2 ground truth
├── canon_s3/                  # Season 3 ground truth
├── planning/
│   └── arc.md                 # Full narrative arc (all 3 seasons)
└── scripts/
    ├── story_outlines_s1.py   # S1 outlines (ep → title + premise)
    ├── story_outlines_s2.py   # S2 outlines
    ├── story_outlines_s3.py   # S3 outlines
    ├── stories_s1_p01.py      # S1 story files (one per part)
    │   ... stories_s1_p09.py
    ├── stories_s2_p01.py ... stories_s2_p09.py
    ├── stories_s3_p01.py ... stories_s3_p11.py
    ├── stories_data_s1.py     # Aggregates S1 part files → STORIES_S1
    ├── stories_data_s2.py     # Aggregates S2 part files → STORIES_S2
    ├── stories_data_s3.py     # Aggregates S3 part files → STORIES_S3
    ├── generate_stories.py    # Generates all HTML
    ├── generate_audio.py      # Generates MP3s (Ryan voice, fixed)
    └── check_canon.py         # Consistency helper
```

## Story Data Format

Each part file exports a list named `STORIES_S{N}_P{NN}`:

```python
STORIES_S1_P01 = [
    {"ep": 1, "title": "Ako-chan's Morning", "text": "..."},
    {"ep": 2, "title": "The Silver in the Night", "text": "..."},
]
```

## Generating HTML

```bash
cd scripts
python generate_stories.py s1        # Season 1 only
python generate_stories.py s2        # Season 2 only
python generate_stories.py s3        # Season 3 only
python generate_stories.py all       # All seasons + root index
```

## Generating Audio

```bash
cd scripts
python generate_audio.py s1 all      # Season 1, all parts
python generate_audio.py s2 all      # Season 2, all parts
python generate_audio.py s3 all      # Season 3, all parts
python generate_audio.py s3 1 2 3    # Season 3, specific parts
```

Voice: `en-GB-RyanNeural` (fixed — do not change).

**Important**: Generate audio BEFORE running generate_stories.py, or the audio player UI will be silently omitted from story pages.

## Story Writing Workflow

### Writing a part (standard procedure)

When starting a new writing session for a specific part:

**1. Check the part list**
Open `planning/parts.md` — find the target season and part number.
Confirm: episode range, episode count, and which file to write to.

**2. Read the arc**
Open `planning/arc.md` — find the section for the target season and part.
Read the part summary, setting, and key events.

**3. Read the canon**
| Season | Canon files to read |
|---|---|
| S1 | `canon/characters.md`, `canon/world.md`, `canon/timeline.md` |
| S2 | `canon_s2/characters.md`, `canon_s2/world.md`, `canon_s2/timeline.md` |
| S3 | `canon_s3/characters.md`, `canon_s3/world.md`, `canon_s3/timeline.md` |

**4. Read the outlines**
Open `scripts/story_outlines_s{N}.py`.
Find the entries for the episodes you are about to write.
If an outline entry is missing, write a brief outline before writing the story.

**5. Read existing episodes in the part** (if the part is partially written)
Open `scripts/stories_s{N}_p{NN}.py` and read what is already there.
New episodes must follow naturally from the last written episode.

**6. Write the episodes**
Add new episodes to `scripts/stories_s{N}_p{NN}.py` following the data format:
```python
{
    "ep": N,
    "title": "...",
    "text": "...",
},
```
Follow CEFR A1 standard. Target ~200 words per episode.

**7. Preview**
```bash
cd scripts
python3 generate_stories.py s{N}
```
Open the generated HTML in a browser to check layout and flow.

**8. Update canon**
After writing, add new events to `canon_s{N}/timeline.md`.
Update `canon_s{N}/characters.md` if a new character appears or changes.

### Episode numbering

Episodes are numbered sequentially within each season (ep: 1, 2, 3, ...).
Part files are appended in order by `stories_data_s{N}.py`.
Do not reorder or renumber episodes within a season.

### Checking consistency

```bash
cd scripts
python3 check_canon.py character "Ako-chan"    # all appearances across seasons
python3 check_canon.py find "serial number"    # keyword search across seasons
python3 check_canon.py facts s1                # list all written S1 stories
python3 check_canon.py facts                   # list all written stories
```

## GitHub Pages

The site is deployed automatically on every push to `main` via
`.github/workflows/pages.yml`. All HTML is pre-generated — just commit
the generated files and push.

Enable Pages in the repository settings:
- **Source**: GitHub Actions
- No extra build step is needed.

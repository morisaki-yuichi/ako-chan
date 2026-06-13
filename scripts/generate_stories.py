#!/usr/bin/env python3
"""Generate HTML for Ako-chan.

Usage:
  python generate_stories.py s1        # Season 1
  python generate_stories.py s2        # Season 2
  python generate_stories.py s3        # Season 3
  python generate_stories.py all       # All seasons + root index
  python generate_stories.py index     # Root index only
"""

import re
import sys
import importlib
from pathlib import Path

ROOT = Path(__file__).parent.parent

MONTH_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_NAMES = ["", "January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# ── Season configurations ────────────────────────────────────────────────────

SEASONS = {
    "s1": {
        "dir":          "season1",
        "title":        "Ako-chan and the Robot Dog",
        "season_label": "Season 1",
        "subtitle":     "120 Episodes · 10 Parts",
        "ep_based":     True,
        "parts": [
            (1,  "England"),
            (2,  "Through Europe"),
            (3,  "Mediterranean"),
            (4,  "Japan"),
            (5,  "The North"),
            (6,  "South America"),
            (7,  "Toward the Ice"),
            (8,  "The Southern Signal"),
            (9,  "Obia's Confession"),
            (10, "We Are Home"),
        ],
        "narrative": (
            "Ako-chan and her puppy Dango set off on a long journey across the world. "
            "Along the way they meet new friends — and face mysteries they did not expect."
        ),
        "data_module": "stories_data_s1",
        "data_var":    "STORIES_S1",
        "audio_dir":   "s1",
        "gradients": {
            1: "135deg, #3a4a3a, #8a9a8a",   # England
            2: "135deg, #4a3a2a, #c8a050",   # Through Europe
            3: "135deg, #2a4a6a, #c8a050",   # Mediterranean
            4: "135deg, #6a3a5a, #e8a8c0",   # Japan
            5: "135deg, #2a4a5a, #6a8a9a",   # The North
            6: "135deg, #2a5a2a, #8a9a40",   # South America
            7: "135deg, #2a3a5a, #8aaaca",   # Toward the Ice
            8:  "135deg, #1a2a4a, #6a9aba",   # The Southern Signal
            9:  "135deg, #1a1a3a, #7a5a9a",   # Obia's Confession
            10: "135deg, #3a2a5a, #c4902a",   # We Are Home
        },
        # (keyword, emoji, display_name, join_date, exclude_window)
        "cast": [
            ("Ako-chan",       "🧒", "Ako-chan",       "01-01", None),
            ("Dango",          "🐕", "Dango",           "01-01", None),
            ("Obia",           "🤖", "Obia",            "01-11", None),
            ("Daru",           "🐢", "Daru",            "04-08", None),
            ("Gabu",           "🐊", "Gabu",            "04-17", None),
            ("Suke-san",       "🦊", "Suke-san",        "06-17", None),
            ("Riro",           "🦦", "Riro",            "07-08", None),
            ("Pen-san",        "🐧", "Pen-san",         "11-15", None),
            ("Colonel Adelie", "🐧", "Colonel Adelie",  "11-20", None),
            ("Yu-chan",        "🥼", "Yu-chan",          "12-12", None),
        ],
    },

    "s2": {
        "dir":          "season2",
        "title":        "Ako-chan and the Hidden Door",
        "season_label": "Season 2",
        "subtitle":     "108 Episodes · 9 Parts",
        "ep_based":     True,
        "parts": [
            (1,  "The Signal"),
            (2,  "Gathering"),
            (3,  "Into the Ice"),
            (4,  "The First Challenges"),
            (5,  "The Garden"),
            (6,  "Governance"),
            (7,  "Something Alive"),
            (8,  "The Truth"),
            (9,  "Through the Door"),
        ],
        "narrative": (
            "Back home in England, Ako-chan finds a hidden message. "
            "A new journey begins — this time into a world unlike anything she has seen before. "
            "Old friends return, and a truth slowly comes to light."
        ),
        "data_module": "stories_data_s2",
        "data_var":    "STORIES_S2",
        "audio_dir":   "s2",
        "gradients": {
            1: "135deg, #1a2a4a, #3a6a9a",   # The Signal
            2: "135deg, #2a3a5a, #5a8a9a",   # Gathering
            3: "135deg, #1a3a5a, #4a8a9a",   # Into the Ice
            4: "135deg, #1a3a5a, #3a9a7a",   # The First Challenges
            5: "135deg, #2a5a3a, #6a9a5a",   # The Garden
            6: "135deg, #3a2a5a, #6a6a8a",   # Governance
            7: "135deg, #5a3a1a, #c8802a",   # Something Alive
            8: "135deg, #5a2a2a, #c87040",   # The Truth
            9: "135deg, #3a3a2a, #9a8a5a",   # Through the Door
        },
        "cast": [
            ("Ako-chan",        "🧒", "Ako-chan",        "01-01", None),
            ("Dango",           "🐕", "Dango",            "01-01", None),
            ("Obia",            "🤖", "Obia",             "01-01", None),
            ("Ruka",            "🐢", "Ruka",             "01-01", None),
            ("Suke-san",        "🦊", "Suke-san",         "02-11", None),
            ("Riro",            "🦦", "Riro",             "02-17", None),
            ("Daru",            "🐢", "Daru",             "03-02", None),
            ("Gabu",            "🐊", "Gabu",             "03-10", None),
            ("Pen-san",         "🐧", "Pen-san",          "03-23", None),
            ("Colonel Adelie",  "🐧", "Colonel Adelie",   "03-25", None),
            ("Yu-chan",         "🥼", "Yu-chan",           "11-21", None),
        ],
    },

    "s3": {
        "dir":          "season3",
        "title":        "Ako-chan and the Boy with No Name",
        "season_label": "Season 3",
        "subtitle":     "99 Episodes · 11 Parts",
        "ep_based":     True,
        "parts": [
            (1,  "No Gaps"),
            (2,  "First Meeting"),
            (3,  "Second Meeting"),
            (4,  "Pattern Classified"),
            (5,  "Behavior Data Only"),
            (6,  "Full Records"),
            (7,  "Unrecordable"),
            (8,  "The Protocol"),
            (9,  "The Far South"),
            (10, "The Project"),
            (11, "Departure"),
        ],
        "narrative": (
            "Years after the journey ended, a young man wanders alone. "
            "He cannot remember faces. He only trusts what he can count. "
            "Yet one question keeps bringing him back — one he cannot put into numbers."
        ),
        "data_module": "stories_data_s3",
        "data_var":    "STORIES_S3",
        "audio_dir":   "s3",
        "gradients": {
            1:  "135deg, #2a3a4a, #6a8aaa",  # Tokyo, numbers — cool slate
            2:  "135deg, #7a4a6a, #e8a8c0",  # First meeting Ako — cherry pink
            3:  "135deg, #3a5a6a, #7ab0b8",  # Riro, invisible loss — muted sea
            4:  "135deg, #6a5a8a, #b8a8d8",  # Second encounter, déjà vu — lilac
            5:  "135deg, #7a6a4a, #c8b080",  # Central Asia, self-knowledge — ochre
            6:  "135deg, #8a6a20, #d4a040",  # Third encounter, drawn — amber
            7:  "135deg, #3a5a3a, #7a9a7a",  # Mediterranean — olive
            8:  "135deg, #2a2a5a, #5a6a9a",  # Yokohama: The Protocol — deep navy
            9:  "135deg, #7a4a4a, #c88080",  # The Far South — dusk rose
            10: "135deg, #3a4a5a, #7a9ab0",  # Yokohama: The Project — cold steel
            11: "135deg, #3a5a7a, #a0c8e8",  # Yokohama: Departure — snow blue
        },
        "cast": [
            ("the boy",        "👦", "the boy",         "01-01", None),
            ("Ako-chan",        "🧒", "Ako-chan",         "02-01", None),
            ("Dango",           "🐕", "Dango",            "02-01", None),
            ("Ruka",            "🐢", "Ruka",             "02-01", None),
            ("Suke-san",        "🦊", "Suke-san",         "01-01", None),
            ("Riro",            "🦦", "Riro",             "03-01", None),
            ("Gabu",            "🐊", "Gabu",             "07-01", None),
            ("Daru",            "🐢", "Daru",             "07-01", None),
            ("Pen-san",         "🐧", "Pen-san",          "10-01", None),
            ("Colonel Adelie",  "🐧", "Colonel Adelie",   "10-01", None),
            ("Obia",            "🤖", "Obia",             "12-01", None),
        ],
    },
}

# ── Character badge detection ────────────────────────────────────────────────

_ABSENT_PATTERNS = [
    r"think(?:s|ing)?\s+of\s+{kw}",
    r"thought\s+of\s+{kw}",
    r"dream(?:s|ed|ing)?\s+of\s+{kw}",
    r"remember(?:s|ed|ing)?\s+{kw}",
    r"wonder(?:s|ed|ing)?\s+about\s+{kw}",
    r"miss(?:es|ed|ing)?\s+{kw}",
    r"talk(?:s|ed|ing)?\s+about\s+{kw}",
    r"hear(?:s|d)?\s+(?:about|of)\s+{kw}",
    r"heard\s+(?:about|of)\s+{kw}",
]


def _is_present(keyword, text):
    for pat in _ABSENT_PATTERNS:
        text = re.sub(pat.format(kw=re.escape(keyword)), " ", text, flags=re.IGNORECASE)
    kw = re.escape(keyword)
    sentence_start = re.search(
        r'(?:^|(?<=[.?!\n])\s+)(?:(?:Then|And|But|So|Now),?\s+)?' + kw +
        r"\b(?!'s)(?!\s*[.?!])",
        text, re.IGNORECASE,
    )
    attribution = re.search(
        r'\b(?:says?|said|asks?|asked|replies?|replied|calls?|called)\s+' + kw + r'\b',
        text, re.IGNORECASE,
    )
    return bool(sentence_start or attribution)


def characters(date, text, cast):
    m = re.match(r"This is ([\w][\w-]*)'s story", text)
    if m:
        featured = m.group(1)
        for keyword, emoji, name, *_ in cast:
            if keyword == featured:
                return [(emoji, name)]

    detected = set()
    for keyword, _, _, _, exclude in cast:
        if exclude and exclude[0] <= date < exclude[1]:
            continue
        if _is_present(keyword, text):
            detected.add(keyword)

    joined = {kw for kw, _, _, jd, _ in cast if date >= jd}

    result = []
    for keyword, emoji, name, join_date, exclude in cast:
        if exclude and exclude[0] <= date < exclude[1]:
            continue
        if keyword in detected:
            result.append((emoji, name))
        elif keyword in joined and any(k in detected for k in joined if k != keyword):
            result.append((emoji, name))
    return result


# ── HTML helpers ─────────────────────────────────────────────────────────────

def day_number(month, day):
    return sum(MONTH_DAYS[1:month]) + day


def adjacent(month, day):
    prev = next_ = None
    if day > 1:
        prev = (month, day - 1)
    elif month > 1:
        prev = (month - 1, MONTH_DAYS[month - 1])
    if day < MONTH_DAYS[month]:
        next_ = (month, day + 1)
    elif month < 12:
        next_ = (month + 1, 1)
    return prev, next_


def paras_html(text):
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    def render(b):
        b = re.sub(r'_([^_]+)_', r'<em>\1</em>', b)
        return f"      <p>{b}</p>"
    return "\n".join(render(b) for b in blocks)


# ── Audio player ─────────────────────────────────────────────────────────────

_PLAYER_JS = """
    <script>
    (function() {
      var audio = document.getElementById('playAudio');
      var btn   = document.getElementById('playBtn');
      var bar   = document.getElementById('playBar');
      var wrap  = document.getElementById('playWrap');
      var lbl   = document.getElementById('playTime');
      function fmt(s) {
        var m = Math.floor(s / 60), sec = Math.floor(s % 60);
        return m + ':' + (sec < 10 ? '0' : '') + sec;
      }
      btn.addEventListener('click', function() {
        if (audio.paused) { audio.play(); btn.textContent = '⏸'; }
        else { audio.pause(); btn.textContent = '▶'; }
      });
      document.getElementById('seekBack').addEventListener('click', function() {
        audio.currentTime = Math.max(0, audio.currentTime - 5);
      });
      document.getElementById('seekFwd').addEventListener('click', function() {
        audio.currentTime = Math.min(audio.duration || 0, audio.currentTime + 5);
      });
      audio.addEventListener('timeupdate', function() {
        if (audio.duration) {
          bar.style.width = (audio.currentTime / audio.duration * 100) + '%';
          lbl.textContent = fmt(audio.currentTime) + ' / ' + fmt(audio.duration);
        }
      });
      audio.addEventListener('ended', function() {
        btn.textContent = '▶';
        bar.style.width = '0';
        lbl.textContent = '0:00 / ' + fmt(audio.duration);
      });
      wrap.addEventListener('click', function(e) {
        if (!audio.duration) return;
        var r = wrap.getBoundingClientRect();
        audio.currentTime = ((e.clientX - r.left) / r.width) * audio.duration;
      });
      var spds = document.querySelectorAll('.ply-spd');
      spds.forEach(function(b) {
        b.addEventListener('click', function() {
          audio.playbackRate = parseFloat(this.dataset.rate);
          spds.forEach(function(s) { s.classList.remove('on'); });
          this.classList.add('on');
        });
      });
    })();
    </script>"""


def build_player(date, audio_dir, has_audio):
    if not has_audio:
        return ""
    src = f"../audio/{audio_dir}/{date}.mp3"
    return f"""\
    <div class="player">
      <div class="ply-ctrl">
        <button class="ply-seek" id="seekBack">−5s</button>
        <button class="ply-btn" id="playBtn" aria-label="Play">▶</button>
        <button class="ply-seek" id="seekFwd">+5s</button>
      </div>
      <div class="ply-prog" id="playWrap">
        <div class="ply-bar" id="playBar"></div>
      </div>
      <span class="ply-time" id="playTime">0:00</span>
      <div class="ply-speeds">
        <button class="ply-spd" data-rate="0.8">0.8×</button>
        <button class="ply-spd on" data-rate="1">1×</button>
        <button class="ply-spd" data-rate="1.2">1.2×</button>
        <button class="ply-spd" data-rate="1.5">1.5×</button>
      </div>
      <audio id="playAudio" src="{src}" preload="none"></audio>
    </div>
{_PLAYER_JS}"""


# ── Ep-based story template (Season 3) ───────────────────────────────────────

_STORY_EP_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Ep {ep}</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
</head>
<body>
  <article class="book">
    <header class="cover">
      <div class="date-label">{season_label} · Ep {ep}</div>
      <h1>{title}</h1>
    </header>
{player}
    <section class="story">
{paragraphs}
    </section>
    <nav class="nav">
      {prev_link}
      <a class="dc" href="index.html">Ep {ep} / {total}</a>
      {next_link}
    </nav>
  </article>
</body>
</html>"""


def render_story_ep(story, season_cfg, prev_key, next_key, has_audio, total):
    ep = story["ep"]
    part = story.get("part", 1)
    grad = season_cfg["gradients"][part]
    ep_slug = f"ep-{ep:03d}"
    css = _STORY_CSS.replace("{gradient}", grad)

    def link(key, label):
        if key is None:
            return f'<span style="visibility:hidden">{label}</span>'
        return f'<a href="{key}.html">{label}</a>'

    return _STORY_EP_TMPL.format(
        title=story["title"],
        ep=ep,
        total=total,
        season_label=season_cfg.get("season_label", season_cfg["title"].split(":")[0]),
        css=css,
        paragraphs=paras_html(story["text"]),
        prev_link=link(prev_key, "← Previous"),
        next_link=link(next_key, "Next →"),
        player=build_player(ep_slug, season_cfg["audio_dir"], has_audio),
    )


# ── Story page template ───────────────────────────────────────────────────────

_STORY_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; padding: 1.5rem 1rem 4rem; }
    .book { max-width: 620px; margin: 0 auto; background: #fffdf5; border-radius: 24px; box-shadow: 0 8px 40px rgba(100,60,20,0.12); }
    .cover { background: linear-gradient({gradient}); padding: 2.5rem 2rem 1.75rem; text-align: center; border-radius: 24px 24px 0 0; }
    .date-label { font-size: 0.78rem; font-weight: 700; color: rgba(255,255,255,0.85); text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
    .cover h1 { font-size: 1.5rem; font-weight: 800; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,0.2); line-height: 1.3; margin-bottom: 0.75rem; }
    .story { padding: 2rem 2.25rem 2.5rem; }
    .story p { font-size: 1.125rem; line-height: 2.1; margin-bottom: 0.9rem; }
    .story p:last-child { margin-bottom: 0; }
    .player { position: sticky; top: 0; z-index: 100; background: #fffdf5; display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; padding: 0.65rem 2.25rem; border-bottom: 2px dashed #e8d0b8; box-shadow: 0 2px 8px rgba(100,60,20,0.07); }
    .ply-ctrl { display: flex; align-items: center; gap: 0.35rem; flex-shrink: 0; }
    .ply-btn { width: 2rem; height: 2rem; border-radius: 50%; border: none; background: #9a7a5a; color: #fff; font-size: 0.8rem; cursor: pointer; }
    .ply-btn:hover { background: #7a5a3a; }
    .ply-seek { height: 1.75rem; padding: 0 0.5rem; border: none; background: #f5ede0; color: #7a5a3a; font-size: 0.75rem; font-weight: 700; border-radius: 12px; cursor: pointer; white-space: nowrap; }
    .ply-seek:hover { background: #e8d0b8; }
    .ply-prog { flex: 1; min-width: 60px; height: 5px; background: #e8d0b8; border-radius: 3px; cursor: pointer; }
    .ply-bar { height: 100%; background: #9a7a5a; border-radius: 3px; width: 0; }
    .ply-time { font-size: 0.7rem; font-weight: 700; color: #b8987a; white-space: nowrap; flex-shrink: 0; }
    .ply-speeds { display: flex; gap: 0.2rem; margin-left: auto; }
    .ply-spd { padding: 0.15rem 0.4rem; font-size: 0.7rem; font-weight: 700; border: 1.5px solid #e8d0b8; background: transparent; color: #9a7a5a; border-radius: 4px; cursor: pointer; }
    .ply-spd.on { background: #9a7a5a; color: #fff; border-color: #9a7a5a; }
    .nav { display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 2rem; border-top: 2px dashed #e8d0b8; gap: 0.5rem; }
    .nav a { font-size: 0.88rem; font-weight: 700; color: #9a7a5a; text-decoration: none; padding: 0.35rem 0.75rem; border-radius: 8px; background: #f5ede0; white-space: nowrap; }
    .nav a:hover { background: #e8d0b8; }
    .dc { font-size: 0.78rem; color: #b8987a; font-weight: 700; white-space: nowrap; text-decoration: none; }
    .dc:hover { color: #9a7a5a; }
    @media (max-width: 480px) { .cover h1 { font-size: 1.25rem; } .story p { font-size: 1rem; } .story { padding: 1.5rem 1.5rem 2rem; } .nav { padding: 0.75rem 1.25rem; } .player { padding: 0.6rem 1.5rem; } .ply-speeds { margin-left: 0; width: 100%; justify-content: flex-end; } }"""

_STORY_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {mname} {day}</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
</head>
<body>
  <article class="book">
    <header class="cover">
      <div class="date-label">{season_label} · {mname} {day}</div>
      <h1>{title}</h1>
    </header>
{player}
    <section class="story">
{paragraphs}
    </section>
    <nav class="nav">
      {prev_link}
      <a class="dc" href="index.html">Day {daynum} / 365</a>
      {next_link}
    </nav>
  </article>
</body>
</html>"""


def render_story(story, season_cfg, prev_md, next_md, has_audio):
    mm, dd = story["date"].split("-")
    month, day = int(mm), int(dd)
    date = story["date"]
    grad = season_cfg["gradients"][month]
    chars = characters(date, story["text"], season_cfg["cast"])
    badges = "".join(f'<span class="fbadge">{e} {n}</span>' for e, n in chars)
    daynum = day_number(month, day)
    css = _STORY_CSS.replace("{gradient}", grad)

    def link(md, label):
        if md is None:
            return f'<span style="visibility:hidden">{label}</span>'
        m, d = md
        return f'<a href="{m:02d}-{d:02d}.html">{label}</a>'

    return _STORY_TMPL.format(
        title=story["title"],
        mname=MONTH_NAMES[month],
        day=day,
        season_label=season_cfg["title"].split(":")[0],
        css=css,
        gradient=grad,
        badges=badges,
        paragraphs=paras_html(story["text"]),
        daynum=daynum,
        prev_link=link(prev_md, "← Previous"),
        next_link=link(next_md, "Next →"),
        player=build_player(date, season_cfg["audio_dir"], has_audio),
    )


# ── Season index (calendar) ───────────────────────────────────────────────────

_SEASON_INDEX_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; padding: 1.5rem 1rem 4rem; }
    .page { max-width: 900px; margin: 0 auto; }
    .hd { text-align: center; padding: 2rem 1rem 2.5rem; }
    .hd h1 { font-size: 1.6rem; font-weight: 800; color: #5a3a1a; margin-bottom: 0.3rem; }
    .hd .sub { font-size: 0.9rem; color: #9a7a5a; margin-bottom: 0.6rem; }
    .hd .desc { font-size: 0.88rem; color: #7a5a3a; max-width: 540px; margin: 0 auto 1.2rem; line-height: 1.7; }
    .back { display: inline-block; font-size: 0.82rem; font-weight: 700; color: #9a7a5a; text-decoration: none; padding: 0.3rem 0.75rem; background: #f5ede0; border-radius: 8px; }
    .back:hover { background: #e8d0b8; }
    .months { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1.5rem; }
    .mc { background: #fffdf5; border-radius: 14px; box-shadow: 0 3px 14px rgba(100,60,20,0.1); overflow: hidden; }
    .mh { padding: 0.55rem 0.75rem; font-size: 0.82rem; font-weight: 800; color: #fff; letter-spacing: 0.04em; }
    .days { display: grid; grid-template-columns: repeat(7, 1fr); padding: 0.6rem 0.5rem 0.7rem; gap: 1px; }
    .days a { display: flex; align-items: center; justify-content: center; height: 2rem; font-size: 0.8rem; font-weight: 700; color: #7a5a3a; text-decoration: none; border-radius: 5px; }
    .days a:hover { background: #f5ede0; }
    .days .nd { display: flex; align-items: center; justify-content: center; height: 2rem; font-size: 0.8rem; font-weight: 600; color: #c8b09a; }
    .days .em { height: 2rem; }
    .stats { font-size: 0.75rem; color: #b8987a; text-align: center; margin-top: 0.35rem; padding: 0 0.5rem 0.5rem; }
    @media (max-width: 700px) { .months { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 380px) { .months { grid-template-columns: 1fr; } }"""

_SEASON_INDEX_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{season_title}</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
</head>
<body>
  <div class="page">
    <div class="hd">
      <h1>{season_title}</h1>
      <p class="sub">{subtitle}</p>
      <p class="desc">{narrative}</p>
      <a class="back" href="../index.html">← Ako-chan</a>
    </div>
    <div class="months">
{months_html}
    </div>
  </div>
</body>
</html>"""


def generate_season_index(season_key, stories_by_date, season_cfg):
    out_dir = ROOT / season_cfg["dir"]
    out_dir.mkdir(exist_ok=True)
    gradients = season_cfg["gradients"]
    audio_dir = ROOT / "audio" / season_cfg["audio_dir"]

    blocks = []
    for month in range(1, 13):
        grad = gradients[month]
        days = MONTH_DAYS[month]
        written = 0
        total = days
        cells = []
        for day in range(1, days + 1):
            date = f"{month:02d}-{day:02d}"
            if date in stories_by_date:
                written += 1
                title = stories_by_date[date]["title"]
                cells.append(f'<a href="{date}.html" title="{title}">{day}</a>')
            else:
                cells.append(f'<div class="nd">{day}</div>')
        pad = (7 - days % 7) % 7
        cells.extend(['<div class="em"></div>'] * pad)
        pct = f"{written}/{total}"
        blocks.append(
            f'      <div class="mc">\n'
            f'        <div class="mh" style="background:linear-gradient({grad})">{MONTH_NAMES[month]}</div>\n'
            f'        <div class="days">{"".join(cells)}</div>\n'
            f'        <div class="stats">{pct} stories</div>\n'
            f'      </div>'
        )

    html = _SEASON_INDEX_TMPL.format(
        season_title=season_cfg["title"],
        subtitle=season_cfg["subtitle"],
        narrative=season_cfg["narrative"],
        css=_SEASON_INDEX_CSS,
        months_html="\n".join(blocks),
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote: {season_cfg['dir']}/index.html")


# ── Ep-based season index (Season 3) ─────────────────────────────────────────

_SEASON_INDEX_EP_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; padding: 1.5rem 1rem 4rem; }
    .page { max-width: 900px; margin: 0 auto; }
    .hd { text-align: center; padding: 2rem 1rem 2.5rem; }
    .hd h1 { font-size: 1.6rem; font-weight: 800; color: #5a3a1a; margin-bottom: 0.3rem; }
    .hd .sub { font-size: 0.9rem; color: #9a7a5a; margin-bottom: 0.6rem; }
    .hd .desc { font-size: 0.88rem; color: #7a5a3a; max-width: 540px; margin: 0 auto 1.2rem; line-height: 1.7; }
    .back { display: inline-block; font-size: 0.82rem; font-weight: 700; color: #9a7a5a; text-decoration: none; padding: 0.3rem 0.75rem; background: #f5ede0; border-radius: 8px; }
    .back:hover { background: #e8d0b8; }
    .parts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem; }
    .pc { background: #fffdf5; border-radius: 14px; box-shadow: 0 3px 14px rgba(100,60,20,0.1); overflow: hidden; }
    .ph { padding: 0.55rem 0.75rem; font-size: 0.82rem; font-weight: 800; color: #fff; letter-spacing: 0.04em; }
    .eps { display: flex; flex-direction: column; padding: 0.4rem 0.5rem; }
    .eps a { display: block; padding: 0.28rem 0.5rem; font-size: 0.8rem; font-weight: 600; color: #7a5a3a; text-decoration: none; border-radius: 4px; }
    .eps a:hover { background: #f5ede0; }
    .eps .nd { display: block; padding: 0.28rem 0.5rem; font-size: 0.8rem; color: #c8b09a; }
    .stats { font-size: 0.75rem; color: #b8987a; text-align: center; margin-top: 0.35rem; padding: 0 0.5rem 0.5rem; }
    @media (max-width: 600px) { .parts { grid-template-columns: 1fr; } }"""

_SEASON_INDEX_EP_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{season_title}</title>
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
</head>
<body>
  <div class="page">
    <div class="hd">
      <h1>{season_title}</h1>
      <p class="sub">{subtitle}</p>
      <p class="desc">{narrative}</p>
      <a class="back" href="../index.html">← Ako-chan</a>
    </div>
    <div class="parts">
{parts_html}
    </div>
  </div>
</body>
</html>"""


def generate_season_index_ep(season_key, stories_by_ep, season_cfg):
    out_dir = ROOT / season_cfg["dir"]
    out_dir.mkdir(exist_ok=True)
    gradients = season_cfg["gradients"]
    parts_cfg = season_cfg.get("parts", [])

    parts_data = {}
    for key in sorted(stories_by_ep.keys()):
        story = stories_by_ep[key]
        part_num = story.get("part", 1)
        parts_data.setdefault(part_num, []).append((key, story))

    blocks = []
    for part_num, part_name in parts_cfg:
        grad = gradients[part_num]
        part_stories = parts_data.get(part_num, [])
        written = len(part_stories)

        ep_links = []
        for key, story in part_stories:
            ep_links.append(f'<a href="{key}.html">Ep {story["ep"]} · {story["title"]}</a>')

        blocks.append(
            f'      <div class="pc">\n'
            f'        <div class="ph" style="background:linear-gradient({grad})">Part {part_num} · {part_name}</div>\n'
            f'        <div class="eps">{"".join(ep_links)}</div>\n'
            f'        <div class="stats">{written} episodes</div>\n'
            f'      </div>'
        )

    html = _SEASON_INDEX_EP_TMPL.format(
        season_title=season_cfg["title"],
        subtitle=season_cfg["subtitle"],
        narrative=season_cfg["narrative"],
        css=_SEASON_INDEX_EP_CSS,
        parts_html="\n".join(blocks),
    )
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote: {season_cfg['dir']}/index.html")


# ── Root index ────────────────────────────────────────────────────────────────

_ROOT_CSS = """\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Nunito', sans-serif; background: #fdf6e3; color: #3d2b1f; min-height: 100vh; }
    .hero { background: linear-gradient(160deg, #2a1a4a 0%, #5a3a1a 60%, #3a2a0a 100%); padding: 4rem 1.5rem 3rem; text-align: center; }
    .hero h1 { font-size: 2.4rem; font-weight: 800; color: #fff; text-shadow: 0 3px 16px rgba(0,0,0,0.35); margin-bottom: 0.5rem; letter-spacing: -0.01em; }
    .hero p { font-size: 1rem; color: rgba(255,255,255,0.8); max-width: 560px; margin: 0 auto; line-height: 1.7; text-wrap: balance; }
    .seasons { display: grid; grid-template-columns: 1fr; gap: 1.5rem; max-width: 560px; margin: -2rem auto 0; padding: 0 1.5rem 4rem; }
    .card { background: #fffdf5; border-radius: 20px; box-shadow: 0 6px 30px rgba(100,60,20,0.14); overflow: hidden; text-decoration: none; color: inherit; display: block; transition: transform 0.18s, box-shadow 0.18s; }
    .card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(100,60,20,0.2); }
    .card-band { height: 6px; }
    .card-body { padding: 1.5rem 1.5rem 1.25rem; }
    .season-num { font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: #9a7a5a; margin-bottom: 0.35rem; }
    .card h2 { font-size: 1.15rem; font-weight: 800; color: #3d2b1f; margin-bottom: 0.55rem; line-height: 1.3; }
    .card p { font-size: 0.85rem; color: #7a5a3a; line-height: 1.7; margin-bottom: 1rem; }
    .read-link { display: inline-block; font-size: 0.82rem; font-weight: 700; color: #fff; background: #9a7a5a; padding: 0.3rem 0.85rem; border-radius: 20px; }
    @media (max-width: 700px) { .hero h1 { font-size: 1.8rem; } }"""

_ROOT_TMPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ako-chan</title>
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
</head>
<body>
  <div class="hero">
    <h1>Ako-chan</h1>
    <p>A girl who hears what others cannot — across three seasons and two worlds.</p>
  </div>
  <div class="seasons">
    <a class="card" href="season1/index.html">
      <div class="card-band" style="background:linear-gradient(90deg,#3a2a5a,#d4a040)"></div>
      <div class="card-body">
        <div class="season-num">Season 1</div>
        <h2>Ako-chan and the Robot Dog</h2>
        <p>A silver dog appears in the park — and it knows Ako-chan's name. Something is wrong far away, and the answer may lie at the end of a long journey.</p>
        <span class="read-link">Read Season 1 →</span>
      </div>
    </a>
    <a class="card" href="season2/index.html">
      <div class="card-band" style="background:linear-gradient(90deg,#2a4a6a,#5a9a5a)"></div>
      <div class="card-body">
        <div class="season-num">Season 2</div>
        <h2>Ako-chan and the Hidden Door</h2>
        <p>Back home, a hidden message leads Ako-chan through a door that should not exist — into a world that was waiting for her.</p>
        <span class="read-link">Read Season 2 →</span>
      </div>
    </a>
    <a class="card" href="season3/index.html">
      <div class="card-band" style="background:linear-gradient(90deg,#2a3a4a,#d4b060)"></div>
      <div class="card-body">
        <div class="season-num">Season 3</div>
        <h2>Ako-chan and the Boy with No Name</h2>
        <p>A young man who cannot remember faces wanders alone — and one question keeps bringing him back to the same girl.</p>
        <span class="read-link">Read Season 3 →</span>
      </div>
    </a>
  </div>
</body>
</html>"""


def generate_root_index():
    html = _ROOT_TMPL.format(css=_ROOT_CSS)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("  wrote: index.html")


# ── Season generator ──────────────────────────────────────────────────────────

def load_stories(season_key):
    cfg = SEASONS[season_key]
    sys.path.insert(0, str(Path(__file__).parent))
    mod = importlib.import_module(cfg["data_module"])
    stories = getattr(mod, cfg["data_var"])
    if cfg.get("ep_based"):
        return {f"ep-{s['ep']:03d}": s for s in stories}
    return {s["date"]: s for s in stories}


def generate_season_ep(season_key):
    cfg = SEASONS[season_key]
    out_dir = ROOT / cfg["dir"]
    out_dir.mkdir(exist_ok=True)
    audio_dir = ROOT / "audio" / cfg["audio_dir"]

    stories_by_ep = load_stories(season_key)
    ep_keys = sorted(stories_by_ep.keys())
    total = len(ep_keys)

    count = 0
    for i, key in enumerate(ep_keys):
        story = stories_by_ep[key]
        prev_key = ep_keys[i - 1] if i > 0 else None
        next_key = ep_keys[i + 1] if i < total - 1 else None
        has_audio = (audio_dir / f"{key}.mp3").exists()
        html = render_story_ep(story, cfg, prev_key, next_key, has_audio, total)
        (out_dir / f"{key}.html").write_text(html, encoding="utf-8")
        flag = " [♪]" if has_audio else ""
        print(f"  wrote: {cfg['dir']}/{key}.html{flag}")
        count += 1

    generate_season_index_ep(season_key, stories_by_ep, cfg)
    print(f"\n  {cfg['title']}: {count} stories written.")


def generate_season(season_key):
    cfg = SEASONS[season_key]
    if cfg.get("ep_based"):
        generate_season_ep(season_key)
        return

    out_dir = ROOT / cfg["dir"]
    out_dir.mkdir(exist_ok=True)
    audio_dir = ROOT / "audio" / cfg["audio_dir"]

    stories_by_date = load_stories(season_key)

    # Build adjacency map (only written stories)
    written_dates = sorted(stories_by_date.keys())

    def adjacent_written(date):
        idx = written_dates.index(date)
        prev_d = written_dates[idx - 1] if idx > 0 else None
        next_d = written_dates[idx + 1] if idx < len(written_dates) - 1 else None
        def to_md(d):
            if d is None:
                return None
            mm, dd = d.split("-")
            return (int(mm), int(dd))
        return to_md(prev_d), to_md(next_d)

    count = 0
    for date, story in sorted(stories_by_date.items()):
        mm, dd = date.split("-")
        month, day = int(mm), int(dd)
        prev_md, next_md = adjacent_written(date)
        has_audio = (audio_dir / f"{date}.mp3").exists()
        html = render_story(story, cfg, prev_md, next_md, has_audio)
        (out_dir / f"{date}.html").write_text(html, encoding="utf-8")
        flag = " [♪]" if has_audio else ""
        print(f"  wrote: {cfg['dir']}/{date}.html{flag}")
        count += 1

    generate_season_index(season_key, stories_by_date, cfg)
    print(f"\n  {cfg['title']}: {count} stories written.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:] or ["all"]

    if "all" in args:
        targets = list(SEASONS.keys())
        do_index = True
    else:
        targets = [a for a in args if a in SEASONS]
        do_index = "index" in args or not targets

    for key in targets:
        print(f"\n── {SEASONS[key]['title']} ──")
        generate_season(key)

    if do_index or targets:
        print("\n── Root index ──")
        generate_root_index()

    print("\nDone.")


if __name__ == "__main__":
    main()

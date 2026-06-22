#!/usr/bin/env python3
"""Generate index.html listing every built presentation.

Walks the immediate subdirectories of the repo root (excluding reference/,
scripts/, theme/, node_modules/ and dotted dirs), reads the YAML frontmatter
from each `slides.md` (title, date, description), and writes an index.html
linking to the built HTML and PDF for each deck, newest first.

Styled with the cburr palette. Invoked by `pixi run index`.
"""
from __future__ import annotations

import base64
import datetime
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "theme" / "fonts"
EXCLUDE = {"reference", "scripts", "theme", "node_modules", "assets"}

# (file, family, weight, style) — embedded so the index matches the deck
# typography on GitHub Pages without depending on system-installed fonts.
EMBED_FONTS = [
    ("Overlock-Regular.ttf", "Overlock", 400, "normal"),
    ("Overlock-Italic.ttf", "Overlock", 400, "italic"),
    ("Overlock-Bold.ttf", "Overlock", 700, "normal"),
    ("Overlock-Black.ttf", "Overlock", 900, "normal"),
    ("FiraMono-Regular.ttf", "Fira Mono", 400, "normal"),
]


def font_face_css() -> str:
    blocks = []
    for fname, family, weight, style in EMBED_FONTS:
        path = FONTS / fname
        if not path.exists():
            continue
        b64 = base64.b64encode(path.read_bytes()).decode()
        blocks.append(
            f'  @font-face {{ font-family: "{family}"; font-weight: {weight}; '
            f"font-style: {style}; font-display: swap; "
            f'src: url("data:font/ttf;base64,{b64}") format("truetype"); }}'
        )
    return "\n".join(blocks)

INK = "#4A1789"
INK_SOFT = "#6A3FA8"
GOLD = "#F4C20D"
PAPER = "#FFFFFF"
MUTED = "#6C7280"
RULE = "rgba(74, 23, 137, 0.18)"


def parse_frontmatter(md: Path) -> dict[str, str]:
    """Minimal YAML-frontmatter reader: top-of-file block between '---' lines.

    Only flat `key: value` pairs are needed (title, date, description).
    """
    text = md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() in ("---", "..."):
            break
        if ":" not in line or line[:1] in (" ", "\t", "#"):
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip("'\"")
        out[key.strip().lower()] = value
    return out


def coerce_date(value: str) -> datetime.date | None:
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def collect() -> list[dict]:
    decks = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if d.name in EXCLUDE or d.name.startswith("."):
            continue
        md = d / "slides.md"
        if not md.exists():
            continue
        fm = parse_frontmatter(md)
        date = coerce_date(fm.get("date", "")) or coerce_date(d.name[:10])
        decks.append(
            {
                "slug": d.name,
                "title": fm.get("title") or d.name,
                "description": fm.get("description", ""),
                "date": date,
                "date_str": date.strftime("%-d %B %Y") if date else "",
                "html": f"{d.name}/slides.html" if (d / "slides.html").exists() else None,
                "pdf": f"{d.name}/slides.pdf" if (d / "slides.pdf").exists() else None,
            }
        )
    # reverse date order; undated decks sort to the bottom
    decks.sort(key=lambda x: (x["date"] or datetime.date.min), reverse=True)
    return decks


def render(decks: list[dict]) -> str:
    cards = []
    for deck in decks:
        title = html.escape(deck["title"])
        desc = html.escape(deck["description"])
        date_str = html.escape(deck["date_str"])
        links = []
        if deck["html"]:
            links.append(f'<a class="btn" href="{html.escape(deck["html"])}">View&nbsp;slides</a>')
        if deck["pdf"]:
            links.append(f'<a class="btn pdf" href="{html.escape(deck["pdf"])}">PDF</a>')
        if not links:
            links.append('<span class="unbuilt">not built yet</span>')
        cards.append(
            f"""      <li class="card">
        <div class="meta">{date_str}</div>
        <h2>{title}</h2>
        {f'<p class="desc">{desc}</p>' if desc else ''}
        <div class="links">{''.join(links)}</div>
      </li>"""
        )
    body = "\n".join(cards) if cards else '      <li class="empty">No presentations built yet.</li>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talks &middot; Chris Burr</title>
<style>
{font_face_css()}
  :root {{
    --ink: {INK}; --ink-soft: {INK_SOFT}; --gold: {GOLD};
    --paper: {PAPER}; --muted: {MUTED}; --rule: {RULE};
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: var(--paper); color: var(--ink); }}
  body {{
    font-family: "Overlock", Georgia, serif;
    line-height: 1.3;
    -webkit-font-smoothing: antialiased;
  }}
  header.masthead {{
    background: var(--ink);
    color: var(--paper);
    padding: 56px 8vw 40px;
  }}
  header.masthead h1 {{ margin: 0; font-size: 48px; font-weight: 900; letter-spacing: -0.01em; }}
  header.masthead p {{ margin: 10px 0 0; font-size: 20px; opacity: 0.85; }}
  main {{ max-width: 980px; margin: 0 auto; padding: 40px 8vw 80px; }}
  ul.decks {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 24px; }}
  .card {{
    border: 1px solid var(--rule);
    border-left: 4px solid var(--ink);
    padding: 22px 26px;
  }}
  .card .meta {{
    font-family: "Fira Mono", Menlo, monospace;
    font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--muted);
  }}
  .card h2 {{ margin: 6px 0 0; font-size: 28px; font-weight: 700; color: var(--ink); }}
  .card .desc {{ margin: 8px 0 0; font-size: 18px; color: var(--ink); }}
  .links {{ margin-top: 16px; display: flex; gap: 12px; flex-wrap: wrap; }}
  a.btn {{
    display: inline-block;
    font-size: 16px; font-weight: 700;
    text-decoration: none;
    color: var(--paper); background: var(--ink);
    padding: 8px 18px;
  }}
  a.btn:hover {{ background: var(--ink-soft); }}
  a.btn.pdf {{ background: var(--paper); color: var(--ink); border: 1px solid var(--ink); }}
  a.btn.pdf:hover {{ background: rgba(74,23,137,0.06); }}
  .unbuilt {{ color: var(--muted); font-style: italic; }}
  .empty {{ color: var(--muted); font-style: italic; list-style: none; }}
  footer {{
    max-width: 980px; margin: 0 auto; padding: 0 8vw 60px;
    color: var(--muted); font-size: 15px; font-style: italic;
  }}
  footer a {{ color: var(--gold); text-decoration: underline; text-underline-offset: 3px; }}
</style>
</head>
<body>
  <header class="masthead">
    <h1>Talks</h1>
    <p>Chris Burr &middot; CERN / LHCb</p>
  </header>
  <main>
    <ul class="decks">
{body}
    </ul>
  </main>
  <footer>
    Built with <a href="https://marp.app/">Marp</a> &middot; {len(decks)} presentation{'s' if len(decks) != 1 else ''}.
  </footer>
</body>
</html>
"""


def main() -> int:
    decks = collect()
    out = ROOT / "index.html"
    out.write_text(render(decks), encoding="utf-8")
    print(f"wrote {out} ({len(decks)} presentation(s))")
    for deck in decks:
        print(f"  - {deck['slug']}: {deck['title']} [{deck['date_str'] or 'undated'}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

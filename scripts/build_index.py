#!/usr/bin/env python3
"""Generate index.html listing every built presentation.

Walks the immediate subdirectories of the repo root (excluding reference/,
scripts/, theme/, node_modules/ and dotted dirs), reads the YAML frontmatter
from each `slides.md` (title, date, description), and writes an index.html
linking to the built HTML and PDF for each deck, newest first.

The landing page has its own look — deliberately *not* the slide theme: the
cloud-chamber photo fills the viewport and the talks sit in translucent
frosted-glass cards over it, in a clean system sans. Invoked by `pixi run index`.
"""
from __future__ import annotations

import base64
import datetime
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "theme" / "assets"
EXCLUDE = {"reference", "scripts", "theme", "node_modules", "assets"}

# Clean system-sans stacks — the landing page intentionally does NOT use
# Overlock (that's the slide voice); these need no embedding.
FONT_SANS = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, '
    "Helvetica, Arial, sans-serif"
)
FONT_MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace'


def cloud_chamber_uri() -> str:
    """The masthead photo as a base64 data URI, so the page is self-contained."""
    img = ASSETS / "cloud-chamber.jpeg"
    if not img.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(img.read_bytes()).decode()


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
                # Link to the deck directory (served by its index.html) for a clean URL.
                "html": f"{d.name}/" if (d / "index.html").exists() else None,
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
        date_str = html.escape(deck["date_str"]).upper()
        links = []
        if deck["html"]:
            links.append(f'<a class="btn primary" href="{html.escape(deck["html"])}">View&nbsp;slides</a>')
        if deck["pdf"]:
            links.append(f'<a class="btn" href="{html.escape(deck["pdf"])}">PDF</a>')
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
    body = "\n".join(cards) if cards else '      <li class="card empty">No presentations built yet.</li>'
    count = f"{len(decks)} presentation{'s' if len(decks) != 1 else ''}"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talks &middot; Chris Burr</title>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; }}
  body {{
    font-family: {FONT_SANS};
    line-height: 1.4;
    color: #f3f0fb;
    -webkit-font-smoothing: antialiased;
    min-height: 100vh;
  }}
  /* Cloud-chamber fills the viewport and stays put while content scrolls; a
     purple-tinted scrim darkens it so the frosted cards read clearly. */
  body::before {{
    content: "";
    position: fixed;
    inset: 0;
    z-index: -1;
    background:
      linear-gradient(180deg, rgba(20,10,45,0.55), rgba(20,10,45,0.68)),
      url("{cloud_chamber_uri()}") center / cover no-repeat;
  }}
  .wrap {{ max-width: 840px; margin: 0 auto; padding: 7vh 24px 64px; }}

  /* Header — its own frosted panel */
  .masthead {{
    backdrop-filter: blur(16px) saturate(130%);
    -webkit-backdrop-filter: blur(16px) saturate(130%);
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px;
    padding: 30px 34px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  }}
  .masthead h1 {{ margin: 0; font-size: clamp(34px, 6vw, 52px); font-weight: 800; letter-spacing: -0.02em; }}
  .masthead p {{
    margin: 8px 0 0; font-size: 16px; letter-spacing: 0.04em;
    text-transform: uppercase; color: rgba(243,240,251,0.78);
    font-family: {FONT_MONO};
  }}

  ul.decks {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 20px; }}

  /* Talk cards — frosted glass */
  .card {{
    backdrop-filter: blur(14px) saturate(125%);
    -webkit-backdrop-filter: blur(14px) saturate(125%);
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 24px 28px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
  }}
  .card:hover {{
    transform: translateY(-3px);
    background: rgba(255,255,255,0.14);
    border-color: rgba(255,255,255,0.32);
  }}
  .card .meta {{
    font-family: {FONT_MONO};
    font-size: 12px; letter-spacing: 0.12em;
    color: rgba(243,240,251,0.72);
  }}
  .card h2 {{ margin: 8px 0 0; font-size: 26px; font-weight: 700; letter-spacing: -0.01em; color: #fff; }}
  .card .desc {{ margin: 8px 0 0; font-size: 16px; color: rgba(243,240,251,0.82); }}
  .card.empty {{ text-align: center; color: rgba(243,240,251,0.7); }}

  .links {{ margin-top: 18px; display: flex; gap: 12px; flex-wrap: wrap; }}
  a.btn {{
    display: inline-block;
    font-size: 15px; font-weight: 600;
    text-decoration: none;
    padding: 9px 18px; border-radius: 999px;
    color: #fff; border: 1px solid rgba(255,255,255,0.45);
    background: rgba(255,255,255,0.06);
    transition: background 0.15s ease, color 0.15s ease;
  }}
  a.btn:hover {{ background: rgba(255,255,255,0.18); }}
  a.btn.primary {{ background: rgba(255,255,255,0.92); color: #2a0f52; border-color: transparent; }}
  a.btn.primary:hover {{ background: #fff; }}
  .unbuilt {{ color: rgba(243,240,251,0.6); font-style: italic; }}

  footer {{
    margin-top: 30px; text-align: center;
    color: rgba(243,240,251,0.7); font-size: 14px;
  }}
  footer a {{ color: #fff; text-decoration: underline; text-underline-offset: 3px; }}
</style>
</head>
<body>
  <div class="wrap">
    <header class="masthead">
      <h1>Talks</h1>
      <p>Chris Burr &middot; CERN / LHCb</p>
    </header>
    <ul class="decks">
{body}
    </ul>
    <footer>Built with <a href="https://marp.app/">Marp</a> &middot; {count}</footer>
  </div>
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

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
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "theme" / "assets"
# Old / external talks not built in this repo (PDF + Indico links only).
EXTERNAL_TALKS = ROOT / "external-talks.json"
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


def _parse_repo(remote_url: str) -> str | None:
    """owner/repo from a git remote URL (ssh or https)."""
    url = remote_url.strip().removesuffix(".git")
    m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+)$", url)
    return m.group(1) if m else None


def github_base() -> str | None:
    """Base GitHub URL for this repo (e.g. https://github.com/owner/repo).

    Prefers CI's GITHUB_REPOSITORY, else the local git remote; None if neither
    is available, in which case "Source" links are simply omitted.
    """
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        try:
            out = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            repo = _parse_repo(out)
        except Exception:
            repo = None
    return f"{server}/{repo}" if repo else None


GITHUB_BASE = github_base()


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


def external_talks() -> list[dict]:
    """Old / external talks from external-talks.json (PDF + Indico links only)."""
    if not EXTERNAL_TALKS.exists():
        return []
    try:
        items = json.loads(EXTERNAL_TALKS.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"  !! could not read {EXTERNAL_TALKS.name}: {exc}")
        return []
    out = []
    for it in items:
        date = coerce_date(it.get("date", ""))
        out.append(
            {
                "kind": "external",
                "slug": "",
                "title": it.get("title") or "Untitled",
                "description": it.get("description", ""),
                "date": date,
                "date_str": date.strftime("%-d %B %Y") if date else "",
                "event_url": (it.get("event_url") or "").strip(),
                "pdf": (it.get("pdf") or "").strip() or None,
                "html": None,
            }
        )
    return out


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
                "kind": "local",
                "slug": d.name,
                "title": fm.get("title") or d.name,
                "description": fm.get("description", ""),
                "date": date,
                "date_str": date.strftime("%-d %B %Y") if date else "",
                # Link to the deck directory (served by its index.html) for a clean URL.
                "html": f"{d.name}/" if (d / "index.html").exists() else None,
                "pdf": f"{d.name}/slides.pdf" if (d / "slides.pdf").exists() else None,
                "event_url": fm.get("event_url", "").strip(),
            }
        )
    decks.extend(external_talks())
    # reverse date order; undated decks sort to the bottom
    decks.sort(key=lambda x: (x["date"] or datetime.date.min), reverse=True)
    return decks


ARROW = "&#8599;"  # ↗ external-link indicator


def _event_label(url: str) -> str:
    return "Indico" if "indico." in url else "Event"


def render_local(deck: dict, title: str, desc: str, date_str: str) -> str:
    btns = []
    if deck["html"]:
        btns.append(f'<a class="btn primary" href="{html.escape(deck["html"])}">View&nbsp;slides</a>')
    if deck["pdf"]:
        btns.append(f'<a class="btn" href="{html.escape(deck["pdf"])}">PDF</a>')
    if not btns:
        btns.append('<span class="unbuilt">not built yet</span>')

    refs = []
    if deck["event_url"]:
        url = html.escape(deck["event_url"])
        refs.append(f'<a class="reflink" href="{url}" target="_blank" rel="noopener">{_event_label(deck["event_url"])}&nbsp;{ARROW}</a>')
    if GITHUB_BASE and deck["slug"]:
        src = f'{html.escape(GITHUB_BASE)}/tree/main/{html.escape(deck["slug"])}'
        refs.append(f'<a class="reflink" href="{src}" target="_blank" rel="noopener">Source&nbsp;{ARROW}</a>')
    refs_html = f'<span class="reflinks">{"".join(refs)}</span>' if refs else ""

    return f"""      <li class="card">
        <div class="meta">{date_str}</div>
        <h2>{title}</h2>
        {f'<p class="desc">{desc}</p>' if desc else ''}
        <div class="links">{''.join(btns)}{refs_html}</div>
      </li>"""


def render_external(deck: dict, title: str, desc: str, date_str: str) -> str:
    # The whole card is a link to the primary external page; a stretched <a>
    # overlay makes it clickable, with any extra link sitting above it.
    primary = deck["event_url"] or deck["pdf"] or "#"
    tag = _event_label(deck["event_url"]) if deck["event_url"] else "External"
    meta = f"{date_str} &middot; {tag}" if date_str else tag
    # A direct PDF in addition to the event page rides above the card overlay.
    extra = ""
    if deck["pdf"] and deck["event_url"]:
        extra = (f'<div class="links"><a class="reflink ontop" href="{html.escape(deck["pdf"])}" '
                 f'target="_blank" rel="noopener">PDF&nbsp;{ARROW}</a></div>')
    return f"""      <li class="card external">
        <a class="stretched" href="{html.escape(primary)}" target="_blank" rel="noopener" aria-label="{title} (opens externally)"></a>
        <span class="ext-arrow">{ARROW}</span>
        <div class="meta">{meta}</div>
        <h2>{title}</h2>
        {f'<p class="desc">{desc}</p>' if desc else ''}
        {extra}
      </li>"""


def render(decks: list[dict]) -> str:
    cards = []
    for deck in decks:
        title = html.escape(deck["title"])
        desc = html.escape(deck["description"])
        date_str = html.escape(deck["date_str"]).upper()
        if deck["kind"] == "external":
            cards.append(render_external(deck, title, desc, date_str))
        else:
            cards.append(render_local(deck, title, desc, date_str))
    body = "\n".join(cards) if cards else '      <li class="card empty">No presentations built yet.</li>'
    count = f"{len(decks)} talk{'s' if len(decks) != 1 else ''}"

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

  /* Secondary reference links (Indico / Source), pushed to the right */
  .reflinks {{ margin-left: auto; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }}
  a.reflink {{
    font-size: 14px; text-decoration: none; white-space: nowrap;
    color: rgba(243,240,251,0.82);
    border-bottom: 1px solid rgba(255,255,255,0.28); padding-bottom: 1px;
  }}
  a.reflink:hover {{ color: #fff; border-bottom-color: #fff; }}

  /* External talks — the whole card is a link (stretched overlay) */
  .card.external {{ position: relative; }}
  .card.external h2 {{ margin-top: 4px; padding-right: 28px; }}
  a.stretched {{ position: absolute; inset: 0; border-radius: inherit; z-index: 0; }}
  .card.external .ext-arrow {{
    position: absolute; top: 22px; right: 26px; z-index: 1;
    font-size: 22px; line-height: 1; color: rgba(243,240,251,0.85);
  }}
  .card.external:hover .ext-arrow {{ color: #fff; }}
  .card.external .meta, .card.external h2, .card.external .desc {{ position: relative; z-index: 1; pointer-events: none; }}
  .card.external a.ontop {{ position: relative; z-index: 1; }}  /* clickable over the overlay */

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

#!/usr/bin/env python3
"""Scaffold a new presentation folder: NAME/slides.md + NAME/README.md + NAME/assets/.

The README is a generic per-deck landing page (what the talk is, where to view
it, how to build it) — the index website links straight to each deck's folder.

Usage: python scripts/new_presentation.py 2026-07-01-my-talk
Invoked by `pixi run new NAME`.
"""
from __future__ import annotations

import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGOS = ("lhcb-logo.png", "cern-logo.png")

TEMPLATE = """\
---
marp: true
theme: cburr
paginate: true
title: "{title}"
subtitle: ""
author: "Chris Burr"
affiliation: "CERN"
event: ""
event_url: ""
date: "{date}"
description: ""
---

<!-- The title slide is generated automatically from the front-matter above
     (title / subtitle / author / affiliation / event / date). Just start
     writing slides. -->

<!-- _class: section -->

# Section title

---

# Slide title

➤ bullets are written as plain markdown list items.

- First point, always a full sentence.
- Second point, with a **Label:** prefix for parallel structure.
"""


def title_from_name(name: str) -> str:
    """`2026-07-01-my-talk` -> `My talk` (drop a leading ISO date)."""
    stem = Path(name).name
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}[-_]?", "", stem)
    words = stem.replace("-", " ").replace("_", " ").strip()
    return words[:1].upper() + words[1:] if words else stem


def date_from_name(name: str) -> datetime.date:
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", Path(name).name)
    if m:
        try:
            return datetime.date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            pass
    return datetime.date.today()


def repo_slug() -> str | None:
    """`owner/repo` from CI's GITHUB_REPOSITORY or the git remote; None if
    neither is available (README links then fall back to relative pointers)."""
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        try:
            out = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout
            url = out.strip().removesuffix(".git")
            m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+)$", url)
            repo = m.group(1) if m else None
        except Exception:
            repo = None
    return repo


def deck_urls(slug: str) -> dict[str, str] | None:
    """Public URLs for a deck: its rendered page + PDF on GitHub Pages, and the
    talks index. Derived from the repo slug so this tracks the actual remote."""
    repo = repo_slug()
    if not repo:
        return None
    owner, _, name = repo.partition("/")
    host = f"https://{owner}.github.io"
    # A `<owner>.github.io` repo is served at the host root; others under /repo/.
    base = host if name.lower() == f"{owner.lower()}.github.io" else f"{host}/{name}"
    return {
        "pages": f"{base}/{slug}/",
        "pdf": f"{base}/{slug}/slides.pdf",
        "index": f"{base}/",
    }


def readme_text(
    slug: str, title: str, event: str, event_url: str, date_str: str,
    urls: dict[str, str] | None,
) -> str:
    """A generic per-deck README for the folder we link to from the website —
    what the talk is, where to view it, and how to build it locally."""
    where = " · ".join(x for x in (event, date_str) if x)
    out = [f"# {title}", ""]
    if where:
        out += [f"*{where}*", ""]
    out += [
        "Source for one of **Chris Burr**'s talks (CERN / LHCb) — a single slide",
        "deck written in Markdown and built with [Marp](https://marp.app/).",
        "",
        "## View the talk",
        "",
    ]
    if urls:
        out += [f"- **Slides:** <{urls['pages']}>", f"- **PDF:** <{urls['pdf']}>"]
    if event_url:
        out.append(f"- **Event page:** <{event_url}>")
    if urls:
        out.append(f"- **All talks:** <{urls['index']}>")
    out += [
        "",
        "The rendered links go live once the deck is built and deployed to GitHub",
        "Pages (automatic on every push to `main`).",
        "",
        "## What's in this folder",
        "",
        "- `slides.md` — the deck: YAML front-matter followed by Markdown slides.",
        "- `assets/` — images and logos this deck embeds.",
        "",
        "The title slide, kicker, footer and progressive reveals are generated from",
        "the front-matter by a custom Marp engine, so the Markdown stays clean.",
        "",
        "## Build or edit it locally",
        "",
        "Everything runs through [pixi](https://pixi.sh):",
        "",
        "```bash",
        "pixi install         # one-time toolchain setup",
        f"pixi run dev {slug}  # live preview (watch + server)",
        "pixi run build       # build every deck to HTML + PDF",
        "```",
        "",
        "See the [repository README](../README.md) for full setup and how the",
        "**cburr** theme and engine work.",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: new_presentation.py NAME", file=sys.stderr)
        return 2

    name = sys.argv[1].rstrip("/")
    folder = Path(name)
    slides = folder / "slides.md"
    if slides.exists():
        print(f"refusing to overwrite existing {slides}", file=sys.stderr)
        return 1

    assets = folder / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    # Logos live with each deck so the built HTML/PDF are self-contained.
    for logo in LOGOS:
        src = ROOT / "theme" / "assets" / logo
        if src.exists():
            shutil.copy2(src, assets / logo)

    title = title_from_name(name)
    d = date_from_name(name)
    slides.write_text(TEMPLATE.format(title=title, date=d.isoformat()))

    # A generic README for the folder — the website links people straight here.
    # event/event_url are blank in a fresh scaffold; fill them in slides.md.
    readme = folder / "README.md"
    readme.write_text(
        readme_text(
            slug=folder.name, title=title, event="", event_url="",
            date_str=d.strftime("%-d %B %Y"), urls=deck_urls(folder.name),
        )
    )

    print(f"created {slides}")
    print(f"created {readme}")
    print(f"  -> edit it, then: pixi run dev {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

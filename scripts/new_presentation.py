#!/usr/bin/env python3
"""Scaffold a new presentation folder: NAME/slides.md + NAME/assets/.

Usage: python scripts/new_presentation.py 2026-07-01-my-talk
Invoked by `pixi run new NAME`.
"""
from __future__ import annotations

import datetime
import re
import shutil
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
    print(f"created {slides}")
    print(f"  -> edit it, then: pixi run dev {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

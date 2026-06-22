#!/usr/bin/env python3
"""Build every presentation deck to HTML and PDF, in place.

Finds each immediate subdirectory containing a `slides.md` (excluding
reference/, scripts/, theme/, node_modules/ and dotted dirs) and runs
marp-cli twice per deck: once for HTML, once for PDF. Outputs sit
alongside the source slides.md. Invoked by `pixi run build`.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {"reference", "scripts", "theme", "node_modules", "assets"}

COMMON = ["--theme-set", "./theme/", "--html", "--allow-local-files"]


def marp_cmd() -> list[str]:
    """Prefer the locally-installed binary, fall back to npx."""
    local = ROOT / "node_modules" / ".bin" / "marp"
    if local.exists():
        return [str(local)]
    return ["npx", "marp"]


def find_decks() -> list[Path]:
    decks = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if d.name in EXCLUDE or d.name.startswith("."):
            continue
        if (d / "slides.md").exists():
            decks.append(d)
    return decks


def run(cmd: list[str]) -> None:
    print("    $", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    decks = find_decks()
    if not decks:
        print("no decks found (looked for */slides.md)")
        return 0

    if shutil.which("marp") is None and not (ROOT / "node_modules/.bin/marp").exists():
        print("marp-cli not found — run `pixi run _install` first", file=sys.stderr)
        return 1

    marp = marp_cmd()
    failures = []
    for deck in decks:
        src = str((deck / "slides.md").relative_to(ROOT))
        # Build the deck to index.html so the bare directory URL (…/deck/)
        # serves it on GitHub Pages; the PDF stays slides.pdf.
        html = str((deck / "index.html").relative_to(ROOT))
        pdf = str((deck / "slides.pdf").relative_to(ROOT))
        print(f"==> {deck.name}")
        try:
            run([*marp, src, *COMMON, "-o", html])
            run([*marp, src, *COMMON, "--pdf", "-o", pdf])
        except subprocess.CalledProcessError as exc:
            print(f"    !! failed ({exc.returncode})", file=sys.stderr)
            failures.append(deck.name)

    print()
    print(f"built {len(decks) - len(failures)}/{len(decks)} deck(s)")
    if failures:
        print("failed:", ", ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # PDF export needs Chrome/Chromium; honour CHROME_PATH if the
    # environment set one (CI installs Chromium and exports it).
    os.environ.setdefault("PUPPETEER_SKIP_DOWNLOAD", "true")
    raise SystemExit(main())

---
name: implement-slide-comments
description: Implement the HTML comment notes (<!-- ... -->) left in a Marp slides.md deck in this presentations repo. Use when Chris says things like "implement the comments", "take care of the comments in the deck", "fix the comments in the <talk> slides", or "look for comments to implement". Turns terse authoring notes — screenshots, comics, footnotes, links, draft bullets — into real slide content using the cburr theme's components.
---

# Implement slide comments

Chris drafts decks by leaving `<!-- … -->` notes describing what a slide still
needs. This skill turns those into finished slide content. Read `CLAUDE.md` first
for the theme's layouts, components, and his style — this skill assumes them.

## 1. Find the comments

```bash
grep -nE '<!--' DECK/slides.md | grep -v '_class'
```

`<!-- _class: … -->` are layout directives, **not** TODOs — skip them. Everything
else is a note to implement. Also look for obvious stubs (a lone `- ` bullet, an
empty `<!--  -->`, trailing note fragments under a heading).

## 2. Implement each, by type

- **"Screenshot of X" / "with a link and caption"** → produce the image and place
  it in `DECK/assets/`, then a `<figure>` with a linked `<figcaption>`.
  - PDF page → `pixi run pdftoppm -png -f N -l N -r 150 ~/Downloads/file.pdf /tmp/out`
    (Chris drops the source PDF in `~/Downloads`; confirm the right page with
    `Read` on the PDF `pages:` first). The output is `…-N.png`.
  - Public web page → headless Chrome screenshot (`--headless=new
    --window-size=W,H --virtual-time-budget=12000 --screenshot=…`); crop to a
    landscape ratio that suits the slide by choosing the window size.
  - Auth-walled and no file available → make a labelled placeholder PNG at the
    final filename and leave a `<!-- TODO: replace … -->`.
  - If the note says "with a link in the bullet above", also hyperlink that bullet.

- **"Relevant comic?" / "xkcd …"** → fetch from xkcd, two-column (bullets left,
  comic right) with an xkcd `.src` credit. Get the exact image + title from the
  JSON API and download:
  ```bash
  curl -s https://xkcd.com/1654/info.0.json     # → .img and .title
  curl -s -o DECK/assets/xkcd-1654-name.png https://imgs.xkcd.com/comics/<slug>.png
  ```
  **If the note says "ask me" or several comics fit, ASK which one** (Chris likes
  to choose) — use AskUserQuestion with the candidates and your recommendation.

- **"Add a footnote: …"** → `<sup>*</sup>` on the text + a `<div class="footnotes">
  <div class="footnote">* …</div></div>` block. Markers run `*`, `†`, `‡`. On a
  `build` slide, placing the footnote after the relevant group ties it to that
  reveal step.

- **"Add links to …"** → short labelled links on one line, matching the
  `[ripgrep](…), [htop](…)` style. **Verify each URL resolves** (`curl -sI -L`);
  prefer authoritative/stable pages; swap dead ones.

- **Note fragments under a heading** (e.g. "lb-stack-setup works for X", "if you
  want a different Y") → turn into proper bullets, keeping links. Where a
  fragment is genuinely ambiguous, draft a sensible version and flag it for him
  rather than guessing silently.

## 3. After implementing

- Replace the implemented comment (delete it, or leave only a `TODO` if you were
  blocked, e.g. a placeholder image).
- Keep assets local to the deck (self-containment — see CLAUDE.md).
- `pixi run build`, render the affected slides to PNG, and **look at them**;
  clean up `/tmp` renders.
- Report what you implemented, and surface any placeholders/ambiguities you left.

## Boundaries

- Only act on comments (and obvious stubs). **Don't** rewrite or "improve"
  surrounding content that wasn't flagged — mention it separately if something
  looks off.
- Respect his style: fragment bullets and emoji are intentional; gold is
  links-only; bold `Label:` prefixes; real product-name casing in prose.

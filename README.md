# Presentations

Chris Burr's talk decks, written in Markdown and built with [Marp](https://marp.app/) using the **cburr** theme.

## Layout

```
pixi.toml             tasks + node/python toolchain
.marprc.yml           registers ./theme/ for local dev
theme/
  cburr.css           the Marp theme (fonts + masthead embedded as data URIs)
  fonts/  assets/      source fonts, masthead, logos
scripts/
  build.py            build every deck -> HTML + PDF
  build_index.py      generate index.html
  new_presentation.py scaffold a new deck
YYYY-MM-DD-name/
  slides.md           one deck (front-matter + slides)
  assets/             deck-local images (+ copied logos for the title slide)
reference/            the source design system (not built or deployed)
```

## Usage

```bash
pixi install                       # one-time toolchain setup
pixi run new 2026-07-01-my-talk     # scaffold a new deck
pixi run dev 2026-07-01-my-talk     # live preview (watch + server)
pixi run build                      # build every deck to HTML + PDF
pixi run index                      # regenerate index.html
```

`pixi run build` and `pixi run index` also run automatically on every push to
`main` (see `.github/workflows/deploy.yml`), which publishes `index.html` and
all presentation folders to GitHub Pages.

## Editing in VS Code

`.vscode/settings.json` registers the cburr theme so the **Marp for VS Code**
preview is styled correctly. That extension runs its own Marp, though, and
**can't run our engine** (`scripts/marp-engine.mjs`) — so its built-in preview
won't show the generated title slide, kicker, or footer.

For a faithful, live-reloading preview, drive the dev server from inside VS Code:

1. Open a deck's `slides.md`, then start the server — **`ctrl+alt+m`** (or
   *Tasks: Run Task → Marp: dev server*). It serves the active file's deck.
2. Open the preview — **`ctrl+alt+p`** (or *Simple Browser: Show* →
   `http://localhost:8080/slides.md`); dock it beside the editor.

The Simple Browser reloads on every save and shows the full generated
cover / kicker / footer. The extension's own preview is still handy for a quick
structural glance.

> Tasks live in `.vscode/tasks.json` (also *Marp: build all* and *Marp: rebuild
> index*); the two keybindings are in your user `keybindings.json`.

## Supply chain

The build only trusts what's pinned, and only after it has had time to be
vetted:

- **Lockfiles are authoritative.** `pixi.lock` pins the node/python toolchain;
  `package-lock.json` pins the full marp dependency tree. The `_install` task
  runs `npm ci`, which installs exactly the lock and refuses to drift from it.
  Commit lockfile changes alongside the `package.json` / `pixi.toml` change that
  caused them.
- **7-day cooldown.** `.npmrc` sets `min-release-age=7`, so npm never installs a
  version published less than a week ago (including transitive deps) — long
  enough for most malicious releases to be caught and yanked.
  [`renovate.json`](renovate.json) applies the same `minimumReleaseAge` when it
  opens update PRs for npm, pixi, and the pinned GitHub Actions.
- **Actions are pinned to commit SHAs** (with a `# vX` comment) and the deploy
  pipeline runs least-privilege: only the `deploy` job gets `pages: write` /
  `id-token: write`. Renovate keeps the SHAs current.
- **Enable Renovate** by installing the Renovate GitHub App on the repo (free
  for public repos); it opens an onboarding PR. Prefer not to grant an external
  app? Self-host a SHA-pinned `renovatebot/github-action` on a schedule instead.
- **Urgent override.** To take a fix younger than the cooldown, merge its
  Renovate PR early, or temporarily lower `min-release-age` for a single
  `npm install`.

## Writing slides

Slides are Markdown, separated by `---`. The front matter drives the theme and
the auto-generated bits — you don't hand-write the cover slide or footer:

```yaml
---
marp: true
theme: cburr
paginate: true
title: "Towards a new file format"   # cover title + footer + <title>
subtitle: ""                          # optional one-liner under the title
author: "Chris Burr"                  # cover author (defaults to Chris Burr)
affiliation: "CERN"                   # e.g. "CERN · on behalf of the LHCb collaboration"
event: "LHCb Week"                    # cover kicker, with the date
date: "2026-06-22"                    # ISO date → formatted; also the kicker
---
```

From that front matter the engine (`scripts/marp-engine.mjs`) generates, with
no markup in the deck:

- a **title slide** (masthead, kicker, title, subtitle, author, affiliation,
  image credit, logos) prepended as slide 1;
- the **kicker** eyebrow line — `event · date`, or just `date` if no event;
- the **footer** on every other slide — `email ○ title` (set `email:` to
  override; `footer:` still wins if you'd rather write it yourself).

Then write your content slides, applying a layout with a class directive:

| Directive                          | Layout                                    |
| ---------------------------------- | ----------------------------------------- |
| _(none)_                           | content slide: title pill + ➤ bullets     |
| `<!-- _class: section -->`         | section divider (centred card on the image)|
| `<!-- _class: code -->`            | code-heavy slide (tuned `<pre>` / TES list)|
| `<!-- _class: comparison -->`      | two-column Pros/Cons                       |
| `<!-- _class: diagram -->`         | schematic event grid                       |

The first `# Heading` on a content slide becomes the title pill; bullets are
plain Markdown lists (rendered as ➤). A hand-written `<!-- _class: title -->`
first slide is left untouched if you ever need to override the generated cover.

A Markdown blockquote renders as a **pull-quote** — bold grey text framed by
soft-purple 66/99 marks. Add an attribution with a trailing `<cite>`:

```markdown
> Looking back at your PyHEP 2019 conda-forge talk… <cite>Eduardo Rodrigues, PyHEP 2026</cite>
```

A `<figure>` is a **screenshot / image with caption** — drop the image in the
deck's `assets/`, and it auto-fits the body space left by any bullets or quote
above it:

```html
<figure>
  <img src="assets/my-screenshot.png" alt="…">
  <figcaption>From <a href="https://…">source</a> (slide 20)</figcaption>
</figure>
```

`<!-- _class: build -->` turns a bulleted slide into a **progressive reveal** —
the engine splits it into one slide per top-level bullet. Each step shows every
group in the same place (nothing reflows): earlier groups dim to 40%, the
current group is full, later groups are hidden but keep their space. Author the
slide once:

```markdown
<!-- _class: build -->
# How does it help LHCb?

- From one perspective LHCb has solved this problem
  - Install software on CVMFS
- But this is a very specific solution to a very specific problem
  - How do I put the software on CVMFS?
```

Each step is its own page (the slide number increments). Needs two or more
top-level bullets; with fewer, the slide renders normally.

An `<img class="overlay …">` floats a **small logo / accent** over the body
without reflowing any text (it's absolutely positioned). Position it with a
corner modifier — `t`/`b` (top/bottom) × `l`/`m`/`r` (left/middle/right):

```html
<img class="overlay tr" src="assets/pixi.png" alt="Pixi">
```

Resize with an inline `height` or `style="--overlay-h: 130px"`. The Pixi logo
lives in `theme/assets/pixi.png` — copy it into a deck's `assets/` to use it.

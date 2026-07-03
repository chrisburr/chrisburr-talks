# Conda, Pixi and RattlerFS

*LHCb Week · 22 June 2026*

Source for one of **Chris Burr**'s talks (CERN / LHCb) — a single slide
deck written in Markdown and built with [Marp](https://marp.app/).

## View the talk

- **Slides:** <https://chrisburr.github.io/chrisburr-talks/2026-06-22-pixi-and-rattlerfs/>
- **PDF:** <https://chrisburr.github.io/chrisburr-talks/2026-06-22-pixi-and-rattlerfs/slides.pdf>
- **Event page:** <https://indico.cern.ch/event/1696907/contributions/7143130/>
- **All talks:** <https://chrisburr.github.io/chrisburr-talks/>

The rendered links go live once the deck is built and deployed to GitHub
Pages (automatic on every push to `main`).

## What's in this folder

- `slides.md` — the deck: YAML front-matter followed by Markdown slides.
- `assets/` — images and logos this deck embeds.

The title slide, kicker, footer and progressive reveals are generated from
the front-matter by a custom Marp engine, so the Markdown stays clean.

## Build or edit it locally

Everything runs through [pixi](https://pixi.sh):

```bash
pixi install         # one-time toolchain setup
pixi run dev 2026-06-22-pixi-and-rattlerfs  # live preview (watch + server)
pixi run build       # build every deck to HTML + PDF
```

See the [repository README](../README.md) for full setup and how the
**cburr** theme and engine work.

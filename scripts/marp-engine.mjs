// Custom Marp engine for the cburr theme. Referenced from .marprc.yml via
// `engine:`, so it applies to both `build` and `dev`. Everything below is
// derived from front-matter so decks don't repeat themselves:
//
// 1. Title slide — generated in full from front-matter when the deck doesn't
//    already start with one. Just write:
//      title: "…"   author: "…"   affiliation: "…"   subtitle: "…"   (+ event/date)
//    and the cover slide (masthead, kicker, title, subtitle, author,
//    affiliation, image credit, logos) is built for you. A hand-written
//    `<!-- _class: title -->` first slide is left untouched.
//
// 2. Title-slide kicker (the uppercase eyebrow line):
//      event: "CHEP 2026"  +  date: "2026-05-28"  ->  CHEP 2026 · 28 May 2026
//      (no event)                                 ->  28 May 2026
//
// 3. Footer composed as `email ○ title`:
//      title: "Towards a new file format"  ->  …@cern.ch ○ Towards a new …
//    Skipped if `footer:` is set explicitly; per-slide `_footer: ""`
//    (e.g. the title slide) still wins.
//
// 4. Progressive reveal — `<!-- _class: build -->` on a bulleted slide expands
//    it into one slide per top-level bullet. Each step shows all groups in the
//    same place (so nothing reflows): earlier groups dimmed, the current group
//    full, later groups hidden-but-space-reserved. Author the slide once; the
//    steps are generated. Theme handles the .is-faded / .is-hidden styling.

import { Marp } from '@marp-team/marp-core'

// Defaults for the generated title slide; override per deck with the matching
// front-matter key (email:, author:, affiliation:).
const DEFAULT_EMAIL = 'christopher.burr@cern.ch'
const DEFAULT_AUTHOR = 'Chris Burr'
const DEFAULT_AFFILIATION = 'CERN'

// Minimal flat front-matter reader — we only need scalar string values.
function readFrontMatter(yaml) {
  const out = {}
  for (const line of (yaml || '').split('\n')) {
    const m = /^([A-Za-z0-9_-]+)\s*:\s*(.*)$/.exec(line)
    if (m) out[m[1]] = m[2].trim().replace(/^['"]|['"]$/g, '')
  }
  return out
}

// ISO `YYYY-MM-DD` -> `3 June 2026`; anything else passes through verbatim
// (so `date: "Spring 2026"` works too).
function formatDate(value) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value || '')
  if (!m) return value || ''
  const dt = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]))
  return dt.toLocaleDateString('en-GB', {
    day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC',
  })
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

// Markdown for a generated cover slide (the kicker is added later, by the
// kicker rule, since this slide carries `_class: title`).
function buildTitleSlide(fm) {
  const author = fm.author || DEFAULT_AUTHOR
  const affiliation = fm.affiliation || DEFAULT_AFFILIATION
  const subtitle = (fm.subtitle || '').trim()
  // Optional extra cover logos, sat after the default LHCb + CERN marks (e.g.
  // co-presenting institutions on a joint talk). Front-matter is scalar-only,
  // so list them comma-separated, each as `path` or `path|Alt text`:
  //   extra_logos: "assets/uw-logo.png|UW, assets/iris-hep-logo.png|IRIS-HEP"
  const extraLogos = (fm.extra_logos || '')
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
    .map((entry) => {
      const [src, alt = ''] = entry.split('|').map((s) => s.trim())
      return `  <img class="extra" src="${src}" alt="${escapeHtml(alt)}">`
    })
  return [
    '<!-- _class: title -->',
    '<!-- _paginate: false -->',
    '<!-- _footer: "" -->',
    '',
    `# ${fm.title}`,
    '',
    ...(subtitle ? [`<p class="subtitle">${subtitle}</p>`, ''] : []),
    `<div class="author">${escapeHtml(author)}</div>`,
    `<div class="affiliation">${escapeHtml(affiliation)}</div>`,
    '',
    '<p class="credit">Image: <a href="https://cds.cern.ch/record/39312">CERN-EX-66954B</a> &copy; 1998&ndash;2026 CERN</p>',
    '<div class="logos">',
    '  <img class="lhcb" src="assets/lhcb-logo.png" alt="LHCb">',
    '  <img class="cern" src="assets/cern-logo.png" alt="CERN">',
    ...extraLogos,
    '</div>',
  ].join('\n')
}

// Expand one `<!-- _class: build -->` slide into N progressive-reveal steps,
// one per top-level bullet. Every step renders ALL groups (so layout is frozen);
// only their reveal state differs. Returns the slide unchanged if it has fewer
// than two top-level bullets (nothing to reveal incrementally).
function buildSteps(slide) {
  const lines = slide.split('\n')
  const isTop = (l) => /^(?:[-*+]|\d+[.)])\s+/.test(l) // top-level bullet or `1.` number (column 0)

  const first = lines.findIndex(isTop)
  if (first < 0) return slide

  // Group boundaries: each top-level bullet starts a group that runs to the
  // next top-level bullet (or the end of the slide).
  const starts = lines.map((l, i) => (isTop(l) ? i : -1)).filter((i) => i >= 0)
  if (starts.length < 2) return slide

  const preamble = lines.slice(0, first).join('\n').replace(/\s+$/, '')
  const groups = starts.map((s, gi) => {
    const end = gi + 1 < starts.length ? starts[gi + 1] : lines.length
    const slice = lines.slice(s, end)
    // Each group renders as its own list, so an ordered list would restart at 1
    // in every group — renumber the leading marker to the group's position so
    // the numbers stay 1, 2, 3… across reveal steps. (No-op for `-`/`*`/`+`.)
    slice[0] = slice[0].replace(/^(\d+)([.)])/, `${gi + 1}$2`)
    return slice.join('\n').replace(/\s+$/, '')
  })

  const N = groups.length
  const steps = []
  for (let step = 1; step <= N; step++) {
    const blocks = groups.map((g, gi) => {
      const i = gi + 1 // 1-based group index
      const state = i < step ? ' is-faded' : i > step ? ' is-hidden' : ''
      return `<div class="reveal-group${state}">\n\n${g}\n\n</div>`
    })
    steps.push(`${preamble}\n\n${blocks.join('\n\n')}\n`)
  }
  return steps.join('\n---\n')
}

// Expand every build slide in the deck body; pass others through untouched.
function expandBuildSlides(body) {
  return body
    .split(/^---\s*$/m)
    .map((slide) => (/_class\s*:\s*build\b/.test(slide) ? buildSteps(slide) : slide))
    .join('\n---\n')
}

function cburrPlugin(md) {
  // Runs before Marp parses directives, editing the raw source so the rest of
  // Marp's machinery (footer rendering, slide splitting) treats the results as
  // hand-authored. Two jobs: (a) compose the `email ○ title` footer directive,
  // (b) prepend a generated title slide when the deck doesn't start with one.
  md.core.ruler.before('marpit_directives_front_matter', 'cburr_frontmatter', (state) => {
    const m = /^(---\r?\n)([\s\S]*?)(\r?\n---\r?\n?)/.exec(state.src)
    if (!m) return false
    const fm = readFrontMatter(m[2])
    if (!fm.title) return false
    const body = state.src.slice(m[0].length)

    // (a) footer — unless one was written explicitly.
    let yaml = m[2]
    if (fm.footer === undefined) {
      const email = fm.email || DEFAULT_EMAIL
      const value = `${email} <span class="sep">○</span> ${fm.title}`.replace(/'/g, "''")
      yaml += `\nfooter: '${value}'`
    }

    // (b) title slide — unless the deck already opens with one.
    const firstChunk = body.split(/\r?\n---\r?\n/, 1)[0]
    const cover = /_class\s*:\s*title/.test(firstChunk)
      ? ''
      : `\n${buildTitleSlide(fm)}\n\n---\n`

    // (c) progressive-reveal: expand any `_class: build` slides into steps.
    state.src = m[1] + yaml + m[3] + cover + expandBuildSlides(body)
    return false
  })

  md.core.ruler.push('cburr_kicker', (state) => {
    const tokens = state.tokens

    const fm = tokens.find((t) => t.type === 'front_matter')
    if (!fm) return false
    const meta = readFrontMatter(fm.meta)
    const event = (meta.event || '').trim()
    const date = formatDate((meta.date || '').trim())
    if (!event && !date) return false
    const text = event && date ? `${event} · ${date}` : event || date

    // Bound the first slide.
    const open = tokens.findIndex((t) => t.type === 'marpit_slide_open')
    if (open < 0) return false
    const close = tokens.findIndex(
      (t, i) => i > open && t.type === 'marpit_slide_close',
    )
    const body = tokens.slice(open, close < 0 ? undefined : close)

    // Only on a title slide…
    const isTitle = body.some(
      (t) =>
        t.type === 'marpit_comment' &&
        /(^|\s)title(\s|$)/.test(t.meta?.marpitParsedDirectives?._class || ''),
    )
    if (!isTitle) return false

    // …and never clobber a hand-written kicker.
    const hasKicker = body.some(
      (t) =>
        t.type === 'html_block' && /class=["'][^"']*\bkicker\b/.test(t.content),
    )
    if (hasKicker) return false

    const tok = new state.Token('html_block', '', 0)
    tok.content = `<p class="kicker">${escapeHtml(text)}</p>\n`
    tok.block = true
    tokens.splice(open + 1, 0, tok)
    return false
  })
}

// Functional engine: marp-cli hands us the constructor options.
export default (opts) => new Marp(opts).use(cburrPlugin)

---
marp: true
theme: cburr
paginate: true
title: "The DiracX Transformation System"
subtitle: "What we are building, and what we need from you"
author: "Chris Burr & Christophe Haen"
affiliation: "CERN"
event: "DIRAC Users' Workshop 2026"
event_url: ""
date: "2026-10-12"
description: "Monday session: the approved Transformation System ADRs, where they lead (Analysis Productions for everyone), and the questions for building on them."
---

<!-- Deck-local styling, copied from 2026-07-01-diracx-transformation-system so
     the flow diagrams keep the same visual language. -->
<style>
/* ---------- Flow diagrams (inline `<svg class="flow">`) ----------
   A small visual language for the workflow story. COLOUR = IDENTITY: simulate
   (blue), reconstruct (orange), merge (green), generic payload (purple). Wrap a
   node in a <g> carrying a c-* class — it sets --c (border/label) and --cf
   (tint fill); children read those. SHAPE = ROLE: .step / .payload solid box,
   .job dashed box (a runtime container), .tile a Transformation, .container /
   .prod the dashed wrappers (Job / Production). */
section .flow { display: block; width: 100%; height: auto; margin: 0 auto; }

/* identity palette — sets the fill tint (--cf) + line/label colour (--c) */
section .flow .c-sim    { --c: #2D6CDF; --cf: #E6EEFC; }
section .flow .c-reco   { --c: #E8810B; --cf: #FCF0E1; }
section .flow .c-filter { --c: #8B3FA0; --cf: #F1E8F4; }
section .flow .c-merge  { --c: #1F9D55; --cf: #E4F3EB; }
section .flow .c-gen    { --c: #4A1789; --cf: #ECE6F4; }

/* nodes */
section .flow .step, section .flow .payload {
  fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.6;
  filter: drop-shadow(0 2px 3px rgba(74, 23, 137, 0.16));
}
section .flow .tile {
  fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.2;
  filter: drop-shadow(0 2px 3px rgba(74, 23, 137, 0.16));
}
section .flow .job { fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.6; stroke-dasharray: 9 5; }
/* Merged two-step job: two steps (e.g. Reco + Filter) fused into one
   double-width pill, a colour per step, showing they run inside one job. Each
   half is a path that shares the inner edge, so the two strokes there double as
   the divider. .mstep = concrete (solid + shadow); .mjob = abstract protostep
   (dashed, no shadow), mirroring .step vs .job. */
section .flow .mfill { fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.6; }
/* Shadow lives on the wrapping group, not the halves, so only the merged
   pill's outer silhouette casts it — the shared seam stays flat (no inner
   shadow bleeding onto the other half). */
section .flow .mstep-grp { filter: drop-shadow(0 2px 3px rgba(74, 23, 137, 0.16)); }
section .flow .mjob  { fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.6; stroke-dasharray: 9 5; }
section .flow .container { fill: rgba(74, 23, 137, 0.025); stroke: var(--ink); stroke-width: 2.4; stroke-dasharray: 9 6; }
section .flow .prod { fill: rgba(74, 23, 137, 0.02); stroke: var(--ink); stroke-width: 2.6; stroke-dasharray: 8 7; }
section .flow .box-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 20px; fill: var(--c, #4A1789); text-anchor: middle; }
section .flow .step-hdr { font-family: var(--font-sans); font-weight: 700; font-size: 12px; fill: var(--c, #4A1789); text-anchor: middle; opacity: 0.7; }

/* connectors */
section .flow .ln { stroke: var(--ink-soft); stroke-width: 3; fill: none; stroke-linecap: round; }
section .flow .ln.dash { stroke-dasharray: 7 6; }

/* data pills + text labels */
section .flow .pill { fill: #F4F1FA; stroke: rgba(74, 23, 137, 0.30); stroke-width: 1.5; }
section .flow .pill-lbl { font-family: var(--font-sans); font-size: 17px; fill: var(--ink); text-anchor: middle; }
section .flow .node { font-family: var(--font-sans); font-size: 17px; fill: var(--ink); }
section .flow .lbl { font-family: var(--font-mono); font-size: 13px; fill: var(--muted); }
section .flow .job-lbl { font-family: var(--font-mono); font-size: 12px; font-weight: 700; fill: var(--ink); letter-spacing: 0.08em; }
section .flow .prod-lbl { font-family: var(--font-mono); font-size: 14px; font-weight: 700; fill: var(--ink); letter-spacing: 0.12em; }

/* transformation tiles + job-dot clusters */
section .flow .corner { fill: var(--c, #4A1789); }
section .flow .tname { font-family: var(--font-sans); font-weight: 700; font-size: 24px; fill: var(--c, #4A1789); text-anchor: middle; }
section .flow .tsub { font-family: var(--font-sans); font-size: 14px; fill: var(--muted); text-anchor: middle; }
section .flow .count { font-family: var(--font-sans); font-style: italic; font-size: 14px; fill: var(--muted); text-anchor: middle; }
section .flow .dot { fill: var(--c, #6A3FA8); }

/* Transformation grouping box — a solid translucent frame drawn behind the
   steps it owns, with a centred heading in the band above them. */
section .flow .tgroup     { fill: rgba(74, 23, 137, 0.03); stroke: var(--ink-soft); stroke-width: 2; }
section .flow .tgroup-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 16px; fill: var(--ink-soft); text-anchor: middle; }
/* Input plugin + metadata-query store feeding a transformation (teal accent). */
section .flow .plugin     { fill: #E6F4F2; stroke: #138D8D; stroke-width: 2.2; }
section .flow .plugin-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 15px; fill: #0F7A7A; text-anchor: middle; }
/* Per-input annotation above an input arrow: each input (one arrow) is fetched
   by a metadata query and supplied through an input plugin. */
section .flow .io-sed { font-family: var(--font-sans); font-size: 13px; fill: #0F7A7A; text-anchor: middle; }
section .flow .io-lbl { font-family: var(--font-sans); font-size: 13px; fill: #0F7A7A; text-anchor: middle; }
section .flow .io-sub { font-family: var(--font-sans); font-size: 13px; fill: #3D9A9A; text-anchor: middle; }
</style>

# Where Ryun left us

- A **workgraph** is a DAG of **transformations**, written as one CWL document
- Each orange outline is a transformation: one step, run as many jobs
- This talk: what happens *inside* an outline, where it leads, and what we need from you

<svg class="flow" style="max-width: 880px" viewBox="0 40 812 188" role="img" aria-label="A single abstract chain Sim, Reco, Filter, Merge with the transformation and workgraph boxes around it">
  <defs>
    <marker id="ah8" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="prod" x="10" y="58" width="784" height="148" rx="18"/>
  <text class="prod-lbl" x="28" y="80">WORKGRAPH</text>
  <rect class="tgroup" x="28" y="92" width="154" height="92" rx="14"/>
  <text class="tgroup-lbl" x="105" y="110">Transformation 1</text>
  <rect class="tgroup" x="238" y="92" width="334" height="92" rx="14"/>
  <text class="tgroup-lbl" x="405" y="110">Transformation 2</text>
  <rect class="tgroup" x="624" y="92" width="154" height="92" rx="14"/>
  <text class="tgroup-lbl" x="701" y="110">Transformation 3</text>
  <g class="c-sim">
    <rect class="job" x="40" y="120" width="130" height="50" rx="13"/>
    <text class="box-lbl" x="105" y="151">Sim</text>
  </g>
  <line class="ln" x1="170" y1="145" x2="250" y2="145" marker-end="url(#ah8)"/>
  <g class="c-reco">
    <path class="mjob" d="M405,120 L263,120 Q250,120 250,133 L250,157 Q250,170 263,170 L405,170 Z"/>
    <text class="box-lbl" x="328" y="151">Reco</text>
  </g>
  <g class="c-filter">
    <path class="mjob" d="M405,120 L547,120 Q560,120 560,133 L560,157 Q560,170 547,170 L405,170 Z"/>
    <text class="box-lbl" x="482" y="151">Filter</text>
  </g>
  <line class="ln" x1="560" y1="145" x2="636" y2="145" marker-end="url(#ah8)"/>
  <g class="c-merge">
    <rect class="job" x="636" y="120" width="130" height="50" rx="13"/>
    <text class="box-lbl" x="701" y="151">Merge</text>
  </g>
  <line class="ln" x1="766" y1="145" x2="806" y2="145" marker-end="url(#ah8)"/>
</svg>

<!-- TODO(Chris): check the hand-off line matches Ryun's final slide once his edits land. -->

---

# One system instead of three

- The DiracX Transformation System covers what DIRAC split across:
     - the **Transformation System**
     - the **Production System** (now just the workgraph: a table, a roll-up state, some hooks)
     - the **job** part of the WMS: a user job is a parcel too
- Same underpinnings as DIRAC, with twenty years of lessons applied
- Some words change on purpose: **production → workgraph**, **task → parcel**

---

# The approved ADRs

| ADR | What it fixes |
| --- | --- |
| [DX-ADR-002](https://diracx.diracgrid.org/adr/DX-ADR-002_overview/) | The model and the vocabulary (read this one first) |
| DX-ADR-003 | Compute backends and the dispatcher |
| DX-ADR-004 | The database schema |
| DX-ADR-005 | State machines: workgraph, transformation, input, parcel |
| DX-ADR-006 | Extension points: feeders, packers, hooks, actions |
| DX-ADR-007 | CWL: user jobs and workgraphs, the `dirac:` hints |
| DX-ADR-008 / 009 | Data transformations, journalled counters |

<div class="footnotes">
  <div class="footnote">Plus DX-ADR-001 (tasks), which everything above runs on.</div>
</div>

<!-- TODO(Chris): confirm the docs-site URL pattern for the ADR pages once PR 1042 is merged. -->

---

<!-- _class: section -->

# Inside a transformation

---

# The three things a transformation sits between

<svg class="flow" style="max-width: 600px" viewBox="0 0 720 540" role="img" aria-label="A Venn diagram: metadata management, data management and the compute and data backends overlap, and the transformation system sits where all three meet">
  <g style="fill-opacity: 0.22">
    <circle cx="360" cy="200" r="165" fill="#8B3FA0" stroke="#8B3FA0" stroke-width="2.5" stroke-opacity="1"/>
    <circle cx="268" cy="348" r="165" fill="#2D6CDF" stroke="#2D6CDF" stroke-width="2.5" stroke-opacity="1"/>
    <circle cx="452" cy="348" r="165" fill="#1F9D55" stroke="#1F9D55" stroke-width="2.5" stroke-opacity="1"/>
  </g>
  <text class="box-lbl" x="360" y="108" style="fill:#8B3FA0">Metadata</text>
  <text class="box-lbl" x="360" y="134" style="fill:#8B3FA0">management</text>
  <text class="box-lbl" x="205" y="372" style="fill:#2D6CDF">Data</text>
  <text class="box-lbl" x="205" y="398" style="fill:#2D6CDF">management</text>
  <text class="box-lbl" x="515" y="372" style="fill:#1F9D55">Compute / data</text>
  <text class="box-lbl" x="515" y="398" style="fill:#1F9D55">backend</text>
  <text class="box-lbl" x="360" y="292" style="fill:#3A1772; stroke:#fff; stroke-width:4px; paint-order:stroke">Transformation</text>
  <text class="box-lbl" x="360" y="318" style="fill:#3A1772; stroke:#fff; stroke-width:4px; paint-order:stroke">system</text>
</svg>

---

# The loop

<svg class="flow" style="max-width: 1180px" viewBox="0 40 1240 214" role="img" aria-label="The loop inside one transformation: a feeder fills the input pool from the metadata catalogue, the packer groups pooled inputs into parcels, the dispatcher hands each parcel to a backend, and outcomes flow back to the inputs">
  <defs>
    <marker id="ahL" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <g class="c-gen">
    <rect class="step" x="10" y="90" width="132" height="72" rx="14"/>
    <text class="box-lbl" x="76" y="122" style="font-size:17px">Metadata</text>
    <text class="box-lbl" x="76" y="144" style="font-size:17px">catalogue</text>
  </g>
  <line class="ln" x1="142" y1="126" x2="182" y2="126" marker-end="url(#ahL)"/>
  <rect class="plugin" x="186" y="100" width="110" height="52" rx="14"/>
  <text class="plugin-lbl" x="241" y="131">feeder</text>
  <line class="ln" x1="296" y1="126" x2="336" y2="126" marker-end="url(#ahL)"/>
  <rect class="container" x="340" y="60" width="152" height="132" rx="16"/>
  <text class="job-lbl" x="354" y="80">INPUT POOL</text>
  <rect class="pill" x="356" y="90" width="120" height="26" rx="13"/>
  <text class="pill-lbl" x="416" y="108">LFN1</text>
  <rect class="pill" x="356" y="122" width="120" height="26" rx="13"/>
  <text class="pill-lbl" x="416" y="140">LFN2</text>
  <rect class="pill" x="356" y="154" width="120" height="26" rx="13"/>
  <text class="pill-lbl" x="416" y="172">seed 42</text>
  <line class="ln" x1="492" y1="126" x2="522" y2="126" marker-end="url(#ahL)"/>
  <rect class="plugin" x="526" y="100" width="110" height="52" rx="14"/>
  <text class="plugin-lbl" x="581" y="131">packer</text>
  <line class="ln" x1="636" y1="126" x2="666" y2="126" marker-end="url(#ahL)"/>
  <rect class="container" x="670" y="60" width="142" height="132" rx="16"/>
  <text class="job-lbl" x="684" y="80">PARCELS</text>
  <rect class="pill" x="684" y="94" width="114" height="30" rx="15"/>
  <text class="pill-lbl" x="741" y="115">parcel 1</text>
  <rect class="pill" x="684" y="136" width="114" height="30" rx="15"/>
  <text class="pill-lbl" x="741" y="157">parcel 2</text>
  <line class="ln" x1="812" y1="126" x2="842" y2="126" marker-end="url(#ahL)"/>
  <rect class="plugin" x="846" y="100" width="124" height="52" rx="14"/>
  <text class="plugin-lbl" x="908" y="131">dispatcher</text>
  <line class="ln" x1="970" y1="126" x2="1000" y2="126" marker-end="url(#ahL)"/>
  <rect class="container" x="1004" y="60" width="226" height="132" rx="16"/>
  <text class="job-lbl" x="1018" y="80">BACKEND</text>
  <rect class="pill" x="1018" y="90" width="198" height="26" rx="13"/>
  <text class="pill-lbl" x="1117" y="108">DiracX pilots</text>
  <rect class="pill" x="1018" y="122" width="198" height="26" rx="13"/>
  <text class="pill-lbl" x="1117" y="140">HTCondor · HPC</text>
  <rect class="pill" x="1018" y="154" width="198" height="26" rx="13"/>
  <text class="pill-lbl" x="1117" y="172">legacy DIRAC · RMS</text>
  <path class="ln dash" d="M1117 192 L1117 236 L416 236 L416 200" marker-end="url(#ahL)"/>
  <text class="lbl" x="766" y="228" text-anchor="middle">outcomes per input: Processed, or Failed → retry, split or quarantine</text>
</svg>


- **Feeder:** tops up the pool, from a catalogue query, upstream outputs or a seed generator
- **Packer:** decides when and how inputs become parcels
- **Dispatcher:** routes each parcel to its backend

---

# Packing the pool into parcels

- The **feeder** inserts new inputs as `Unassigned`
- Periodically the **packer** claims inputs and proposes **parcels**
- An input is usually a file, but can be part of one or not a file at all

<svg class="flow" style="max-width: 760px" viewBox="0 0 900 352" role="img" aria-label="The input-pool box is split into unassigned, assigned and done sections; the packer assigns LFN3 and LFN6 are unassigned, the five assigned LFNs are grouped into three parcels, nothing is done yet">
  <defs>
    <marker id="ahD" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <text class="tsub" x="120" y="16">Input pool</text>
  <rect class="container" x="14" y="24" width="212" height="316" rx="16"/>
  <text class="job-lbl" x="26" y="44">UNASSIGNED</text>
  <rect class="pill" x="32" y="52" width="176" height="26" rx="13" style="fill:#F1E8F4;stroke:#8B3FA0"/>
  <text class="pill-lbl" x="120" y="70" style="fill:#8B3FA0">LFN3</text>
  <rect class="pill" x="32" y="82" width="176" height="26" rx="13" style="fill:#F8E6F1;stroke:#C0398B"/>
  <text class="pill-lbl" x="120" y="100" style="fill:#C0398B">LFN6</text>
  <line x1="14" y1="116" x2="226" y2="116" stroke="#4A1789" stroke-opacity="0.28" stroke-width="1.6"/>
  <text class="job-lbl" x="26" y="134">ASSIGNED</text>
  <rect class="pill" x="32" y="140" width="176" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="120" y="158" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="32" y="170" width="176" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="120" y="188" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="32" y="200" width="176" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="120" y="218" style="fill:#1F9D55">LFN4</text>
  <rect class="pill" x="32" y="230" width="176" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="120" y="248" style="fill:#138D8D">LFN5</text>
  <rect class="pill" x="32" y="260" width="176" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="120" y="278" style="fill:#5B53C0">LFN7</text>
  <line x1="14" y1="294" x2="226" y2="294" stroke="#4A1789" stroke-opacity="0.28" stroke-width="1.6"/>
  <text class="job-lbl" x="26" y="312">DONE</text>
  <text class="lbl" x="120" y="330" text-anchor="middle" style="font-style:italic">&#8212; none yet &#8212;</text>
  <text class="lbl" x="302" y="170" text-anchor="middle">periodically</text>
  <line class="ln" x1="226" y1="182" x2="376" y2="182" marker-end="url(#ahD)"/>
  <rect class="plugin" x="378" y="156" width="150" height="52" rx="14"/>
  <text class="plugin-lbl" x="453" y="188">packer</text>
  <line class="ln" x1="528" y1="182" x2="590" y2="92" marker-end="url(#ahD)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="182" marker-end="url(#ahD)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="272" marker-end="url(#ahD)"/>
  <rect class="container" x="600" y="56" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="76">PARCEL 1</text>
  <rect class="pill" x="620" y="84" width="124" height="32" rx="16" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="682" y="105" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="752" y="84" width="124" height="32" rx="16" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="814" y="105" style="fill:#1F9D55">LFN4</text>
  <rect class="container" x="600" y="146" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="166">PARCEL 2</text>
  <rect class="pill" x="620" y="174" width="124" height="32" rx="16" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="682" y="195" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="752" y="174" width="124" height="32" rx="16" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="814" y="195" style="fill:#138D8D">LFN5</text>
  <rect class="container" x="600" y="236" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="256">PARCEL 3</text>
  <rect class="pill" x="620" y="264" width="124" height="32" rx="16" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="682" y="285" style="fill:#5B53C0">LFN7</text>
</svg>

---

# Parcels are never retried

- A failed parcel returns its inputs to the pool
- `HandleFailedInput` decides per input: **retry**, **split**, or **quarantine** for an operator
- An input is processed exactly once, or not at all

<svg class="flow" style="max-width: 900px" viewBox="-60 0 1220 392" role="img" aria-label="Each parcel is submitted as a job; job 1 succeeds so LFN1 and LFN4 move to done, jobs 2 and 3 fail so LFN2, LFN5 and LFN7 return to the unassigned section, leaving nothing assigned">
  <defs>
    <marker id="ahE" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
    <marker id="ahEr" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker>
  </defs>
  <text class="tsub" x="120" y="16">Input pool</text>
  <rect class="container" x="14" y="24" width="212" height="316" rx="16"/>
  <text class="job-lbl" x="26" y="42">UNASSIGNED</text>
  <rect class="pill" x="32" y="50" width="176" height="26" rx="13" style="fill:#F1E8F4;stroke:#8B3FA0"/>
  <text class="pill-lbl" x="120" y="68" style="fill:#8B3FA0">LFN3</text>
  <rect class="pill" x="32" y="80" width="176" height="26" rx="13" style="fill:#F8E6F1;stroke:#C0398B"/>
  <text class="pill-lbl" x="120" y="98" style="fill:#C0398B">LFN6</text>
  <rect class="pill" x="32" y="110" width="176" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="120" y="128" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="32" y="140" width="176" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="120" y="158" style="fill:#138D8D">LFN5</text>
  <rect class="pill" x="32" y="170" width="176" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="120" y="188" style="fill:#5B53C0">LFN7</text>
  <line x1="14" y1="200" x2="226" y2="200" stroke="#4A1789" stroke-opacity="0.28" stroke-width="1.6"/>
  <text class="job-lbl" x="26" y="218">ASSIGNED</text>
  <text class="lbl" x="120" y="240" text-anchor="middle" style="font-style:italic">&#8212; none &#8212;</text>
  <line x1="14" y1="256" x2="226" y2="256" stroke="#4A1789" stroke-opacity="0.28" stroke-width="1.6"/>
  <text class="job-lbl" x="26" y="274">DONE</text>
  <rect class="pill" x="32" y="280" width="176" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="120" y="298" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="32" y="310" width="176" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="120" y="328" style="fill:#1F9D55">LFN4</text>
  <line class="ln" x1="226" y1="182" x2="376" y2="182" marker-end="url(#ahE)"/>
  <rect class="plugin" x="378" y="156" width="150" height="52" rx="14"/>
  <text class="plugin-lbl" x="453" y="188">packer</text>
  <line class="ln" x1="528" y1="182" x2="590" y2="92" marker-end="url(#ahE)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="182" marker-end="url(#ahE)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="272" marker-end="url(#ahE)"/>
  <rect class="container" x="600" y="56" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="76">PARCEL 1</text>
  <rect class="pill" x="612" y="84" width="110" height="32" rx="16" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="667" y="105" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="728" y="84" width="110" height="32" rx="16" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="783" y="105" style="fill:#1F9D55">LFN4</text>
  <rect class="container" x="600" y="146" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="166">PARCEL 2</text>
  <rect class="pill" x="612" y="174" width="110" height="32" rx="16" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="667" y="195" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="728" y="174" width="110" height="32" rx="16" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="783" y="195" style="fill:#138D8D">LFN5</text>
  <rect class="container" x="600" y="236" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="256">PARCEL 3</text>
  <rect class="pill" x="612" y="264" width="110" height="32" rx="16" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="667" y="285" style="fill:#5B53C0">LFN7</text>
  <text class="lbl" x="878" y="80" text-anchor="middle">submit</text>
  <line class="ln" x1="850" y1="92" x2="918" y2="92" marker-end="url(#ahE)"/>
  <line class="ln" x1="850" y1="182" x2="918" y2="182" marker-end="url(#ahE)"/>
  <line class="ln" x1="850" y1="272" x2="918" y2="272" marker-end="url(#ahE)"/>
  <rect class="container" x="908" y="40" width="208" height="288" rx="16"/>
  <text class="job-lbl" x="920" y="60">COMPUTE BACKEND</text>
  <rect class="step" x="924" y="70" width="180" height="48" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="box-lbl" x="1014" y="100" style="fill:#1F9D55">JOB 1 &#10003;</text>
  <rect class="step" x="924" y="160" width="180" height="48" rx="13" style="fill:#FBEAE8;stroke:#C0392B"/>
  <text class="box-lbl" x="1014" y="190" style="fill:#C0392B">JOB 2 &#10007;</text>
  <rect class="step" x="924" y="250" width="180" height="48" rx="13" style="fill:#FBEAE8;stroke:#C0392B"/>
  <text class="box-lbl" x="1014" y="280" style="fill:#C0392B">JOB 3 &#10007;</text>
  <path class="ln dash" style="stroke:#C0392B" d="M1104 184 L1142 184 L1142 372 L-34 372 L-34 112 L12 112" marker-end="url(#ahEr)"/>
  <path class="ln dash" style="stroke:#C0392B" d="M1104 274 L1142 274 L1142 372"/>
  <text class="lbl" x="554" y="366" text-anchor="middle" style="fill:#C0392B">failed &#183; HandleFailedInput returns them to the pool</text>
</svg>

---

# A workgraph's lifecycle

<svg class="flow" style="max-width: 1180px" viewBox="0 30 1200 170" role="img" aria-label="Workgraph lifecycle: New, then optional Scouting and Approving, then Active, Finalizing, Completed, Archiving and Archived">
  <defs>
    <marker id="ahW" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <g class="c-gen">
    <rect class="step" x="10" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="72" y="122" style="font-size:17px">New</text>
  </g>
  <line class="ln" x1="134" y1="116" x2="156" y2="116" marker-end="url(#ahW)"/>
  <g class="c-reco">
    <rect class="step" x="160" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="222" y="122" style="font-size:17px">Scouting</text>
  </g>
  <line class="ln" x1="284" y1="116" x2="306" y2="116" marker-end="url(#ahW)"/>
  <g class="c-reco">
    <rect class="step" x="310" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="372" y="122" style="font-size:17px">Approving</text>
  </g>
  <line class="ln" x1="434" y1="116" x2="456" y2="116" marker-end="url(#ahW)"/>
  <g class="c-merge">
    <rect class="step" x="460" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="522" y="122" style="font-size:17px">Active</text>
  </g>
  <line class="ln" x1="584" y1="116" x2="606" y2="116" marker-end="url(#ahW)"/>
  <g class="c-gen">
    <rect class="step" x="610" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="672" y="122" style="font-size:17px">Finalizing</text>
  </g>
  <line class="ln" x1="734" y1="116" x2="756" y2="116" marker-end="url(#ahW)"/>
  <g class="c-gen">
    <rect class="step" x="760" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="822" y="122" style="font-size:17px">Completed</text>
  </g>
  <line class="ln" x1="884" y1="116" x2="906" y2="116" marker-end="url(#ahW)"/>
  <g class="c-gen">
    <rect class="step" x="910" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="972" y="122" style="font-size:17px">Archiving</text>
  </g>
  <line class="ln" x1="1034" y1="116" x2="1056" y2="116" marker-end="url(#ahW)"/>
  <g class="c-gen">
    <rect class="step" x="1060" y="92" width="124" height="48" rx="13"/>
    <text class="box-lbl" x="1122" y="122" style="font-size:17px">Archived</text>
  </g>
  <path class="ln dash" d="M160 80 L160 66 L434 66 L434 80" style="stroke:#E8810B"/>
  <text class="lbl" x="297" y="56" text-anchor="middle" style="fill:#E8810B">optional: validate by doing</text>
  <text class="lbl" x="522" y="168" text-anchor="middle">feeders, packers and parcels run</text>
  <text class="lbl" x="600" y="194" text-anchor="middle" style="font-style:italic">Cancelling → Cleaned is open from every state before Completed</text>
</svg>

- **Scouting:** run on a reduced sample, measure resources, prove the payload works
- **Approving:** ordered actions, e.g. success rate, resource estimate, a manual sign-off
- **Finalizing:** checks that the deliverable is complete, upstream first

---

# What is core and what is yours

<div class="cols">
<div>

**The core** (DiracX, the same everywhere)

- State machines
- Schema and counters
- Dispatcher and backends
- Writing every change

</div>
<div>

**Extensions** (your experiment)

- **Feeders:** where inputs come from
- **Packers:** how they are grouped
- **Hooks:** what to do while active, or on failure
- **Actions:** approve, finalise, archive, clean

</div>
</div>

> Plugins propose, the core writes.

---

# Moving work off DIRAC

- The dispatcher chooses a backend per parcel, which makes migration gradual and reversible

1. Every parcel goes to `legacy-dirac`: DiracX keeps the books, DIRAC runs the jobs
2. A fraction goes to a native backend instead, chosen by hashing the parcel ID
3. The fraction rises until DIRAC carries nothing

<div class="footnotes">
  <div class="footnote">DX-ADR-003. Which native backends you need is for Tuesday's pilots session.</div>
</div>

---

<!-- _class: section -->

# Where this is going

---

# Analysis Productions today

- LHCb's declarative ntupling service, built on the DIRAC Transformation System
- Users declare the application configuration and the input query
- The system handles grouping, failures and provenance
- **Scale:** over 1 EB processed since 2024, about 50M files, 22k samples in 2025 alone

<div class="footnotes">
  <div class="footnote">CHEP 2026, <a href="https://indico.cern.ch/event/1471803/contributions/6970826/">Analysis Productions: an exascale analysis data processing and management service for LHCb</a></div>
</div>

<!-- TODO(Chris): add a screenshot or figure from the CHEP 2026 slides (not reachable from the build environment). -->

---

# The same shape for simulation

- **LbMCSubmit:** LHCb's simulation request system, standard since 2023
- Rules expand a short, structured request into full configurations
- Requests arrive as a GitLab merge request, are tested by CI and reviewed, and only then reach DIRAC

<div class="footnotes">
  <div class="footnote">CHEP 2023 and <a href="https://doi.org/10.1051/epjconf/202533701258">CHEP 2024 proceedings</a></div>
</div>

<!-- TODO(Chris): add a figure from the LbMCSubmit slides. -->

---

<!-- _class: build -->

# Two services, one loop

1. **Declare** what you want, in a short file
2. **Test** it automatically before it runs at scale
3. **Measure** the resources it needs
4. **Approve** it: review, rules, sign-off
5. **Merge** to run, and keep the provenance

---

# The ADRs already have the pieces

| Analysis Productions / LbMCSubmit | DiracX Transformation System |
| --- | --- |
| The YAML request | A workgraph: one CWL document |
| The CI test before submission | **Scouting** on a reduced sample |
| Resource measurement | The scouting resource estimate |
| Review and approval rules | **Approving** actions |
| Provenance in the bookkeeping | Content-addressed processes |

---

# The direction

- Today this loop exists for LHCb, built on top of DIRAC
- In DiracX it becomes part of the system: **declare, test, approve, run**
- Available to every community, not reinvented by each one
- What sits in front of it (YAML, a web form, a merge request) can still differ

<!-- TODO(Chris): decide how firmly to state this as a plan versus a direction. -->

---

<!-- _class: section -->

# Questions for you

---

# How this part works

- The design is settled: each question starts from **what the ADR decided**
- What we need is how your community fits onto it: your extensions, your configuration, your priorities
- Answers become issues for the Transformation System track; anything bigger seeds a birds-of-a-feather session

<div class="footnotes">
  <div class="footnote">Data management, Rucio and the future of pilots have their own sessions on Tuesday.</div>
</div>

---

# 1 · What is an input for you?

- **Decided:** usually a file (LFN); possibly part of one (a lumi section); possibly not a file (a seed, a parameter set)
- **Question:** which of these are your units of work, and which feeder would produce them? Does any of your work have **no inputs at all**, not even seeds?

<div class="footnotes">
  <div class="footnote">DX-ADR-004, DX-ADR-005</div>
</div>

---

# 2 · When an input fails, what should happen?

- **Decided:** `HandleFailedInput` decides per input: retry, split into smaller pieces, or quarantine for an operator
- **Question:** what should your `HandleFailedInput` do? Who decides, and on what information?

<div class="footnotes">
  <div class="footnote">DX-ADR-005, DX-ADR-006</div>
</div>

---

# 3 · What do you need to see before approving?

- **Decided:** optional scouting on a reduced sample, then ordered approving actions
- **Question:** which approving actions does your community need? What must pass before a person signs off?

<div class="footnotes">
  <div class="footnote">DX-ADR-005, DX-ADR-006</div>
</div>

---

# 4 · How will your users submit work?

- **Decided:** everything is CWL underneath; what users see in front of it is open
- **Question:** will your users write CWL directly, or through a higher-level tool like Analysis Productions or LbMCSubmit?

<div class="footnotes">
  <div class="footnote">Not yet in any ADR</div>
</div>

---

# 5 · What drives your feeders?

- **Decided:** a feeder evaluates a query against your catalogue and inserts new inputs
- **Question:** what is your catalogue (DFC metadata, a bookkeeping, DBS, Rucio DIDs)? Can the same file reach a transformation from two feeders?

<div class="footnotes">
  <div class="footnote">DX-ADR-006</div>
</div>

---

# 6 · How fast can you move off DIRAC?

- **Decided:** start with everything on `legacy-dirac`, then shift a growing fraction of parcels to native backends
- **Question:** what would you need to see before raising the fraction? What should we build first to get you there?

<div class="footnotes">
  <div class="footnote">DX-ADR-003</div>
</div>

---

# 7 · Should plugins be pinned?

- **Decided:** feeders, packers and hooks are plain functions discovered through entry points
- **Question:** should a running transformation keep the plugin versions it started with, even after an upgrade?

<div class="footnotes">
  <div class="footnote">DX-ADR-006</div>
</div>

---

# What happens next

- Answers from today shape the development plan and the first extensions
- The **Transformation System track** turns the ADRs into a development plan and starts on the first tasks
- The **CWL track** writes and runs real workgraphs with the `dirac:` hints
- Everything is on the docs site, including the [playground](https://diracx.diracgrid.org/playground/)

<!-- TODO(Chris): align with Alexandre's hackathon deck, which follows. -->

---

# Questions?

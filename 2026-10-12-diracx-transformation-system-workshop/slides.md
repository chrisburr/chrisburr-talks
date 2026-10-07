---
marp: true
theme: cburr
paginate: true
title: "The DiracX Transformation System"
subtitle: "What it is, and how it covers what we need"
author: "Chris Burr & Christophe Haen"
affiliation: "CERN"
event: "DIRAC Users' Workshop 2026"
event_url: ""
date: "2026-10-12"
description: "Monday session: what the DiracX Transformation System is (and is not), broken down concept by concept with CTAO and CMS examples, and how it covers the use cases we know about."
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
<style>
section .cols .flow { max-width: 100%; }
section .side { font-family: var(--font-mono); font-size: 14px; font-weight: 700; letter-spacing: 0.08em; color: var(--muted); text-transform: uppercase; margin: 0 0 var(--sp-2); }
section .cols ul { font-size: 0.78em; }
section .what { font-size: 0.86em; line-height: 1.45; }
</style>

# Before we start

- This talk is about **what** the Transformation System does
- **Not today:** implementation and scalability
     - Write your questions down and catch us at coffee

---

<!-- _class: section -->

# What it is not

---

# Not the DIRAC Transformation System

- Same ideas, twenty years of lessons, **a new model**
- One system covers what DIRAC split three ways:
     - the Transformation System
     - the Production System
     - the **job** half of the WMS
- **"User jobs" change:** a user job is just a parcel, run through the same machinery

---

# DIRAC's WMS was two abstractions

<div class="cols">
<div>

### Pilots

- Get hold of resources
- Match and run work

</div>
<div>

### Jobs

- The work itself
- Transformations, productions and user jobs are **all the same concept**

</div>
</div>

- The Transformation System now owns **the work**; pilots are one way to run it (Tuesday)

---

# Grid high-throughput batch

- Most grid "user jobs" are not one job: they are the same command over many inputs
- That **is** a transformation
- In DiracX, many user jobs become a transformation: retries, grouping and monitoring for free

<!-- TODO(Chris): an example of a typical user loop submitting N jobs would land this. -->

---

# Two minimal use cases

<div class="cols">
<div>

<p class="side">Generic data processing</p>

<svg class="flow" viewBox="182 70 382 180" role="img" aria-label="GDP example, highlighting the none">
  <defs><marker id="ahm90" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="400" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="462" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 360 165, 394 165" marker-end="url(#ahm90)"/>
</svg>

- Process every input file, then merge the outputs

</div>
<div>

<p class="side">Generic simulation</p>

<svg class="flow" viewBox="182 70 516 180" role="img" aria-label="GSIM example, highlighting the none">
  <defs><marker id="ahm91" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Produce</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm91)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm91)"/>
</svg>

- Produce events from nothing (seeds), process them, then merge

</div>
</div>

- Everything else in this talk is a variation on these two

---

<!-- _class: section -->

# What it is

---

# In one paragraph

<div class="what">

A **workgraph** is a **directed acyclic graph** of **transformations**. It is what DIRAC called a production. Each transformation maintains a pool of **inputs**: a **feeder** tops up the pool from the experiment's metadata catalogue, a **packer** groups pooled inputs into **parcels**, and a **dispatcher** hands each parcel to a compute or data backend, which executes it as a job or a request. A workgraph is written as a **CWL document**: its dataflow declares how transformations chain, and inputs arriving from outside the workgraph carry the metadata queries that tell the feeder what to fetch.

</div>

<div class="footnotes">
  <div class="footnote">DX-ADR-002</div>
</div>

---

<!-- _class: section -->

# Breaking it down

---

# Workgraph

- **The entire thing:** everything needed to deliver one request
- What DIRAC called a production, and CMS a workflow
- Has one state, which rolls up its transformations and is how you control them

---

# Workgraph: two examples

<!-- TODO(Chris): CTAO and CMS examples are drafted from their usual workflows, not from the ADRs. Check them with Natthan/Luisa (CTAO) and the CMS contacts. -->

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="182 70 516 180" role="img" aria-label="CTAO example, highlighting the workgraph">
  <defs><marker id="ahm1" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <rect class="prod" x="188" y="76" width="504" height="160" rx="18"/>
  <text class="prod-lbl" x="204" y="96">WORKGRAPH</text>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm1)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm1)"/>
</svg>

- One MC request: a particle type, a zenith angle, a site

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="182 14 402 292" role="img" aria-label="CMS example, highlighting the workgraph">
  <defs><marker id="ahm2" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <rect class="prod" x="188" y="20" width="390" height="272" rx="18"/>
  <text class="prod-lbl" x="204" y="40">WORKGRAPH</text>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm2)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm2)"/>
</svg>

- One request: re-reconstruct a RAW dataset

</div>
</div>

---

# Directed acyclic graph

- Transformations are the nodes; data flowing between them are the edges
- **Directed:** outputs of one feed the next
- **Acyclic:** nothing feeds back into itself
- Graphs fork and merge, which is why it is a graph and not a chain

---

# DAG: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="182 70 516 180" role="img" aria-label="CTAO example, highlighting the dag">
  <defs><marker id="ahm3" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm3)" style="stroke-width:4"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm3)" style="stroke-width:4"/>
  <text class="lbl" x="440" y="246" text-anchor="middle">edges come from the CWL dataflow</text>
</svg>

- A straight chain: produce, process, merge

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="182 14 402 292" role="img" aria-label="CMS example, highlighting the dag">
  <defs><marker id="ahm4" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm4)" style="stroke-width:4"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm4)" style="stroke-width:4"/>
  <text class="lbl" x="383" y="302" text-anchor="middle">edges come from the CWL dataflow</text>
</svg>

- One step fans out: each output type gets its own merge

</div>
</div>

---

# Transformation

- **One step**, run as many independent jobs
- An embarrassingly parallel problem: the same operation over a pool of inputs
- Knows its inputs, its outputs, and which feeder and packer to use

---

# Transformation: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="182 70 516 180" role="img" aria-label="CTAO example, highlighting the transformation">
  <defs><marker id="ahm5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <rect class="tgroup" x="210" y="114" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="284" y="130">×10 000 jobs</text>
  <g class="c-sim"><rect class="step" x="230" y="148" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="226" y="144" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <rect class="tgroup" x="366" y="114" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="440" y="130">×2 000 jobs</text>
  <g class="c-reco"><rect class="step" x="386" y="148" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="382" y="144" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <rect class="tgroup" x="522" y="114" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="596" y="130">×50 jobs</text>
  <g class="c-merge"><rect class="step" x="542" y="148" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="538" y="144" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm5)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm5)"/>
</svg>

- Each box is one transformation, each with its own job count

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="182 14 402 292" role="img" aria-label="CMS example, highlighting the transformation">
  <defs><marker id="ahm6" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <rect class="tgroup" x="210" y="114" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="284" y="130">×5 000 jobs</text>
  <g class="c-reco"><rect class="step" x="230" y="148" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="226" y="144" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <rect class="tgroup" x="408" y="58" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="482" y="74">×200 jobs</text>
  <g class="c-merge"><rect class="step" x="428" y="92" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="424" y="88" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <rect class="tgroup" x="408" y="170" width="148" height="102" rx="14"/>
  <text class="tgroup-lbl" x="482" y="186">×200 jobs</text>
  <g class="c-merge"><rect class="step" x="428" y="204" width="124" height="50" rx="12" style="opacity:.35"/><rect class="step" x="424" y="200" width="124" height="50" rx="12" style="opacity:.6"/></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm6)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm6)"/>
</svg>

- Thousands of reconstruction jobs, far fewer merges

</div>
</div>

<!-- TODO(Chris): job counts are illustrative. -->

---

# Inputs

- The unit a transformation works through, kept in a **pool**
- Usually a file (LFN), possibly **part of one**, possibly **not a file at all**
- Each input is processed exactly once, or not at all

---

# Inputs: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="0 36 698 214" role="img" aria-label="CTAO example, highlighting the inputs">
  <defs><marker id="ahm7" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm7)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm7)"/>
  <rect class="pill" x="8" y="82" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="102" style="font-size:15px">run 1</text>
  <rect class="pill" x="8" y="122" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="142" style="font-size:15px">run 2</text>
  <rect class="pill" x="8" y="162" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="182" style="font-size:15px">run 3</text>
  <rect class="pill" x="8" y="202" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="222" style="font-size:15px">run …</text>
  <line class="ln" x1="196" y1="165" x2="216" y2="165" marker-end="url(#ahm7)"/>
  <text class="tsub" x="100" y="68">input pool</text>
</svg>

- No input files: run numbers (seeds)

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="0 14 584 292" role="img" aria-label="CMS example, highlighting the inputs">
  <defs><marker id="ahm8" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm8)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm8)"/>
  <rect class="pill" x="8" y="82" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="102" style="font-size:15px">A.root [lumi 1–40]</text>
  <rect class="pill" x="8" y="122" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="142" style="font-size:15px">A.root [lumi 41–80]</text>
  <rect class="pill" x="8" y="162" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="182" style="font-size:15px">B.root [lumi 1–60]</text>
  <rect class="pill" x="8" y="202" width="184" height="30" rx="15"/><text class="pill-lbl" x="100" y="222" style="font-size:15px">C.root [all]</text>
  <line class="ln" x1="196" y1="165" x2="216" y2="165" marker-end="url(#ahm8)"/>
  <text class="tsub" x="100" y="68">input pool</text>
</svg>

- Files, or **luminosity sections** of a file

</div>
</div>

---

# Feeding

- A **feeder** tops up the pool, from outside the workgraph
- Usually a query on your metadata catalogue; possibly a generator
- **Internal edges are automatic:** an edge feeder hands each step's outputs to the next one
- So the feeder you write is the external one

---

# Feeding: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="0 36 698 214" role="img" aria-label="CTAO example, highlighting the feeding">
  <defs><marker id="ahm9" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm9)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm9)"/>
  <g class="c-gen"><rect class="step" x="20" y="40" width="160" height="62" rx="14"/><text class="box-lbl" x="100" y="66" style="font-size:16px">Run-number</text><text class="box-lbl" x="100" y="88" style="font-size:16px">generator</text></g>
  <line class="ln" x1="100" y1="102" x2="100" y2="134" marker-end="url(#ahm9)"/>
  <rect class="plugin" x="45" y="140" width="110" height="46" rx="14"/><text class="plugin-lbl" x="100" y="169">feeder</text>
  <line class="ln" x1="155" y1="165" x2="216" y2="165" marker-end="url(#ahm9)"/>
  <text class="lbl" x="100" y="216" text-anchor="middle">yours: an extension</text>
  <text class="lbl" x="440" y="220" text-anchor="middle" style="font-style:italic">internal edges: automatic</text>
</svg>

- A generator issues run numbers until the target statistics are reached

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="0 14 584 292" role="img" aria-label="CMS example, highlighting the feeding">
  <defs><marker id="ahm10" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm10)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm10)"/>
  <g class="c-gen"><rect class="step" x="20" y="40" width="160" height="62" rx="14"/><text class="box-lbl" x="100" y="66" style="font-size:16px">DBS dataset</text><text class="box-lbl" x="100" y="88" style="font-size:16px">query</text></g>
  <line class="ln" x1="100" y1="102" x2="100" y2="134" marker-end="url(#ahm10)"/>
  <rect class="plugin" x="45" y="140" width="110" height="46" rx="14"/><text class="plugin-lbl" x="100" y="169">feeder</text>
  <line class="ln" x1="155" y1="165" x2="216" y2="165" marker-end="url(#ahm10)"/>
  <text class="lbl" x="100" y="216" text-anchor="middle">yours: an extension</text>
  <text class="lbl" x="383" y="276" text-anchor="middle" style="font-style:italic">internal edges: automatic</text>
</svg>

- A DBS query on the dataset, picking up new blocks as they appear

</div>
</div>

---

# Packing and parcels

- A **packer** decides **when** and **how** pooled inputs become **parcels**
- A **parcel** is an immutable unit of work: it becomes one job or one request
- Parcels are never retried: a failed parcel returns its inputs to the pool

---

# Packing: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="0 36 698 264" role="img" aria-label="CTAO example, highlighting the packing">
  <defs><marker id="ahm11" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm11)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm11)"/>
  <rect class="container" x="8" y="52" width="184" height="62" rx="14"/><text class="job-lbl" x="20" y="70">PARCEL 1</text>
  <rect class="pill" x="20" y="78" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="96" style="font-size:14px">run 1</text>
  <rect class="container" x="8" y="124" width="184" height="62" rx="14"/><text class="job-lbl" x="20" y="142">PARCEL 2</text>
  <rect class="pill" x="20" y="150" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="168" style="font-size:14px">run 2</text>
  <rect class="container" x="8" y="196" width="184" height="62" rx="14"/><text class="job-lbl" x="20" y="214">PARCEL 3</text>
  <rect class="pill" x="20" y="222" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="240" style="font-size:14px">run 3</text>
  <line class="ln" x1="196" y1="165" x2="216" y2="165" marker-end="url(#ahm11)"/>
  <text class="lbl" x="284" y="221" text-anchor="middle">packer</text>
</svg>

- **Simulate:** one run per parcel
- **Merge:** group outputs by size

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="0 14 584 292" role="img" aria-label="CMS example, highlighting the packing">
  <defs><marker id="ahm12" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm12)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm12)"/>
  <rect class="container" x="8" y="52" width="184" height="94" rx="14"/><text class="job-lbl" x="20" y="70">PARCEL 1</text>
  <rect class="pill" x="20" y="78" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="96" style="font-size:14px">A [1–40]</text>
  <rect class="pill" x="20" y="110" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="128" style="font-size:14px">A [41–80]</text>
  <rect class="container" x="8" y="156" width="184" height="62" rx="14"/><text class="job-lbl" x="20" y="174">PARCEL 2</text>
  <rect class="pill" x="20" y="182" width="160" height="26" rx="13"/><text class="pill-lbl" x="100" y="200" style="font-size:14px">B [1–60]</text>
  <line class="ln" x1="196" y1="165" x2="216" y2="165" marker-end="url(#ahm12)"/>
  <text class="lbl" x="284" y="221" text-anchor="middle">packer</text>
</svg>

- **Reco:** enough lumi sections for a target number of events, at one site
- **Merge:** group by size per output type

</div>
</div>

---

# Dispatching

- The **dispatcher** hands each parcel to a backend
- Designed to be very flexible: the choice can be made **per parcel**
- Backends can pull (pilots) or push (HPC, sites that cannot call back)
- **Dedicated session tomorrow**

---

# Dispatching: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

<svg class="flow" viewBox="182 70 516 252" role="img" aria-label="CTAO example, highlighting the dispatching">
  <defs><marker id="ahm13" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-sim"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Simulate</text></g>
  <g class="c-reco"><rect class="step" x="378" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="440" y="172" style="font-size:18px">Process</text></g>
  <g class="c-merge"><rect class="step" x="534" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="596" y="172" style="font-size:18px">Merge</text></g>
  <path class="ln" d="M346 165 C 386 165, 338 165, 372 165" marker-end="url(#ahm13)"/>
  <path class="ln" d="M502 165 C 542 165, 494 165, 528 165" marker-end="url(#ahm13)"/>
  <path class="ln" d="M284 190 L284 256" marker-end="url(#ahm13)"/>
  <text class="lbl" x="294" y="230">dispatcher</text>
  <rect class="container" x="212" y="262" width="260" height="50" rx="14"/><text class="box-lbl" x="342" y="294" style="font-size:17px">DiracX pilots</text>
</svg>

- DiracX pilots, or the existing DIRAC during migration

</div>
<div>

<p class="side">CMS · data reprocessing</p>

<svg class="flow" viewBox="182 14 402 308" role="img" aria-label="CMS example, highlighting the dispatching">
  <defs><marker id="ahm14" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker></defs>
  <g class="c-reco"><rect class="step" x="222" y="140" width="124" height="50" rx="12"/><text class="box-lbl" x="284" y="172" style="font-size:18px">Reco</text></g>
  <g class="c-merge"><rect class="step" x="420" y="84" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="116" style="font-size:18px">Merge AOD</text></g>
  <g class="c-merge"><rect class="step" x="420" y="196" width="124" height="50" rx="12"/><text class="box-lbl" x="482" y="228" style="font-size:18px">Merge MINI</text></g>
  <path class="ln" d="M346 165 C 386 165, 380 109, 414 109" marker-end="url(#ahm14)"/>
  <path class="ln" d="M346 165 C 386 165, 380 221, 414 221" marker-end="url(#ahm14)"/>
  <path class="ln" d="M284 190 L284 256" marker-end="url(#ahm14)"/>
  <text class="lbl" x="294" y="230">dispatcher</text>
  <rect class="container" x="212" y="262" width="260" height="50" rx="14"/><text class="box-lbl" x="342" y="294" style="font-size:17px">HTCondor glideins</text>
</svg>

- HTCondor glideins, as today

</div>
</div>

---

# Written as a CWL document

- A workgraph **is** a CWL document
- Its dataflow declares how transformations chain
- Inputs arriving from outside carry the metadata queries that tell the feeder what to fetch
- **Ryun will show you how**

<div class="footnotes">
  <div class="footnote">DX-ADR-007</div>
</div>

---

# The workgraph's lifecycle

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

- **Scouting:** run a small sample first, to prove it works and measure what it needs
- **Approving:** checks and sign-offs before running in full
- **Finalizing:** checks that the deliverable is complete

<div class="footnotes">
  <div class="footnote">Idealised: DX-ADR-005 has the blocked and cancelling states</div>
</div>

---

# Lifecycle: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

- **Scouting:** a few hundred runs
- **Approving:** success rate and resource estimate
- **Active:** keep issuing runs until the statistics are reached
- **Finalizing:** every run merged

</div>
<div>

<p class="side">CMS · data reprocessing</p>

- **Approving** ≈ assignment
- **Active** ≈ running
- **Finalizing** ≈ completed and closed out
- **Archived** ≈ announced and archived

</div>
</div>

<!-- TODO(Chris): check the CMS request-state mapping (ReqMgr) with the CMS contacts. -->

---

# Actions and hooks

<div class="cols">
<div>

### Hooks

- Run **while** in a state, and propose what should change
- e.g. extend the feeder, pause a failing step
- `HandleFailedInput`: retry, split or quarantine

</div>
<div>

### Actions

- Ordered **checks and steps**, each recording a result
- **Approving**, **finalizing**, **archiving**, **cleaning**
- A failure blocks until an operator looks

</div>
</div>

> Plugins propose, the core writes.

---

# Actions and hooks: two examples

<div class="cols">
<div>

<p class="side">CTAO · simulation</p>

- **Active hook:** issue more runs as the statistics come in
- **Finalizing action:** every simulated run has been merged

</div>
<div>

<p class="side">CMS · data reprocessing</p>

- **HandleFailedInput:** a job that processed some lumi sections splits its input, keeping what succeeded
- **Finalizing action:** completion above threshold, then announce

</div>
</div>

---

<!-- _class: section -->

# How does this satisfy everything we need?

---

# You can compose these

- Every use case we know of is some combination of:
     - the shape of the graph
     - a feeder, a packer, hooks and actions
     - data transformations alongside compute ones
- The next slides go through the list, one need at a time

<!-- TODO(Chris): unsure about the order of this section, as in your notes. -->

---

# Scouting

- **Need:** don't launch a billion events before knowing it works
- **How:** the workgraph starts in `Scouting`; the feeder runs in scouting mode on a reduced sample
- A hook decides when the scout is done, and can extend it in stages
- Scout output is ordinary output: approval extends rather than restarts

---

# Resource estimation

- **Need:** know the CPU, memory and disk a job needs before running at scale
- **How:** an `EstimateResourceUsage` approving action measures the scout
- It writes the measured needs back into the requirements of every job that follows

---

# Keeping intermediate files

- **Need:** keep what a middle step produced, not just the final output
- Every parcel's outputs are recorded, which is what feeds the next step
- **But:** that record is for feeding, not a catalogue, and it is cleaned when the transformation is archived
- To keep intermediates, **you have to register them somewhere**, e.g. your catalogue

---

# Multiple steps per job

- **Need:** run several programs in one job to avoid moving data
- **How:** a transformation's process can be a whole CWL workflow, not just one tool
- Same boxes, same wires: you choose where the transformation lines go
- e.g. LHCb Reco + Filter, CMS StepChain

---

# PPG approval

- **Need:** a person or a policy signs off before full production
- **How:** approving actions, in order
     - e.g. scale the scout's usage to the full request; if above what was approved, flag for a second approval
     - then a manual sign-off by the production manager

---

# Histograms

- **Need:** merge monitoring histograms across all jobs and check them
- **How:** finalizing actions on the transformation
     - merge the histograms
     - check the result, e.g. a mean compatible with zero

---

# Processing outputs multiple times

- **Need:** one step's output feeds several consumers
- **How:** each consumer has its own edge feeder from the same declared output
- e.g. one filter feeding several merges, or a removal alongside the next step

---

# Correlated processing

- **Need:** process a file together with related files, e.g. LHCb RDST with its RAW ancestors
- **How:** the pool holds the RDST files; the packer adds each one's RAW ancestors to the parcel
- It holds the parcel back until all of them are staged

---

# Single outputs

- **Need:** one deliverable, e.g. one merged file per request
- **How:** a merge transformation at the end, flushed when the feeders run dry
- The packer knows when its feeder is finished, so it packs the remainder

---

# Many outputs

- **Need:** one step produces several output types
- **How:** each output is declared, and each can have its own consumers and replication
- e.g. CMS AOD and MINIAOD with separate merges

---

# Retrying

- **Need:** recover from failures without double-processing
- **How:** inputs are retried, never parcels
- `HandleFailedInput` decides per input: retry, give up for an operator, or split
- An input is processed exactly once, or not at all

---

# Splitting

- **Need:** a job did part of its work, or an input is too big
- **How:** an input splits into children, e.g. lumi sections or event ranges
- What succeeded is kept; what didn't goes back into the pool, smaller

---

# Staging input

- **Need:** data on tape must be on disk before a job runs
- **How:** a staging data transformation copies it to a buffer
- The processing packer delays each input until its replica is there

---

# Remove a replica after it has been processed N times

- **Need:** free a buffer once every consumer is done with a file
- **How:** a removal data transformation fed from the same files
- Its packer delays each file until every consumer has processed it

---

# … and more

- Raw data distribution: assign each run to a destination and stick to it
- Standalone data transformations, outside any workgraph
- The LHCb worked examples cover simulation, sprucing and stripping end to end

<div class="footnotes">
  <div class="footnote">DX-ADR examples page, on the docs site</div>
</div>

<!-- TODO(Chris): add the items behind the "..." in your notes. -->

---

<!-- _class: section -->

# Going further

---

# Operations and debugging

- Every input and parcel has a state, and every transition is logged
- A quarantined input waits for an operator's decision: nothing is silently dropped
- "Why is this workgraph stuck?" is answered by counts, not by reading logs

---

# Monitoring

- Exact counts of inputs and parcels in every state, without scanning big tables
- Bytes queued per storage element, for data transformations
- The playground shows a workgraph running, step by step

<div class="footnotes">
  <div class="footnote">DX-ADR-009 journalled counters</div>
</div>

---

# Analysis Productions style submission

- LHCb's Analysis Productions and LbMCSubmit share one loop: **declare, test, approve, merge to run**
- Over 1 EB processed since 2024; about 50M files; 22k samples in 2025
- The pieces map directly: a workgraph is the request, scouting is the test, approving actions are the approval
- The direction: this loop for every community, not reinvented by each one

<div class="footnotes">
  <div class="footnote">CHEP 2026; LbMCSubmit at CHEP 2023 and 2024</div>
</div>

---

# Deploying software

- Each job's environment is declared in the CWL, not assumed from the machine

<!-- TODO(Chris): fill in with what you want to say here. -->

---

# Questions?

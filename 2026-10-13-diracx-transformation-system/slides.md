---
marp: true
theme: cburr
paginate: true
title: "The DiracX Transformation System"
subtitle: "Workgraphs, transformations and parcels"
author: "Chris Burr"
affiliation: "CERN"
event: "DIRAC Users' Workshop"
event_url: ""
date: "2026-10-13"
description: "What the DiracX Transformation System is, in the vocabulary of the DX-ADR-002 to DX-ADR-009 ADRs, and how it covers the use cases we need."
---

<!-- Deck-local styling: the flow-diagram language from the July DiracX deck,
     plus the workgraph breakdown (focus-* highlighting) and the pink "new"
     accent used on the "does it do everything" slides. -->
<style>
section .flow { display: block; width: 100%; height: auto; margin: 0 auto; }

/* identity palette — sets the fill tint (--cf) + line/label colour (--c) */
section .flow .c-sim    { --c: #2D6CDF; --cf: #E6EEFC; }
section .flow .c-reco   { --c: #E8810B; --cf: #FCF0E1; }
section .flow .c-filter { --c: #8B3FA0; --cf: #F1E8F4; }
section .flow .c-merge  { --c: #1F9D55; --cf: #E4F3EB; }
section .flow .c-gen    { --c: #4A1789; --cf: #ECE6F4; }
section .flow .nw       { --c: #C0398B; --cf: #F8E6F1; }

/* nodes */
section .flow .step, section .flow .tile {
  fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.4;
  filter: drop-shadow(0 2px 3px rgba(74, 23, 137, 0.16));
}
section .flow .tile.data { stroke-dasharray: 3 5; stroke-linecap: round; stroke-width: 3; }
section .flow .mfill { fill: var(--cf, #ECE6F4); stroke: var(--c, #4A1789); stroke-width: 2.6; }
section .flow .mstep-grp { filter: drop-shadow(0 2px 3px rgba(74, 23, 137, 0.16)); }
section .flow .container { fill: rgba(74, 23, 137, 0.025); stroke: var(--ink); stroke-width: 2.2; stroke-dasharray: 9 6; }
section .flow .prod, section .flow .wgbox { fill: rgba(74, 23, 137, 0.02); stroke: var(--ink); stroke-width: 2.4; stroke-dasharray: 8 7; }
section .flow .tgroup { fill: rgba(74, 23, 137, 0.03); stroke: var(--ink-soft); stroke-width: 2; }
section .flow .tgroup-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 16px; fill: var(--ink-soft); }
section .flow .box-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 20px; fill: var(--c, #4A1789); text-anchor: middle; }
section .flow .tsub { font-family: var(--font-sans); font-size: 16px; font-weight: 700; fill: var(--muted); }
section .flow .tsub2 { font-family: var(--font-sans); font-size: 13px; fill: var(--c, #4A1789); opacity: 0.8; text-anchor: middle; }
section .flow .prod-lbl { font-family: var(--font-mono); font-size: 14px; font-weight: 700; fill: var(--ink); letter-spacing: 0.12em; }
section .flow .job-lbl { font-family: var(--font-mono); font-size: 13px; font-weight: 700; fill: var(--ink); letter-spacing: 0.08em; }

/* connectors */
section .flow .ln { stroke: var(--ink-soft); stroke-width: 3; fill: none; stroke-linecap: round; }
section .flow .ln.thin { stroke-width: 2; }
section .flow .ln.dash { stroke-dasharray: 7 6; }
section .flow .ln.feed { stroke: #138D8D; stroke-dasharray: 7 5; }
section .flow .ln.nw { stroke: #C0398B; }

/* data pills, sources, labels */
section .flow .pill { fill: var(--cf, #F4F1FA); stroke: var(--c, rgba(74, 23, 137, 0.30)); stroke-width: 1.5; }
section .flow .pill-lbl { font-family: var(--font-sans); font-size: 17px; fill: var(--c, var(--ink)); text-anchor: middle; }
section .flow .src { fill: #E6F4F2; stroke: #138D8D; stroke-width: 2; }
section .flow .src-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 16px; fill: #0F7A7A; text-anchor: middle; }
section .flow .feed-lbl { font-family: var(--font-sans); font-size: 14px; fill: #0F7A7A; }
section .flow .edge-lbl { font-family: var(--font-sans); font-size: 13px; fill: var(--muted); }
section .flow .lbl { font-family: var(--font-mono); font-size: 13px; fill: var(--muted); }
section .flow .mini { font-family: var(--font-mono); font-size: 11px; fill: var(--muted); text-anchor: middle; letter-spacing: 0.04em; }
section .flow .mini-job { font-family: var(--font-mono); font-size: 13px; fill: var(--c); text-anchor: middle; }
section .flow .code-lbl { font-family: var(--font-mono); font-size: 16px; fill: var(--ink); }
section .flow .nw-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 15px; fill: #C0398B; }
section .flow .eq { font-family: var(--font-sans); font-weight: 700; font-size: 56px; fill: var(--ink-soft); }

/* inside a transformation card: input pool, parcels, backend */
section .flow .pool { fill: #FFFFFF; stroke: var(--ink-soft); stroke-opacity: 0.45; stroke-width: 1.6; }
section .flow .parcel { fill: #FFFFFF; stroke: var(--c, var(--ink-soft)); stroke-width: 1.8; }
section .flow .backend { fill: #F4F1FA; stroke: var(--ink-soft); stroke-width: 2; }
section .flow .be-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 15px; fill: var(--ink-soft); text-anchor: middle; }
section .flow .dbc { fill: var(--cf); stroke: var(--c); stroke-width: 2; }
section .flow .db-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 14px; fill: var(--c); text-anchor: middle; }

/* state machines, actions, hooks */
section .flow .st { fill: #FFFFFF; stroke: var(--ink-soft); stroke-width: 2; }
section .flow .st.lit { fill: var(--ink); stroke: var(--ink); }
section .flow .st.cancel { fill: #FBEAE8; stroke: #C0392B; }
section .flow .st-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 15px; fill: var(--ink); text-anchor: middle; }
section .flow .st-lbl.big { font-size: 19px; }
section .flow .st.lit + .st-lbl, section .flow .st-lbl.lit { fill: #FFFFFF; }
section .flow .act { fill: var(--cf); stroke: var(--c); stroke-width: 2; }
section .flow .act-n { font-family: var(--font-mono); font-weight: 700; font-size: 15px; fill: var(--c); }
section .flow .act-lbl { font-family: var(--font-sans); font-weight: 700; font-size: 17px; fill: var(--c); }
section .flow .hook { fill: #E6F4F2; stroke: #138D8D; stroke-width: 2.2; }
section .flow .hook-lbl { font-family: var(--font-mono); font-weight: 700; font-size: 15px; fill: #0F7A7A; text-anchor: middle; }
section .flow .chip { stroke-width: 1.8; }
section .flow .hook-c .chip { fill: #E6F4F2; stroke: #138D8D; }
section .flow .act-c .chip { fill: #ECE6F4; stroke: var(--ink-soft); }
section .flow .chip-lbl { font-family: var(--font-mono); font-size: 14px; font-weight: 700; text-anchor: middle; }
section .flow .hook-c .chip-lbl { fill: #0F7A7A; }
section .flow .act-c .chip-lbl { fill: var(--ink); }

/* breakdown slides: dim everything but the concept being introduced */
section .flow.wg[class*="focus-"] .k { opacity: 0.14; }
section .flow.wg.focus-wg .k:is(.k-wg, .k-tf, .k-dag, .k-in, .k-pack, .k-out),
section .flow.wg.focus-dag .k:is(.k-tf, .k-dag),
section .flow.wg.focus-tf .k.k-tf,
section .flow.wg.focus-in .k.k-in,
section .flow.wg.focus-feed .k:is(.k-feed, .k-in),
section .flow.wg.focus-pack .k:is(.k-pack, .k-in),
section .flow.wg.focus-disp .k:is(.k-disp, .k-pack) { opacity: 1; }

/* the split slides: two generic graphs side by side */
section .split { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-6); align-items: start; }
section .split .flow { max-height: 430px; }
section .cap { text-align: center; font-weight: 700; font-size: 22px; margin: 0 0 var(--sp-3); }
section .defn { font-size: 23px; max-width: 64ch; }
</style>

# Before we start

<!-- _class: build -->

- This session is about the **model**: what the system does, and the words we use for it
- **We want to get everyone on the same page:** Forget DIRAC concepts!
- **Implementation and scalability:** not today
    - Write them down, ask us over coffee ☕
- It's all in the ADRs: [diracx#1042](https://github.com/DIRACGrid/diracx/pull/1042)
    - DX-ADR-002 → 009, plus an [explanation](https://diracx--1042.org.readthedocs.build/en/1042/user/explanations/transformation-system/) and a [playground](https://diracx--1042.org.readthedocs.build/en/1042/playground/) you can poke at

---

<!-- _class: section -->

# What this is not

---

<!-- _class: build -->

# What this is not

- **Not** the DIRAC Transformation System with a new coat of paint
    - Same underpinnings and lessons learned, but a different shape
    - One system where DIRAC had three:
      - Transformation
      - Production
      - "job" half of the WMS
- **Not** only for centrally ran activity
    - "User jobs" change too

---

# DIRAC's WMS is two distinct abstractions

<div class="cols">
<div>

- **Pilots:** getting hold of resources
- **Jobs:** describing the work to run on them
- DiracX pulls them apart:
    - Pilots → **Compute Backends**
    - Jobs → **Transformation System**

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 360" role="img" aria-label="DIRAC&#x27;s WMS split into pilots and jobs; pilots become one DiracX compute backend, jobs move into the Transformation System">
  <defs><marker id="m1p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m1t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m1n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m1r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m1g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m1a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <rect class="prod" x="10" y="20" width="190" height="320" rx="18"/>
  <text class="prod-lbl" x="28" y="46">DIRAC WMS</text>
  <g class="c-sim"><rect class="tile" x="30" y="80" width="150" height="60" rx="12"/><text class="box-lbl" x="105.0" y="109.0">Pilots</text><text class="tsub2" x="105.0" y="126.0">resources</text></g>
  <g class="c-reco"><rect class="tile" x="30" y="220" width="150" height="60" rx="12"/><text class="box-lbl" x="105.0" y="249.0">Jobs</text><text class="tsub2" x="105.0" y="266.0">work</text></g>
  <path class="ln" d="M180 110 L300 110" marker-end="url(#m1p)"/>
  <path class="ln" d="M180 250 L300 250" marker-end="url(#m1p)"/>
  <g class="c-sim"><rect class="tile" x="306" y="70" width="240" height="80" rx="14"/><text class="box-lbl" x="426" y="104">Compute backends</text><text class="tsub2" x="426" y="128">pilots, HPC, HTCondor, …</text></g>
  <g class="c-reco"><rect class="tile" x="306" y="210" width="240" height="80" rx="14"/><text class="box-lbl" x="426" y="244">Transformation</text><text class="box-lbl" x="426" y="268">System</text></g>
  <text class="lbl" x="240" y="98" text-anchor="middle">DiracX</text>
  <text class="lbl" x="240" y="238" text-anchor="middle">DiracX</text>
</svg>

</div>
</div>

---

# Same concept, new names

> jobs, transformation and productions are the same <cite>The future of DIRAC</cite>

- We meant that about search APIs. Turns out it goes deeper:



<svg class="flow " style="max-width: 980px" viewBox="0 0 1000 250" role="img" aria-label="DIRAC nests production, transformation, task and job; DiracX nests workgraph, transformation and parcel, where a parcel runs as a job or a request">
  <defs><marker id="m2p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m2t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m2n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m2r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m2g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m2a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <text class="tsub" x="250" y="14" text-anchor="middle">DIRAC</text>
  <rect class="prod" x="50" y="20" width="400" height="210" rx="16"/><text class="prod-lbl" x="64" y="44" text-anchor="start">PRODUCTION</text><rect class="tgroup" x="72" y="56" width="356" height="164" rx="16"/><text class="tgroup-lbl" x="86" y="80" text-anchor="start">Transformation</text><rect class="tgroup" x="94" y="92" width="312" height="118" rx="16"/><text class="tgroup-lbl" x="108" y="116" text-anchor="start">Task</text>
  <g class="c-reco"><rect class="step" x="130" y="150" width="240" height="40" rx="12"/><text class="box-lbl" x="250" y="177">Job</text></g>
  <text class="eq" x="500" y="140" text-anchor="middle">≈</text>
  <text class="tsub" x="750" y="14" text-anchor="middle">DiracX</text>
  <rect class="prod" x="550" y="20" width="400" height="210" rx="16"/><text class="prod-lbl" x="564" y="44" text-anchor="start">WORKGRAPH</text><rect class="tgroup" x="572" y="56" width="356" height="164" rx="16"/><text class="tgroup-lbl" x="586" y="80" text-anchor="start">Transformation</text><rect class="tgroup" x="594" y="92" width="312" height="118" rx="16"/><text class="tgroup-lbl" x="608" y="116" text-anchor="start">Parcel</text>
  <g class="c-reco"><rect class="step" x="630" y="150" width="112" height="40" rx="12"/><text class="box-lbl" x="686" y="177">Job</text></g>
  <g class="c-gen"><rect class="step" x="758" y="150" width="112" height="40" rx="12"/><text class="box-lbl" x="814" y="177">Request</text></g>
</svg>

---

# Grid high-throughput batch

- For the non-DIRAC people: one program, thousands of files, a `for` loop of submissions…
    - …then babysitting: resubmit failures, group small files, track what's done
- **That's a transformation.** Many user jobs become one DiracX transformation

<svg class="flow " style="max-width: 940px" viewBox="0 0 1000 270" role="img" aria-label="Many hand-submitted user jobs, some failed and resubmitted, become one transformation with an input pool and parcels">
  <defs><marker id="m3p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m3t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m3n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m3r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m3g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m3a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <text class="code-lbl" x="200" y="22" text-anchor="middle">for f in files: submit(f)</text>
  <g class="c-reco"><rect class="step" x="20" y="40" width="64" height="40" rx="10"/><text class="mini-job" x="52" y="66">job</text></g>
  <g class="c-reco"><rect class="step" x="94" y="40" width="64" height="40" rx="10"/><text class="mini-job" x="126" y="66">job</text></g>
  <g class="c-reco"><rect class="step" x="168" y="40" width="64" height="40" rx="10" style="fill:#FBEAE8;stroke:#C0392B"/><text class="mini-job" x="200" y="66" style="fill:#C0392B">✗</text></g>
  <g class="c-reco"><rect class="step" x="242" y="40" width="64" height="40" rx="10"/><text class="mini-job" x="274" y="66">job</text></g>
  <g class="c-reco"><rect class="step" x="316" y="40" width="64" height="40" rx="10"/><text class="mini-job" x="348" y="66">↻</text></g>
  <g class="c-reco"><rect class="step" x="20" y="92" width="64" height="40" rx="10"/><text class="mini-job" x="52" y="118">job</text></g>
  <g class="c-reco"><rect class="step" x="94" y="92" width="64" height="40" rx="10"/><text class="mini-job" x="126" y="118">job</text></g>
  <g class="c-reco"><rect class="step" x="168" y="92" width="64" height="40" rx="10" style="fill:#FBEAE8;stroke:#C0392B"/><text class="mini-job" x="200" y="118" style="fill:#C0392B">✗</text></g>
  <g class="c-reco"><rect class="step" x="242" y="92" width="64" height="40" rx="10"/><text class="mini-job" x="274" y="118">job</text></g>
  <g class="c-reco"><rect class="step" x="316" y="92" width="64" height="40" rx="10"/><text class="mini-job" x="348" y="118">job</text></g>
  <g class="c-reco"><rect class="step" x="20" y="144" width="64" height="40" rx="10"/><text class="mini-job" x="52" y="170">job</text></g>
  <g class="c-reco"><rect class="step" x="94" y="144" width="64" height="40" rx="10"/><text class="mini-job" x="126" y="170">job</text></g>
  <g class="c-reco"><rect class="step" x="168" y="144" width="64" height="40" rx="10" style="fill:#FBEAE8;stroke:#C0392B"/><text class="mini-job" x="200" y="170" style="fill:#C0392B">✗</text></g>
  <g class="c-reco"><rect class="step" x="242" y="144" width="64" height="40" rx="10"/><text class="mini-job" x="274" y="170">job</text></g>
  <g class="c-reco"><rect class="step" x="316" y="144" width="64" height="40" rx="10"/><text class="mini-job" x="348" y="170">↻</text></g>
  <g class="c-reco"><rect class="step" x="20" y="196" width="64" height="40" rx="10"/><text class="mini-job" x="52" y="222">job</text></g>
  <g class="c-reco"><rect class="step" x="94" y="196" width="64" height="40" rx="10"/><text class="mini-job" x="126" y="222">job</text></g>
  <g class="c-reco"><rect class="step" x="168" y="196" width="64" height="40" rx="10" style="fill:#FBEAE8;stroke:#C0392B"/><text class="mini-job" x="200" y="222" style="fill:#C0392B">✗</text></g>
  <g class="c-reco"><rect class="step" x="242" y="196" width="64" height="40" rx="10"/><text class="mini-job" x="274" y="222">job</text></g>
  <g class="c-reco"><rect class="step" x="316" y="196" width="64" height="40" rx="10"/><text class="mini-job" x="348" y="222">job</text></g>
  <path class="ln" d="M400 140 L520 140" marker-end="url(#m3p)"/>
  <g class="c-reco"><rect class="tile" x="530" y="70" width="440" height="140" rx="18"/><text class="box-lbl" x="750" y="104">One transformation</text></g>
  <rect class="pool" x="556" y="130" width="160" height="50" rx="25"/>
  <circle cx="578" cy="155" r="6" fill="#138D8D"/>
  <circle cx="601" cy="155" r="6" fill="#138D8D"/>
  <circle cx="624" cy="155" r="6" fill="#138D8D"/>
  <circle cx="647" cy="155" r="6" fill="#138D8D"/>
  <circle cx="670" cy="155" r="6" fill="#138D8D"/>
  <circle cx="693" cy="155" r="6" fill="#138D8D"/>
  <text class="mini" x="636" y="200">inputs</text>
  <path class="ln" d="M716 155 L760 155" marker-end="url(#m3p)"/>
  <rect class="parcel" x="768" y="138" width="58" height="34" rx="8"/>
  <circle cx="786" cy="155" r="5.5" fill="#138D8D"/><circle cx="808" cy="155" r="5.5" fill="#138D8D"/>
  <rect class="parcel" x="834" y="138" width="58" height="34" rx="8"/>
  <circle cx="852" cy="155" r="5.5" fill="#138D8D"/><circle cx="874" cy="155" r="5.5" fill="#138D8D"/>
  <rect class="parcel" x="900" y="138" width="58" height="34" rx="8"/>
  <circle cx="918" cy="155" r="5.5" fill="#138D8D"/><circle cx="940" cy="155" r="5.5" fill="#138D8D"/>
  <text class="mini" x="866" y="200">parcels</text>
</svg>

---

# Two minimal use cases

<div class="split">
<div>

<p class="cap">Generic data processing: process + merge</p>

<svg class="flow wg" viewBox="0 0 540 452" role="img" aria-label="Generic data processing: Process then Merge">
  <defs><marker id="m4p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m4t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m4n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m4r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m4g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m4a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="src-g"><rect class="src" x="175.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="270.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M270.0 40 L270.0 65" marker-end="url(#m4t)"/>
  <g class="c-reco"><rect class="tile" x="170.0" y="70" width="200" height="56" rx="12"/><text class="box-lbl" x="270.0" y="105.0">Process</text></g>
  <path class="ln" d="M270.0 126 L270.0 167" marker-end="url(#m4p)"/>
  <g class="c-merge"><rect class="tile" x="170.0" y="172" width="200" height="56" rx="12"/><text class="box-lbl" x="270.0" y="207.0">Merge</text></g>
  <path class="ln" d="M270.0 228 L270.0 269" marker-end="url(#m4p)"/>
  <g class="out-g"><rect class="pill" x="200.0" y="273" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="270.0" y="296.0">dataset</text></g>
</svg>

</div>
<div>

<p class="cap">Generic simulation: produce + process + merge</p>

<svg class="flow wg" viewBox="0 0 540 452" role="img" aria-label="Generic simulation: Produce then Process then Merge">
  <defs><marker id="m5p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m5t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m5n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m5r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m5g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m5a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="src-g"><rect class="src" x="175.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="270.0" y="29.0">seeds</text></g>
  <path class="ln feed" d="M270.0 40 L270.0 65" marker-end="url(#m5t)"/>
  <g class="c-sim"><rect class="tile" x="170.0" y="70" width="200" height="56" rx="12"/><text class="box-lbl" x="270.0" y="105.0">Produce</text></g>
  <path class="ln" d="M270.0 126 L270.0 167" marker-end="url(#m5p)"/>
  <g class="c-reco"><rect class="tile" x="170.0" y="172" width="200" height="56" rx="12"/><text class="box-lbl" x="270.0" y="207.0">Process</text></g>
  <path class="ln" d="M270.0 228 L270.0 269" marker-end="url(#m5p)"/>
  <g class="c-merge"><rect class="tile" x="170.0" y="274" width="200" height="56" rx="12"/><text class="box-lbl" x="270.0" y="309.0">Merge</text></g>
  <path class="ln" d="M270.0 330 L270.0 371" marker-end="url(#m5p)"/>
  <g class="out-g"><rect class="pill" x="200.0" y="375" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="270.0" y="398.0">dataset</text></g>
</svg>

</div>
</div>

---

<!-- _class: section -->

# What is it?

---

# What is it?

<blockquote class="defn">

A **workgraph** is a directed acyclic graph of **transformations**. It is what DIRAC called a production. Each transformation maintains a pool of **inputs**: a **feeder** tops up the pool from the experiment's metadata catalogue, a **packer** groups pooled inputs into **parcels**, and a **dispatcher** hands each parcel to a compute or data **backend**, which executes it as a job or a request.

<cite>DX-ADR-002</cite>
</blockquote>

---

# Workgraph

- The **entire thing**: everything needed to deliver what was asked for
    - What DIRAC called a **production**
- Created in one go, with all its transformations
- Its status **rolls up** its members, and is the **control surface**
    - start, drain, halt, cancel

---

# Workgraph

<div class="split">
<div>

<svg class="flow wg focus-wg" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m6p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m6t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m6n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m6r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m6g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m6a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m6t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m6p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m6p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m6p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m6p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m6p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m6p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-wg" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m7p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m7t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m7n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m7r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m7g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m7a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m7t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m7p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m7p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m7p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m7p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m7p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m7p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m7p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m7p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m7p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Directed acyclic graph

- Transformations **chain**: the output of one is the input of the next
- A **graph**, not a chain: real workgraphs fork and merge
- Downstream picks up outputs **as they appear**
    - No waiting for the whole upstream stage to finish

---

# Directed acyclic graph

<div class="split">
<div>

<svg class="flow wg focus-dag" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m8p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m8t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m8n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m8r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m8g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m8a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m8t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m8p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m8p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m8p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m8p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m8p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m8p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-dag" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m9p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m9t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m9n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m9r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m9g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m9a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m9t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m9p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m9p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m9p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m9p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m9p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m9p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m9p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m9p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m9p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Transformation

- Applies **one operation** to a pool of inputs
    - An [embarrassingly parallel](https://en.wikipedia.org/wiki/Embarrassingly_parallel) problem
- Two kinds:
    - **Compute:** runs jobs
    - **Data:** runs requests (copy or remove replicas)
- Same name and same idea as in DIRAC

---

# Transformation

<div class="split">
<div>

<svg class="flow wg focus-tf" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m10p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m10t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m10n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m10r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m10g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m10a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m10t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m10p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m10p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m10p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m10p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m10p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m10p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-tf" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m11p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m11t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m11n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m11r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m11g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m11a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m11t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m11p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m11p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m11p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m11p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m11p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m11p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m11p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m11p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m11p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Inputs

- Each transformation keeps a **pool** of inputs
- Usually a file (LFN)
    - Sometimes a fraction of one, sometimes not a file at all (a seed)
- Processed **exactly once, or not at all**
    - `Unassigned` → `Assigned` → `Processed`

---

# Inputs

<div class="split">
<div>

<svg class="flow wg focus-in" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m12p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m12t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m12n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m12r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m12g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m12a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m12t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m12p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m12p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m12p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m12p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m12p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m12p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-in" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m13p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m13t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m13n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m13r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m13g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m13a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m13t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m13p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m13p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m13p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m13p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m13p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m13p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m13p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m13p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m13p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Feeding

- The **feeder** tops up the pool, and never yields the same input twice
- **External** feeders bring work in from outside the workgraph:
    - a metadata query, a run range that grows over time, seeds
    - Experiment-specific: this is where your catalogue plugs in
- **Internal** feeders follow the edges of the graph
    - You don't need to care about these

---

# Feeding

<div class="split">
<div>

<svg class="flow wg focus-feed" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m14p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m14t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m14n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m14r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m14g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m14a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m14t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m14p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m14p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m14p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m14p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m14p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m14p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-feed" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m15p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m15t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m15n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m15r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m15g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m15a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m15t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m15p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m15p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m15p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m15p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m15p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m15p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m15p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m15p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m15p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Packing and parcels

- The **packer** groups pooled inputs into **parcels**
    - **When:** hold out for full groups while input keeps coming, pack the rest once it stops
    - **How:** ~3 GB per parcel, same storage, same run, …
- A **parcel** is immutable and **never retried**
    - A failure sends its *inputs* back to the pool

---

# Packing and parcels

<div class="split">
<div>

<svg class="flow wg focus-pack" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m16p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m16t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m16n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m16r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m16g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m16a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m16t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m16p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m16p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m16p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m16p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m16p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m16p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-pack" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m17p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m17t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m17n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m17r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m17g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m17a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m17t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m17p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m17p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m17p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m17p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m17p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m17p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m17p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m17p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m17p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Dispatching

- The **dispatcher** hands each parcel to a **backend**
    - Compute: native pilots, push to HPC, HTCondor, legacy DIRAC, …
    - Data: requests
- Designed to be **very flexible** in how you decide
    - The dispatcher chooses, the packer can constrain
- User jobs take exactly the same path
- **Dedicated session tomorrow**

---

# Dispatching

<div class="split">
<div>

<svg class="flow wg focus-disp" viewBox="0 0 540 452" role="img" aria-label="Generic data processing workgraph: Process, Merge">
  <defs><marker id="m18p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m18t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m18n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m18r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m18g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m18a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="234" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">metadata query</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m18t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="176" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#2D6CDF"/><circle cx="172" cy="133" r="6" fill="#2D6CDF"/><circle cx="190" cy="133" r="6" fill="#2D6CDF"/><circle cx="208" cy="133" r="6" fill="#2D6CDF"/><circle cx="226" cy="133" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m18p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="133" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="133" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m18p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m18p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#E8810B"/><circle cx="172" cy="239" r="6" fill="#E8810B"/><circle cx="190" cy="239" r="6" fill="#E8810B"/><circle cx="208" cy="239" r="6" fill="#E8810B"/><circle cx="226" cy="239" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m18p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#E8810B"/><circle cx="309" cy="239" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#E8810B"/><circle cx="359" cy="239" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m18p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 268 L202.0 312" marker-end="url(#m18p)"/><g class="out-g"><rect class="pill" x="132.0" y="316" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="339.0">dataset</text></g></g>
</svg>

</div>
<div>

<svg class="flow wg focus-disp" viewBox="0 0 540 452" role="img" aria-label="Generic simulation workgraph: Produce, Process, Merge">
  <defs><marker id="m19p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m19t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m19n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m19r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m19g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m19a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="k k-wg"><rect class="wgbox" x="8" y="56" width="392" height="340" rx="18"/><text class="prod-lbl" x="22" y="76">WORKGRAPH</text></g>
  <g class="k k-feed"><g class="src-g"><rect class="src" x="107.0" y="6" width="190" height="34" rx="17.0"/><text class="src-lbl" x="202.0" y="29.0">seeds</text></g><path class="ln feed" d="M202.0 40 L202.0 87" marker-end="url(#m19t)"/><text class="feed-lbl" x="214.0" y="76">feeder</text></g>
  <g class="k k-disp"><rect class="backend" x="432" y="92" width="100" height="282" rx="14"/><text class="be-lbl" x="482" y="118">compute</text><text class="be-lbl" x="482" y="136">backend</text></g>
  <g class="k k-tf c-sim"><rect class="tile" x="22" y="92" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="134.0">Produce</text></g>
  <g class="k k-in"><text class="mini" x="190" y="108">inputs</text><rect class="pool" x="138" y="116" width="104" height="34" rx="17"/><circle cx="154" cy="133" r="6" fill="#138D8D"/><circle cx="172" cy="133" r="6" fill="#138D8D"/><circle cx="190" cy="133" r="6" fill="#138D8D"/><circle cx="208" cy="133" r="6" fill="#138D8D"/><circle cx="226" cy="133" r="6" fill="#138D8D"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 133 L268 133" marker-end="url(#m19p)"/><text class="mini" x="324" y="108">parcels</text><rect class="parcel" x="278" y="118" width="44" height="30" rx="8"/><circle cx="291" cy="133" r="5.5" fill="#138D8D"/><circle cx="309" cy="133" r="5.5" fill="#138D8D"/><rect class="parcel" x="328" y="118" width="44" height="30" rx="8"/><circle cx="341" cy="133" r="5.5" fill="#138D8D"/><circle cx="359" cy="133" r="5.5" fill="#138D8D"/></g>
  <g class="k k-disp"><path class="ln" d="M382 133 L427 133" marker-end="url(#m19p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 162 L202.0 193" marker-end="url(#m19p)"/><text class="edge-lbl" x="214.0" y="185">edge feeder</text></g>
  <g class="k k-tf c-reco"><rect class="tile" x="22" y="198" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="240.0">Process</text></g>
  <g class="k k-in"><text class="mini" x="190" y="214">inputs</text><rect class="pool" x="138" y="222" width="104" height="34" rx="17"/><circle cx="154" cy="239" r="6" fill="#2D6CDF"/><circle cx="172" cy="239" r="6" fill="#2D6CDF"/><circle cx="190" cy="239" r="6" fill="#2D6CDF"/><circle cx="208" cy="239" r="6" fill="#2D6CDF"/><circle cx="226" cy="239" r="6" fill="#2D6CDF"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 239 L268 239" marker-end="url(#m19p)"/><text class="mini" x="324" y="214">parcels</text><rect class="parcel" x="278" y="224" width="44" height="30" rx="8"/><circle cx="291" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="309" cy="239" r="5.5" fill="#2D6CDF"/><rect class="parcel" x="328" y="224" width="44" height="30" rx="8"/><circle cx="341" cy="239" r="5.5" fill="#2D6CDF"/><circle cx="359" cy="239" r="5.5" fill="#2D6CDF"/></g>
  <g class="k k-disp"><path class="ln" d="M382 239 L427 239" marker-end="url(#m19p)"/></g>
  <g class="k k-dag"><path class="ln" d="M202.0 268 L202.0 299" marker-end="url(#m19p)"/><text class="edge-lbl" x="214.0" y="291">edge feeder</text></g>
  <g class="k k-tf c-merge"><rect class="tile" x="22" y="304" width="360" height="70" rx="14"/><text class="box-lbl" x="80" y="346.0">Merge</text></g>
  <g class="k k-in"><text class="mini" x="190" y="320">inputs</text><rect class="pool" x="138" y="328" width="104" height="34" rx="17"/><circle cx="154" cy="345" r="6" fill="#E8810B"/><circle cx="172" cy="345" r="6" fill="#E8810B"/><circle cx="190" cy="345" r="6" fill="#E8810B"/><circle cx="208" cy="345" r="6" fill="#E8810B"/><circle cx="226" cy="345" r="6" fill="#E8810B"/></g>
  <g class="k k-pack"><path class="ln thin" d="M250 345 L268 345" marker-end="url(#m19p)"/><text class="mini" x="324" y="320">parcels</text><rect class="parcel" x="278" y="330" width="44" height="30" rx="8"/><circle cx="291" cy="345" r="5.5" fill="#E8810B"/><circle cx="309" cy="345" r="5.5" fill="#E8810B"/><rect class="parcel" x="328" y="330" width="44" height="30" rx="8"/><circle cx="341" cy="345" r="5.5" fill="#E8810B"/><circle cx="359" cy="345" r="5.5" fill="#E8810B"/></g>
  <g class="k k-disp"><path class="ln" d="M382 345 L427 345" marker-end="url(#m19p)"/></g>
  <g class="k k-out"><path class="ln" d="M202.0 374 L202.0 418" marker-end="url(#m19p)"/><g class="out-g"><rect class="pill" x="132.0" y="422" width="140" height="34" rx="17.0"/><text class="pill-lbl" x="202.0" y="445.0">dataset</text></g></g>
</svg>

</div>
</div>

---

# Written down as CWL

- A workgraph is a **CWL document** ([DX-ADR-007](https://github.com/DIRACGrid/diracx/pull/1042))
    - Its dataflow declares how transformations chain
    - Inputs arriving from outside carry the metadata queries that tell the feeder what to fetch
- User jobs, workgraphs and transformations: all the same kind of document
- **Ryun will cover this next**

---

# Workgraph state machine (idealised)

<svg class="flow " style="max-width: 1160px" viewBox="0 0 1160 330" role="img" aria-label="Idealised workgraph state machine: New, Scouting, Approving, Active, Finalizing, Completed, Archiving, Archived; Cancelling then Cleaned from any earlier state">
  <defs><marker id="m20p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m20t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m20n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m20r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m20g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m20a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="st-big"><rect class="st" x="20" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="120.0" y="62">New</text></g>
  <path class="ln" d="M224 55 L300 55" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st" x="306" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="406.0" y="62">Scouting</text></g>
  <path class="ln" d="M510 55 L586 55" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st" x="592" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="692.0" y="62">Approving</text></g>
  <path class="ln" d="M796 55 L872 55" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st lit" x="878" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="978.0" y="62">Active</text></g>
  <g class="st-big"><rect class="st" x="20" y="170" width="200" height="50" rx="25"/><text class="st-lbl big" x="120.0" y="202">Finalizing</text></g>
  <path class="ln" d="M224 195 L300 195" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st" x="306" y="170" width="200" height="50" rx="25"/><text class="st-lbl big" x="406.0" y="202">Completed</text></g>
  <path class="ln" d="M510 195 L586 195" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st" x="592" y="170" width="200" height="50" rx="25"/><text class="st-lbl big" x="692.0" y="202">Archiving</text></g>
  <path class="ln" d="M796 195 L872 195" marker-end="url(#m20p)"/>
  <g class="st-big"><rect class="st" x="878" y="170" width="200" height="50" rx="25"/><text class="st-lbl big" x="978.0" y="202">Archived</text></g>
  <path class="ln" d="M978.0 80 Q 978.0 140 306 140 Q 120.0 140 120.0 164" marker-end="url(#m20p)"/>
  <text class="lbl" x="632" y="132" text-anchor="middle">every member drained</text>
  <path class="ln dash" d="M692.0 30 Q 592 4 412.0 26" marker-end="url(#m20p)"/>
  <text class="lbl" x="549" y="14" text-anchor="middle">scout further</text>
  <g class="st-big"><rect class="st cancel" x="592" y="260" width="200" height="46" rx="23"/><text class="st-lbl big" x="692.0" y="290">Cancelling</text></g>
  <g class="st-big"><rect class="st cancel" x="878" y="260" width="200" height="46" rx="23"/><text class="st-lbl big" x="978.0" y="290">Cleaned</text></g>
  <path class="ln" d="M796 283 L872 283" marker-end="url(#m20p)"/>
  <text class="lbl" x="578" y="288" text-anchor="end">operator, from any state before Completed →</text>
</svg>

---

# Hooks and actions

- **Hooks** run while in a state and return what should change: feeder arguments, pause, retry an input
- **Actions** are ordered lists of checks and steps, each recording `Passed`, `Failed` or `Pending`
- **Plugins propose, the core writes**

<svg class="flow " style="max-width: 1160px" viewBox="0 0 1160 400" role="img" aria-label="Idealised workgraph state machine: New, Scouting, Approving, Active, Finalizing, Completed, Archiving, Archived; Cancelling then Cleaned from any earlier state; with the hooks and actions that run in each state">
  <defs><marker id="m21p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m21t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m21n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m21r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m21g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m21a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="st-big"><rect class="st" x="20" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="120.0" y="62">New</text></g>
  <path class="ln" d="M224 55 L300 55" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st" x="306" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="406.0" y="62">Scouting</text></g>
  <path class="ln" d="M510 55 L586 55" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st" x="592" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="692.0" y="62">Approving</text></g>
  <path class="ln" d="M796 55 L872 55" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st lit" x="878" y="30" width="200" height="50" rx="25"/><text class="st-lbl big" x="978.0" y="62">Active</text></g>
  <g class="st-big"><rect class="st" x="20" y="200" width="200" height="50" rx="25"/><text class="st-lbl big" x="120.0" y="232">Finalizing</text></g>
  <path class="ln" d="M224 225 L300 225" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st" x="306" y="200" width="200" height="50" rx="25"/><text class="st-lbl big" x="406.0" y="232">Completed</text></g>
  <path class="ln" d="M510 225 L586 225" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st" x="592" y="200" width="200" height="50" rx="25"/><text class="st-lbl big" x="692.0" y="232">Archiving</text></g>
  <path class="ln" d="M796 225 L872 225" marker-end="url(#m21p)"/>
  <g class="st-big"><rect class="st" x="878" y="200" width="200" height="50" rx="25"/><text class="st-lbl big" x="978.0" y="232">Archived</text></g>
  <path class="ln" d="M978.0 80 Q 978.0 170 306 170 Q 120.0 170 120.0 194" marker-end="url(#m21p)"/>
  <text class="lbl" x="632" y="146" text-anchor="middle">every member drained</text>
  <path class="ln dash" d="M692.0 30 Q 592 4 412.0 26" marker-end="url(#m21p)"/>
  <text class="lbl" x="549" y="14" text-anchor="middle">scout further</text>
  <g class="st-big"><rect class="st cancel" x="592" y="290" width="200" height="46" rx="23"/><text class="st-lbl big" x="692.0" y="320">Cancelling</text></g>
  <g class="st-big"><rect class="st cancel" x="878" y="290" width="200" height="46" rx="23"/><text class="st-lbl big" x="978.0" y="320">Cleaned</text></g>
  <path class="ln" d="M796 313 L872 313" marker-end="url(#m21p)"/>
  <text class="lbl" x="578" y="318" text-anchor="end">operator, from any state before Completed →</text>
  <g class="chip hook-c"><rect class="chip" x="274.5" y="88" width="263.0" height="30" rx="15"/><text class="chip-lbl" x="406.0" y="108">hook: ScoutingToApproving</text></g>
  <g class="chip act-c"><rect class="chip" x="602.8" y="88" width="178.4" height="30" rx="15"/><text class="chip-lbl" x="692.0" y="108">actions: approve</text></g>
  <g class="chip hook-c"><rect class="chip" x="842.4" y="88" width="291.2" height="30" rx="15"/><text class="chip-lbl" x="988.0" y="108">hooks: Active · failed input</text></g>
  <g class="chip act-c"><rect class="chip" x="35.5" y="258" width="169.0" height="30" rx="15"/><text class="chip-lbl" x="120.0" y="278">actions: checks</text></g>
  <g class="chip act-c"><rect class="chip" x="602.8" y="258" width="178.4" height="30" rx="15"/><text class="chip-lbl" x="692.0" y="278">actions: tidy up</text></g>
  <g class="chip act-c"><rect class="chip" x="612.2" y="344" width="159.6" height="30" rx="15"/><text class="chip-lbl" x="692.0" y="364">actions: clean</text></g>
</svg>

---

<!-- _class: section -->

# Does it do everything we need?

---

# Composing the pieces

- Everything so far **composes**: any number of transformations, any shape of graph
- Each use case changes only:
    - the shape of the graph
    - which feeder, packer, hooks and actions are plugged in
- Next: the two generic graphs again, with the **additions in pink**

---

# Scouting

<div class="cols">
<div>

- Run on a **small sample** first
    - Does the configuration work? What does it need?
- A **hook** decides when the scout is done
- Approved → the feeder's limits are lifted
    - Nothing the scout produced is redone
- Not convinced? **Scout further**

</div>
<div>

<svg class="flow " style="max-width: 520px" viewBox="0 0 520 470" role="img" aria-label="Simulation workgraph with a state strip Scouting, Approving, Active, Scouting lit; the seed feeder yields a small scouting sample first">
  <defs><marker id="m22p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m22t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m22n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m22r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m22g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m22a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <rect class="st lit" x="2" y="4" width="150" height="30" rx="15"/><text class="st-lbl lit" x="77.0" y="24">Scouting</text><path class="ln" d="M154 19 L168 19" marker-end="url(#m22p)"/><rect class="st" x="174" y="4" width="150" height="30" rx="15"/><text class="st-lbl" x="249.0" y="24">Approving</text><path class="ln" d="M326 19 L340 19" marker-end="url(#m22p)"/><rect class="st" x="346" y="4" width="150" height="30" rx="15"/><text class="st-lbl" x="421.0" y="24">Active</text>
  <g class="wg-g"><rect class="wgbox" x="10" y="106" width="330" height="280" rx="18"/><text class="prod-lbl" x="24" y="126">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="90" y="58" width="170" height="34" rx="17.0"/><text class="src-lbl" x="175.0" y="81.0">seeds</text></g>
  <path class="ln feed" d="M175 92 L175 129" marker-end="url(#m22t)"/>
  <g class="c-sim"><rect class="tile" x="90.0" y="134" width="170" height="50" rx="12"/><text class="box-lbl" x="175.0" y="166.0">Produce</text></g>
  <path class="ln" d="M175 184 L175 219" marker-end="url(#m22p)"/>
  <g class="c-reco"><rect class="tile" x="90.0" y="224" width="170" height="50" rx="12"/><text class="box-lbl" x="175.0" y="256.0">Process</text></g>
  <path class="ln" d="M175 274 L175 309" marker-end="url(#m22p)"/>
  <g class="c-merge"><rect class="tile" x="90.0" y="314" width="170" height="50" rx="12"/><text class="box-lbl" x="175.0" y="346.0">Merge</text></g>
  <path class="ln" d="M175 364 L175 410" marker-end="url(#m22p)"/>
  <g class="out-g"><rect class="pill" x="110" y="414" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="175.0" y="437.0">dataset</text></g>
  <text class="nw-lbl" x="400" y="118" text-anchor="middle">scout: 100 seeds</text>
  <text class="nw-lbl" x="400" y="140" text-anchor="middle">then: the rest</text>
  <path class="ln nw" d="M318 128 L268 118" marker-end="url(#m22n)"/>
</svg>

</div>
</div>

---

# Resource estimation

<div class="cols">
<div>

- Just an **approving action**
- Measures CPU, memory and disk from the scout
- Writes the needs back into each transformation's **requirements**
- Too high? The action fails, a human looks

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 420" role="img" aria-label="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
  <defs><marker id="m23p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m23t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m23n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m23r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m23g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m23a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="6" y="54" width="228" height="280" rx="18"/><text class="prod-lbl" x="20" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="35" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="120.0" y="29.0">seeds</text></g>
  <path class="ln feed" d="M120 40 L120 77" marker-end="url(#m23t)"/>
  <g class="c-sim"><rect class="tile" x="35.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="114.0">Produce</text></g>
  <path class="ln" d="M120 132 L120 167" marker-end="url(#m23p)"/>
  <g class="c-reco"><rect class="tile" x="35.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="204.0">Process</text></g>
  <path class="ln" d="M120 222 L120 257" marker-end="url(#m23p)"/>
  <g class="c-merge"><rect class="tile" x="35.0" y="262" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="294.0">Merge</text></g>
  <path class="ln" d="M120 312 L120 358" marker-end="url(#m23p)"/>
  <g class="out-g"><rect class="pill" x="55" y="362" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="120.0" y="385.0">dataset</text></g>
  <rect class="container" x="286" y="36" width="274" height="266" rx="16"/>
  <text class="job-lbl" x="300" y="58">APPROVING ACTIONS</text>
  <g class="c-gen"><rect class="act" x="300" y="70" width="246" height="40" rx="10"/><text class="act-n" x="320" y="96">1</text><text class="act-lbl" x="340" y="96">Success rate</text></g>
  <path class="ln thin" d="M423 110 L423 122"/>
  <g class="nw"><rect class="act" x="300" y="124" width="246" height="40" rx="10"/><text class="act-n" x="320" y="150">2</text><text class="act-lbl" x="340" y="150">Resource estimate</text></g>
  <path class="ln thin" d="M423 164 L423 176"/>
  <g class="c-gen"><rect class="act" x="300" y="178" width="246" height="40" rx="10"/><text class="act-n" x="320" y="204">3</text><text class="act-lbl" x="340" y="204">PPG approval</text></g>
  <path class="ln thin" d="M423 218 L423 230"/>
  <g class="c-gen"><rect class="act" x="300" y="232" width="246" height="40" rx="10"/><text class="act-n" x="320" y="258">4</text><text class="act-lbl" x="340" y="258">Manual sign-off</text></g>
  <path class="ln nw" d="M300 144 Q 262 144 210 197" marker-end="url(#m23n)"/>
  <text class="nw-lbl" x="262" y="176" text-anchor="middle" style="font-size:12px">requirements</text>
</svg>

</div>
</div>

---

# PPG approval

<div class="cols">
<div>

- Another approving action
    - LHCb's, so it lives in an extension
- Usage scaled to the full request exceeds what was approved?
    - Flag it for a second approval
- A sign-off = forcing a failed action to `Passed`

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 420" role="img" aria-label="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
  <defs><marker id="m24p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m24t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m24n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m24r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m24g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m24a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="6" y="54" width="228" height="280" rx="18"/><text class="prod-lbl" x="20" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="35" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="120.0" y="29.0">seeds</text></g>
  <path class="ln feed" d="M120 40 L120 77" marker-end="url(#m24t)"/>
  <g class="c-sim"><rect class="tile" x="35.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="114.0">Produce</text></g>
  <path class="ln" d="M120 132 L120 167" marker-end="url(#m24p)"/>
  <g class="c-reco"><rect class="tile" x="35.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="204.0">Process</text></g>
  <path class="ln" d="M120 222 L120 257" marker-end="url(#m24p)"/>
  <g class="c-merge"><rect class="tile" x="35.0" y="262" width="170" height="50" rx="12"/><text class="box-lbl" x="120.0" y="294.0">Merge</text></g>
  <path class="ln" d="M120 312 L120 358" marker-end="url(#m24p)"/>
  <g class="out-g"><rect class="pill" x="55" y="362" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="120.0" y="385.0">dataset</text></g>
  <rect class="container" x="286" y="36" width="274" height="266" rx="16"/>
  <text class="job-lbl" x="300" y="58">APPROVING ACTIONS</text>
  <g class="c-gen"><rect class="act" x="300" y="70" width="246" height="40" rx="10"/><text class="act-n" x="320" y="96">1</text><text class="act-lbl" x="340" y="96">Success rate</text></g>
  <path class="ln thin" d="M423 110 L423 122"/>
  <g class="c-gen"><rect class="act" x="300" y="124" width="246" height="40" rx="10"/><text class="act-n" x="320" y="150">2</text><text class="act-lbl" x="340" y="150">Resource estimate</text></g>
  <path class="ln thin" d="M423 164 L423 176"/>
  <g class="nw"><rect class="act" x="300" y="178" width="246" height="40" rx="10"/><text class="act-n" x="320" y="204">3</text><text class="act-lbl" x="340" y="204">PPG approval</text></g>
  <path class="ln thin" d="M423 218 L423 230"/>
  <g class="nw"><rect class="act" x="300" y="232" width="246" height="40" rx="10"/><text class="act-n" x="320" y="258">4</text><text class="act-lbl" x="340" y="258">Manual sign-off</text></g>
  <text class="nw-lbl" x="423" y="320" text-anchor="middle">too much? → second approval</text>
</svg>

</div>
</div>

---

# Keeping intermediate files

<div class="cols">
<div>

- By default intermediate outputs are **transient**
    - Removed by the consuming job, or by a removal transformation
- Want to keep one? **Declare it as an output** of the workgraph
    - Anything kept has to be registered somewhere
- Neither consumed nor declared? Rejected at submission

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 420" role="img" aria-label="Simulation workgraph where the Process output is also declared as a workgraph output and kept as a second dataset">
  <defs><marker id="m25p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m25t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m25n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m25r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m25g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m25a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="300" height="280" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="65" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="150.0" y="29.0">seeds</text></g>
  <path class="ln feed" d="M150 40 L150 77" marker-end="url(#m25t)"/>
  <g class="c-sim"><rect class="tile" x="65.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="114.0">Produce</text></g>
  <path class="ln" d="M150 132 L150 167" marker-end="url(#m25p)"/>
  <g class="c-reco"><rect class="tile" x="65.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="204.0">Process</text></g>
  <path class="ln" d="M150 222 L150 257" marker-end="url(#m25p)"/>
  <g class="c-merge"><rect class="tile" x="65.0" y="262" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="294.0">Merge</text></g>
  <path class="ln" d="M150 312 L150 358" marker-end="url(#m25p)"/>
  <g class="out-g"><rect class="pill" x="85" y="362" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="150.0" y="385.0">dataset</text></g>
  <path class="ln nw" d="M235.0 197.0 L400 197.0 L400 358" marker-end="url(#m25n)"/>
  <g class="nw"><rect class="pill" x="335" y="362" width="150" height="34" rx="17"/><text class="pill-lbl" x="410" y="385">intermediate</text></g>
  <text class="nw-lbl" x="410" y="185.0" text-anchor="middle">declared output</text>
</svg>

</div>
</div>

---

# Multiple steps per job

<div class="cols">
<div>

- A transformation runs a CWL **process**
    - One tool, or a **workflow** of several
- e.g. reconstruction and filtering in one job
    - No intermediate file to register or clean up
- Same transformation, same parcels

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 420" role="img" aria-label="Simulation workgraph whose Process transformation runs a two-step CWL workflow, Reco then Filter, inside one job">
  <defs><marker id="m26p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m26t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m26n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m26r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m26g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m26a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="340" height="280" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="85" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="170.0" y="29.0">seeds</text></g>
  <path class="ln feed" d="M170 40 L170 77" marker-end="url(#m26t)"/>
  <g class="c-sim"><rect class="tile" x="85.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="170.0" y="114.0">Produce</text></g>
  <path class="ln" d="M170 132 L170 167" marker-end="url(#m26p)"/>
  <path class="ln" d="M170 222 L170 257" marker-end="url(#m26p)"/>
  <g class="c-merge"><rect class="tile" x="85.0" y="262" width="170" height="50" rx="12"/><text class="box-lbl" x="170.0" y="294.0">Merge</text></g>
  <path class="ln" d="M170 312 L170 358" marker-end="url(#m26p)"/>
  <g class="out-g"><rect class="pill" x="105" y="362" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="170.0" y="385.0">dataset</text></g>
  <g class="mstep-grp"><path class="mfill c-reco" d="M170.0,172 L47.0,172 Q35.0,172 35.0,184 L35.0,210 Q35.0,222 47.0,222 L170.0,222 Z"/><path class="mfill c-filter" d="M170.0,172 L293.0,172 Q305.0,172 305.0,184 L305.0,210 Q305.0,222 293.0,222 L170.0,222 Z"/></g>
  <text class="box-lbl c-reco" x="102.5" y="204">Reco</text>
  <text class="box-lbl c-filter" x="237.5" y="204">Filter</text>
  <text class="nw-lbl" x="420.0" y="194" text-anchor="middle">one job,</text>
  <text class="nw-lbl" x="420.0" y="212" text-anchor="middle">two steps</text>
</svg>

</div>
</div>

---

# Histograms

<div class="cols">
<div>

- Every job also writes small files (monitoring histograms)
- Declare them as a **second output** of the step
- Then merge them:
    - with a **transformation** fed by that output, or
    - with a **finalizing action**, once, at the end
    - or both

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 340" role="img" aria-label="Processing workgraph where Process also emits histograms, merged by an extra histogram-merge transformation into a histograms output">
  <defs><marker id="m27p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m27t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m27n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m27r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m27g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m27a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="520" height="190" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="45" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="130.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M130 40 L130 77" marker-end="url(#m27t)"/>
  <g class="c-reco"><rect class="tile" x="45.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="130.0" y="114.0">Process</text></g>
  <path class="ln" d="M130 132 L130 167" marker-end="url(#m27p)"/>
  <g class="c-merge"><rect class="tile" x="45.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="130.0" y="204.0">Merge</text></g>
  <path class="ln" d="M130 222 L130 268" marker-end="url(#m27p)"/>
  <g class="out-g"><rect class="pill" x="65" y="272" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="130.0" y="295.0">dataset</text></g>
  <path class="ln nw" d="M215.0 107.0 L415 107.0 L415 167" marker-end="url(#m27n)"/>
  <text class="nw-lbl" x="425" y="97.0" text-anchor="start">histograms</text>
  <text class="nw-lbl" x="425" y="97.0" text-anchor="start"></text>
  <g class="nw"><rect class="tile" x="330" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="415.0" y="204.0">Hist merge</text></g>
  <path class="ln nw" d="M415 222 L415 268" marker-end="url(#m27n)"/>
  <g class="nw"><rect class="pill" x="350" y="272" width="130" height="34" rx="17"/><text class="pill-lbl" x="415" y="295">histograms</text></g>
</svg>

</div>
</div>

---

# Processing outputs multiple times

<div class="cols">
<div>

- One output, **many consumers**
- Each consumer keeps its own bookmark
    - A fan-out costs nothing
    - A consumer can be added later

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 340" role="img" aria-label="Processing workgraph where the Process output feeds both Merge and an extra Selection transformation with its own output">
  <defs><marker id="m28p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m28t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m28n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m28r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m28g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m28a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="520" height="190" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="45" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="130.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M130 40 L130 77" marker-end="url(#m28t)"/>
  <g class="c-reco"><rect class="tile" x="45.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="130.0" y="114.0">Process</text></g>
  <path class="ln" d="M130 132 L130 167" marker-end="url(#m28p)"/>
  <g class="c-merge"><rect class="tile" x="45.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="130.0" y="204.0">Merge</text></g>
  <path class="ln" d="M130 222 L130 268" marker-end="url(#m28p)"/>
  <g class="out-g"><rect class="pill" x="65" y="272" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="130.0" y="295.0">dataset</text></g>
  <path class="ln nw" d="M215.0 107.0 L415 107.0 L415 167" marker-end="url(#m28n)"/>
  <g class="nw"><rect class="tile" x="330" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="415.0" y="204.0">Selection</text></g>
  <path class="ln nw" d="M415 222 L415 268" marker-end="url(#m28n)"/>
  <g class="nw"><rect class="pill" x="350" y="272" width="130" height="34" rx="17"/><text class="pill-lbl" x="415" y="295">selected</text></g>
</svg>

</div>
</div>

---

# Correlated processing (RDST)

<div class="cols">
<div>

- An RDST has to be processed with its **RAW ancestor**
- The pool holds only RDSTs
    - The **packer** looks up each ancestor and adds it to the parcel
    - …and delays the RDST until both are staged
- Joining two outputs of one workgraph is the same shape

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 340" role="img" aria-label="Processing workgraph fed by an RDST query; the Process packer looks up each RDST&#x27;s RAW ancestor in the bookkeeping and adds it to the parcel">
  <defs><marker id="m29p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m29t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m29n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m29r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m29g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m29a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="300" height="190" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="65" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="150.0" y="29.0">RDST query</text></g>
  <path class="ln feed" d="M150 40 L150 77" marker-end="url(#m29t)"/>
  <g class="c-reco"><rect class="tile" x="65.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="114.0">Process</text></g>
  <path class="ln" d="M150 132 L150 167" marker-end="url(#m29p)"/>
  <g class="c-merge"><rect class="tile" x="65.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="204.0">Merge</text></g>
  <path class="ln" d="M150 222 L150 268" marker-end="url(#m29p)"/>
  <g class="out-g"><rect class="pill" x="85" y="272" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="150.0" y="295.0">dataset</text></g>
  <g class="nw"><path class="dbc" d="M410 84 L410 130 A55.0 8 0 0 0 520 130 L520 84 A55.0 8 0 0 0 410 84 Z"/><ellipse class="dbc" cx="465.0" cy="84" rx="55.0" ry="8"/><text class="db-lbl" x="465.0" y="117.0">bookkeeping</text></g>
  <path class="ln nw dash" d="M410 107 L240.0 107" marker-end="url(#m29n)"/>
  <text class="nw-lbl" x="372" y="72" text-anchor="middle">RAW ancestor</text>
  <g class="nw"><rect class="parcel" x="332" y="120" width="66" height="26" rx="8"/><text class="mini" x="365" y="138" style="fill:#C0398B">RDST+RAW</text></g>
</svg>

</div>
</div>

---

# Single outputs

<div class="cols">
<div>

- Want **one** file at the end?
- The packer knows whether its feeder is still running
    - Hold everything back until upstream is done
    - Then pack it all into one parcel
- Or: a finalizing action

</div>
<div>

<svg class="flow " style="max-width: 540px" viewBox="0 0 540 340" role="img" aria-label="Processing workgraph whose Merge packer waits for its feeder to finish and packs everything into one parcel, giving a single output file">
  <defs><marker id="m30p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m30t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m30n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m30r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m30g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m30a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="300" height="190" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="65" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="150.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M150 40 L150 77" marker-end="url(#m30t)"/>
  <g class="c-reco"><rect class="tile" x="65.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="114.0">Process</text></g>
  <path class="ln" d="M150 132 L150 167" marker-end="url(#m30p)"/>
  <g class="c-merge"><rect class="tile" x="65.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="204.0">Merge</text></g>
  <path class="ln" d="M150 222 L150 268" marker-end="url(#m30p)"/>
  <g class="nw"><rect class="pill" x="85" y="272" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="150.0" y="295.0">1 file</text></g>
  <path class="ln nw" d="M335.0 197.0 L241.0 197.0" marker-end="url(#m30n)"/>
  <text class="nw-lbl" x="343.0" y="181.0" text-anchor="start">packer: wait until</text>
  <text class="nw-lbl" x="343.0" y="199.0" text-anchor="start">upstream is done,</text>
  <text class="nw-lbl" x="343.0" y="217.0" text-anchor="start">then one parcel</text>
</svg>

</div>
</div>

---

# Many outputs

<div class="cols">
<div>

- One step, several **file types**
- A consumer takes **one type**
    - One merge per type
- Every output is consumed or declared

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 340" role="img" aria-label="Processing workgraph where Process emits three file types, each consumed by its own Merge and delivered as its own dataset">
  <defs><marker id="m31p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m31t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m31n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m31r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m31g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m31a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="6" y="54" width="548" height="206" rx="18"/><text class="prod-lbl" x="20" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="195" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="280.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M280 40 L280 77" marker-end="url(#m31t)"/>
  <g class="c-reco"><rect class="tile" x="195" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="280.0" y="114.0">Process</text></g>
  <path class="ln nw" d="M280 132 L102 167" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="tile" x="22" y="172" width="160" height="50" rx="12"/><text class="box-lbl" x="102.0" y="204.0">Merge ●</text></g>
  <path class="ln nw" d="M102 222 L102 279" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="pill" x="42" y="283" width="120" height="34" rx="17"/><text class="pill-lbl" x="102" y="306">type 1</text></g>
  <path class="ln nw" d="M280 132 L280 167" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="tile" x="200" y="172" width="160" height="50" rx="12"/><text class="box-lbl" x="280.0" y="204.0">Merge ▲</text></g>
  <path class="ln nw" d="M280 222 L280 279" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="pill" x="220" y="283" width="120" height="34" rx="17"/><text class="pill-lbl" x="280" y="306">type 2</text></g>
  <path class="ln nw" d="M280 132 L458 167" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="tile" x="378" y="172" width="160" height="50" rx="12"/><text class="box-lbl" x="458.0" y="204.0">Merge ◆</text></g>
  <path class="ln nw" d="M458 222 L458 279" marker-end="url(#m31n)"/>
  <g class="nw"><rect class="pill" x="398" y="283" width="120" height="34" rx="17"/><text class="pill-lbl" x="458" y="306">type 3</text></g>
</svg>

</div>
</div>

---

# Retrying

<div class="cols">
<div>

- A parcel is **never** retried, its **inputs** are
- A **hook** decides each failed input's fate:
    - back to `Unassigned`, and repacked (maybe differently)
    - or `Problematic`, for an operator
- Still processed exactly once, or not at all

</div>
<div>

<svg class="flow " style="max-width: 600px" viewBox="0 0 600 380" role="img" aria-label="Inside one transformation: a parcel fails, its inputs go to the HandleFailedInput hook, which returns them to the pool or quarantines them as Problematic">
  <defs><marker id="m32p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m32t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m32n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m32r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m32g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m32a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="c-reco"><rect class="tgroup" x="6" y="30" width="588" height="250" rx="16"/><text class="box-lbl" x="300" y="54">Process</text></g>
  <rect class="pool" x="30" y="80" width="130" height="46" rx="23"/>
  <circle cx="52" cy="103" r="6" fill="#2D6CDF"/>
  <circle cx="73" cy="103" r="6" fill="#2D6CDF"/>
  <circle cx="94" cy="103" r="6" fill="#2D6CDF"/>
  <circle cx="115" cy="103" r="6" fill="#2D6CDF"/>
  <circle cx="136" cy="103" r="6" fill="#2D6CDF"/>
  <text class="mini" x="95" y="74">inputs</text>
  <path class="ln" d="M160 103 L230 103" marker-end="url(#m32p)"/>
  <text class="mini" x="195" y="92">packer</text>
  <rect class="parcel" x="236" y="86" width="64" height="34" rx="8"/>
  <circle cx="254" cy="103" r="5.5" fill="#2D6CDF"/><circle cx="282" cy="103" r="5.5" fill="#2D6CDF"/>
  <path class="ln" d="M300 103 L360 103" marker-end="url(#m32p)"/>
  <g class=""><rect class="step" x="366" y="80" width="170" height="46" rx="12" style="fill:#FBEAE8;stroke:#C0392B"/><text class="box-lbl" x="451" y="110" style="fill:#C0392B">job ✗</text></g>
  <path class="ln" d="M451 126 L451 176" style="stroke:#C0392B" marker-end="url(#m32r)"/>
  <g class="hook-g"><rect class="hook" x="356" y="182" width="190" height="46" rx="12"/><text class="hook-lbl" x="451" y="211">HandleFailedInput</text></g>
  <path class="ln feed" d="M356 205 Q 95 205 95 131" marker-end="url(#m32t)"/>
  <text class="feed-lbl" x="220" y="238" text-anchor="middle">retry → Unassigned</text>
  <path class="ln dash" d="M451 228 L451 300" style="stroke:#C0392B" marker-end="url(#m32r)"/>
  <g class=""><rect class="pill" x="376" y="306" width="150" height="40" rx="20" style="stroke:#C0392B"/><text class="pill-lbl" x="451" y="332" style="fill:#C0392B">Problematic</text></g>
  <text class="lbl" x="451" y="366" text-anchor="middle">waits for an operator</text>
  <text class="lbl" x="320" y="96"></text>
</svg>

</div>
</div>

---

# Splitting

<div class="cols">
<div>

- A job processed **part** of its input
    - The CMS case: some luminosity sections of a file
- The parent becomes `Split`
    - the processed part → a `Processed` child
    - the rest → an `Unassigned` child, packed again
- Children keep their parent's file and lineage

</div>
<div>

<svg class="flow " style="max-width: 600px" viewBox="0 0 600 330" role="img" aria-label="A parcel processes only part of its input file: the parent input becomes Split, the processed part a Processed child, the rest an Unassigned child back in the pool">
  <defs><marker id="m33p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m33t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m33n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m33r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m33g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m33a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <rect class="pill" x="10" y="30" width="200" height="40" rx="20"/>
  <text class="pill-lbl" x="110" y="56">file · lumis 1–100</text>
  <path class="ln" d="M210 50 L262 50" marker-end="url(#m33p)"/>
  <g class=""><rect class="step" x="268" y="28" width="160" height="44" rx="12" style="fill:#FDF3DF;stroke:#D98E04"/><text class="box-lbl" x="348" y="57" style="fill:#D98E04">job: partial</text></g>
  <text class="nw-lbl" x="110" y="104" text-anchor="middle">parent → Split</text>
  <path class="ln thin" d="M110 70 L110 88"/>
  <path class="ln" d="M110 112 Q 110 160 60 196" style="stroke:#1F9D55" marker-end="url(#m33g)"/>
  <path class="ln" d="M110 112 Q 110 160 300 196" style="stroke:#D98E04" marker-end="url(#m33a)"/>
  <g class=""><rect class="pill" x="10" y="200" width="170" height="40" rx="20" style="fill:#E4F3EB;stroke:#1F9D55"/><text class="pill-lbl" x="95" y="226" style="fill:#1F9D55">lumis 1–60</text></g>
  <text class="lbl" x="95" y="262" text-anchor="middle">Processed</text>
  <g class=""><rect class="pill" x="220" y="200" width="170" height="40" rx="20" style="fill:#FDF3DF;stroke:#D98E04"/><text class="pill-lbl" x="305" y="226" style="fill:#D98E04">lumis 61–100</text></g>
  <text class="lbl" x="305" y="262" text-anchor="middle">Unassigned → repacked</text>
  <path class="ln dash" d="M390 220 Q 520 220 520 120 Q 520 50 436 50" style="stroke:#D98E04" marker-end="url(#m33a)"/>
  <text class="lbl" x="508" y="140" text-anchor="end">next parcel</text>
</svg>

</div>
</div>

---

# Staging input

<div class="cols">
<div>

- Raw data lives on **tape**
- A **data transformation** stages it to a buffer
    - Shares the processing step's query
- The processing **packer delays** each file until its replica exists
    - Delay isn't a state, the input just waits in the pool

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 340" role="img" aria-label="Processing workgraph with a staging data transformation sharing its query; the Process packer delays each file until its staged replica exists">
  <defs><marker id="m34p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m34t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m34n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m34r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m34g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m34a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="10" y="54" width="540" height="190" rx="18"/><text class="prod-lbl" x="24" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="65" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="150.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M150 40 L150 77" marker-end="url(#m34t)"/>
  <g class="c-reco"><rect class="tile" x="65.0" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="114.0">Process</text></g>
  <path class="ln" d="M150 132 L150 167" marker-end="url(#m34p)"/>
  <g class="c-merge"><rect class="tile" x="65.0" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="150.0" y="204.0">Merge</text></g>
  <path class="ln" d="M150 222 L150 268" marker-end="url(#m34p)"/>
  <g class="out-g"><rect class="pill" x="85" y="272" width="130" height="34" rx="17.0"/><text class="pill-lbl" x="150.0" y="295.0">dataset</text></g>
  <path class="ln feed" d="M235 23 Q 425 23 425 77" marker-end="url(#m34t)"/>
  <g class="nw"><rect class="tile data" x="340" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="425.0" y="106.0">Stage</text><text class="tsub2" x="425.0" y="123.0">tape → buffer</text></g>
  <path class="ln nw dash" d="M340 107 L240.0 107.0" marker-end="url(#m34n)"/>
  <text class="nw-lbl" x="288" y="154" text-anchor="middle">delay until staged</text>
</svg>

</div>
</div>

---

# Removing replicas after N uses

<div class="cols">
<div>

- A **removal** transformation, fed by the same output
- Its packer delays each file until **all N consumers** have processed it
- A file a consumer wrote off stays, so someone can look at it
- Same pattern for buffer copies after staging

</div>
<div>

<svg class="flow " style="max-width: 560px" viewBox="0 0 560 340" role="img" aria-label="Processing workgraph where Process feeds Merge and a Selection, and a removal data transformation fed by the same output waits until both have processed each file">
  <defs><marker id="m35p" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker><marker id="m35t" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#138D8D"/></marker><marker id="m35n" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0398B"/></marker><marker id="m35r" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker><marker id="m35g" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#1F9D55"/></marker><marker id="m35a" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#D98E04"/></marker></defs>
  <g class="wg-g"><rect class="wgbox" x="6" y="54" width="548" height="206" rx="18"/><text class="prod-lbl" x="20" y="74">WORKGRAPH</text></g>
  <g class="src-g"><rect class="src" x="25" y="6" width="170" height="34" rx="17.0"/><text class="src-lbl" x="110.0" y="29.0">metadata query</text></g>
  <path class="ln feed" d="M110 40 L110 77" marker-end="url(#m35t)"/>
  <g class="c-reco"><rect class="tile" x="25" y="82" width="170" height="50" rx="12"/><text class="box-lbl" x="110.0" y="114.0">Process</text></g>
  <path class="ln" d="M110 132 L110 167" marker-end="url(#m35p)"/>
  <g class="c-merge"><rect class="tile" x="25" y="172" width="170" height="50" rx="12"/><text class="box-lbl" x="110.0" y="204.0">Merge</text></g>
  <path class="ln" d="M195 118 Q 295 118 295 167" marker-end="url(#m35p)"/>
  <g class="c-filter"><rect class="tile" x="220" y="172" width="150" height="50" rx="12"/><text class="box-lbl" x="295.0" y="204.0">Selection</text></g>
  <path class="ln nw" d="M195 96 L465 96 L465 167" marker-end="url(#m35n)"/>
  <g class="nw"><rect class="tile data" x="390" y="172" width="150" height="50" rx="12"/><text class="box-lbl" x="465.0" y="196.0">Remove</text><text class="tsub2" x="465.0" y="213.0">data transformation</text></g>
  <path class="ln nw dash" d="M370 197 L 384 197" marker-end="url(#m35n)"/>
  <path class="ln nw dash" d="M190 222 Q 300 250 440 227" marker-end="url(#m35n)"/>
  <text class="nw-lbl" x="465" y="292" text-anchor="middle">after both</text>
  <text class="nw-lbl" x="465" y="310" text-anchor="middle">consumers (N = 2)</text>
  <path class="ln" d="M110 222 L110 279" marker-end="url(#m35p)"/>
  <g class="out-g"><rect class="pill" x="50" y="283" width="120" height="34" rx="17.0"/><text class="pill-lbl" x="110.0" y="306.0">dataset</text></g>
  <path class="ln" d="M295 222 L295 279" marker-end="url(#m35p)"/>
  <g class="out-g"><rect class="pill" x="235" y="283" width="120" height="34" rx="17.0"/><text class="pill-lbl" x="295.0" y="306.0">selected</text></g>
</svg>

</div>
</div>

---

# …and what did we miss?

- Have a use case that **doesn't** fit? We want to hear about it this week
- Bring it to the **transformation system** hackathon track

<!-- TODO: add the transformation system questions sent to attendees beforehand -->

---

<!-- _class: section -->

# Going further

---

<!-- _class: build -->

# Going further

- **Operations / transformation debugging**
    - Why is this input `Problematic`? Where did this file come from?
- **Monitoring**
    - Exact counters per state, and a log of every transition
- **Analysis-productions-style submission**
    - Declarative, CI-driven, tested before it's submitted
- **Deploying software**

---

<!-- _class: section -->

# Questions?

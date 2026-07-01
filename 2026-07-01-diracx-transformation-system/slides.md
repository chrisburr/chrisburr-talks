---
marp: true
theme: cburr
paginate: true
title: "DiracX production system"
subtitle: ""
author: "Chris Burr"
affiliation: "CERN"
event: "DiracX hackathon"
event_url: "https://indico.cern.ch/event/1668629/"
date: "2026-07-01"
description: ""
---

# Introduction

<!-- _class: build -->

- These slides aim to build a common understanding of:
     - What a production is?
     - How a production is split into transformations?
     - How to make use of these blocks in your own workflows.
- After the hackathon, an Architecture Design Review (ADR) will be prepared early in summer.
     - Once agreed upon, start development!

---

# DIRAC vs DiracX

- Here I show the intended production system in DiracX.
- The underpinnings are almost identical to the DIRAC Transformation System.
    - With lots of little tweaks based on experience and lessons learned.

<div style="display: flex; align-items: center; justify-content: center; gap: 60px; margin-top: var(--sp-7);">
  <img src="assets/dirac-logo.png" alt="DIRAC — the interware" style="height: 110px; width: auto;">
  <span style="font-family: var(--font-sans); font-weight: 700; font-size: 52px; color: var(--ink-soft); line-height: 1;">➜</span>
  <img src="assets/diracx-logo-square.svg" alt="DiracX" style="height: 150px; width: auto;">
</div>

---

<!-- _class: section -->

# Basic Workflow Management in DiracX

---

# Start with the basics

<!-- _class: overlay -->

<div class="cols">
<div>

- We have a black box that:
     - Might have input(s)
     - Produces output(s)

- For now we ignore any source of parallelism

</div>
<div>

<svg class="flow" style="max-width: 240px" viewBox="0 0 240 280" role="img" aria-label="A payload box with an optional dashed input and a solid output">
  <defs>
    <marker id="ahA" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <line class="ln dash" x1="120" y1="12" x2="120" y2="88" marker-end="url(#ahA)"/>
  <text class="lbl" x="134" y="54">input?</text>
  <g class="c-gen">
    <rect class="payload" x="54" y="96" width="132" height="84" rx="16"/>
    <text class="box-lbl" x="120" y="145">payload</text>
  </g>
  <line class="ln" x1="120" y1="188" x2="120" y2="266" marker-end="url(#ahA)"/>
  <text class="lbl" x="134" y="232">output</text>
</svg>

</div>
</div>

<!-- overlay -->

<p class="ov-title"><strong>Simple case:</strong> a simulation and a reconstruction</p>

<svg class="flow" viewBox="0 0 620 208" role="img" aria-label="A simulation payload produces simulated data with no input; a reconstruction payload turns raw data into reconstructed data">
  <defs>
    <marker id="ahB" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <text class="lbl" x="115" y="62" text-anchor="middle">(no input)</text>
  <g class="c-sim">
    <rect class="payload" x="210" y="30" width="128" height="56" rx="12"/>
    <text class="box-lbl" x="274" y="66">payload</text>
  </g>
  <line class="ln" x1="338" y1="58" x2="400" y2="58" marker-end="url(#ahB)"/>
  <rect class="pill" x="404" y="37" width="176" height="42" rx="21"/>
  <text class="pill-lbl" x="492" y="64">Simulated data</text>
  <rect class="pill" x="20" y="141" width="120" height="42" rx="21"/>
  <text class="pill-lbl" x="80" y="168">Raw data</text>
  <line class="ln" x1="140" y1="162" x2="210" y2="162" marker-end="url(#ahB)"/>
  <g class="c-reco">
    <rect class="payload" x="210" y="134" width="128" height="56" rx="12"/>
    <text class="box-lbl" x="274" y="170">payload</text>
  </g>
  <line class="ln" x1="338" y1="162" x2="400" y2="162" marker-end="url(#ahB)"/>
  <rect class="pill" x="404" y="141" width="200" height="42" rx="21"/>
  <text class="pill-lbl" x="504" y="168">Reconstructed data</text>
</svg>

<!-- overlay -->

<p class="ov-title"><strong>More complex:</strong> correlated inputs, many outputs</p>

<svg class="flow" viewBox="0 0 630 220" role="img" aria-label="Raw data and reconstructed data go into a payload which produces File A, File B and File C">
  <defs>
    <marker id="ahC" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="pill" x="10" y="46" width="120" height="42" rx="21"/>
  <text class="pill-lbl" x="70" y="73">Raw data</text>
  <rect class="pill" x="10" y="150" width="200" height="42" rx="21"/>
  <text class="pill-lbl" x="110" y="177">Reconstructed data</text>
  <path class="ln" d="M130 67 Q 222 67 290 104" marker-end="url(#ahC)"/>
  <path class="ln" d="M210 171 Q 252 171 290 138" marker-end="url(#ahC)"/>
  <g class="c-gen">
    <rect class="payload" x="290" y="92" width="132" height="58" rx="14"/>
    <text class="box-lbl" x="356" y="128">payload</text>
  </g>
  <path class="ln" d="M422 108 Q 462 108 500 66" marker-end="url(#ahC)"/>
  <line class="ln" x1="422" y1="121" x2="500" y2="121" marker-end="url(#ahC)"/>
  <path class="ln" d="M422 134 Q 462 134 500 176" marker-end="url(#ahC)"/>
  <rect class="pill" x="504" y="44" width="100" height="40" rx="20"/>
  <text class="pill-lbl" x="554" y="70">File A</text>
  <rect class="pill" x="504" y="101" width="100" height="40" rx="20"/>
  <text class="pill-lbl" x="554" y="127">File B</text>
  <rect class="pill" x="504" y="158" width="100" height="40" rx="20"/>
  <text class="pill-lbl" x="554" y="184">File C</text>
</svg>

---

# Two steps, one job

- Start with **one job** running two steps end-to-end:
     - **Sim:** simulate events - input is `count`, `seed`
     - **Reco:** reconstruct — processes Sim's output
- A step describes **how to run one program** (a command-line tool).

<svg class="flow" style="max-width: 560px" viewBox="0 0 510 184" role="img" aria-label="One job containing step 1 Sim feeding step 2 Reco, then an output">
  <defs>
    <marker id="ah1" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="container" x="20" y="42" width="346" height="116" rx="16"/>
  <text class="job-lbl" x="38" y="68">JOB 1</text>
  <g class="c-sim">
    <rect class="step" x="44" y="78" width="134" height="66" rx="12"/>
    <text class="step-hdr" x="111" y="100">Step 1</text>
    <text class="box-lbl" x="111" y="126">Sim</text>
  </g>
  <line class="ln" x1="180" y1="111" x2="216" y2="111" marker-end="url(#ah1)"/>
  <g class="c-reco">
    <rect class="step" x="216" y="78" width="134" height="66" rx="12"/>
    <text class="step-hdr" x="283" y="100">Step 2</text>
    <text class="box-lbl" x="283" y="126">Reco</text>
  </g>
  <line class="ln" x1="366" y1="111" x2="478" y2="111" marker-end="url(#ah1)"/>
  <text class="lbl" x="422" y="101" text-anchor="middle">output</text>
</svg>

---

# Splitting things up

- One job hits limits — **disk**, **CPU time**, **memory**.
- Split into steps which are abstract building blocks

<svg class="flow" style="max-width: 740px" viewBox="0 0 760 200" role="img" aria-label="Four building blocks with their input and output types on the arrows: Sim, Reco, Filter and Merge">
  <defs>
    <marker id="ah2" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <text class="lbl" x="59" y="38" text-anchor="middle">count, seed</text>
  <line class="ln" x1="0" y1="52" x2="118" y2="52" marker-end="url(#ah2)"/>
  <g class="c-sim">
    <rect class="job" x="120" y="26" width="96" height="52" rx="13"/>
    <text class="box-lbl" x="168" y="58">Sim</text>
  </g>
  <text class="lbl" x="275" y="38" text-anchor="middle">file(s)</text>
  <line class="ln" x1="216" y1="52" x2="334" y2="52" marker-end="url(#ah2)"/>
  <text class="lbl" x="459" y="38" text-anchor="middle">file(s)</text>
  <line class="ln" x1="400" y1="52" x2="518" y2="52" marker-end="url(#ah2)"/>
  <g class="c-reco">
    <rect class="job" x="520" y="26" width="96" height="52" rx="13"/>
    <text class="box-lbl" x="568" y="58">Reco</text>
  </g>
  <text class="lbl" x="675" y="38" text-anchor="middle">file(s)</text>
  <line class="ln" x1="616" y1="52" x2="734" y2="52" marker-end="url(#ah2)"/>
  <text class="lbl" x="59" y="146" text-anchor="middle">file(s)</text>
  <line class="ln" x1="0" y1="160" x2="118" y2="160" marker-end="url(#ah2)"/>
  <g class="c-filter">
    <rect class="job" x="120" y="134" width="96" height="52" rx="13"/>
    <text class="box-lbl" x="168" y="166">Filter</text>
  </g>
  <text class="lbl" x="275" y="146" text-anchor="middle">file(s)</text>
  <line class="ln" x1="216" y1="160" x2="334" y2="160" marker-end="url(#ah2)"/>
  <text class="lbl" x="459" y="146" text-anchor="middle">file(s)</text>
  <line class="ln" x1="400" y1="160" x2="518" y2="160" marker-end="url(#ah2)"/>
  <g class="c-merge">
    <rect class="job" x="520" y="134" width="96" height="52" rx="13"/>
    <text class="box-lbl" x="568" y="166">merge</text>
  </g>
  <text class="lbl" x="675" y="146" text-anchor="middle">file</text>
  <line class="ln" x1="616" y1="160" x2="734" y2="160" marker-end="url(#ah2)"/>
</svg>

---

# Parallelising the work

- **Many Sim jobs** feed each **Reco** → **Filter** branch.
- The branches **merge** into the final output.
- Each block in the diagram is a job

<svg class="flow" style="max-width: 800px" viewBox="0 0 790 244" role="img" aria-label="Two Sim jobs feed each of two Reco jobs, each followed by a Filter, both branches merging into one output">
  <defs>
    <marker id="ah3" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <g class="c-sim">
    <rect class="step" x="10" y="14" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="42">Sim 1</text>
    <rect class="step" x="10" y="66" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="94">Sim 2</text>
    <rect class="step" x="10" y="138" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="166">Sim 3</text>
    <rect class="step" x="10" y="190" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="218">Sim 4</text>
  </g>
  <line class="ln" x1="114" y1="36" x2="178" y2="54" marker-end="url(#ah3)"/>
  <line class="ln" x1="114" y1="88" x2="178" y2="70" marker-end="url(#ah3)"/>
  <line class="ln" x1="114" y1="160" x2="178" y2="178" marker-end="url(#ah3)"/>
  <line class="ln" x1="114" y1="212" x2="178" y2="194" marker-end="url(#ah3)"/>
  <g class="c-reco">
    <rect class="step" x="180" y="40" width="116" height="44" rx="12"/>
    <text class="box-lbl" x="238" y="68">Reco 1</text>
    <rect class="step" x="180" y="164" width="116" height="44" rx="12"/>
    <text class="box-lbl" x="238" y="192">Reco 2</text>
  </g>
  <line class="ln" x1="296" y1="62" x2="350" y2="62" marker-end="url(#ah3)"/>
  <line class="ln" x1="296" y1="186" x2="350" y2="186" marker-end="url(#ah3)"/>
  <g class="c-filter">
    <rect class="step" x="350" y="40" width="116" height="44" rx="12"/>
    <text class="box-lbl" x="408" y="68">Filter 1</text>
    <rect class="step" x="350" y="164" width="116" height="44" rx="12"/>
    <text class="box-lbl" x="408" y="192">Filter 2</text>
  </g>
  <path class="ln" d="M466 62 Q 526 62 560 110" marker-end="url(#ah3)"/>
  <path class="ln" d="M466 186 Q 526 186 560 138" marker-end="url(#ah3)"/>
  <g class="c-merge">
    <rect class="step" x="560" y="102" width="120" height="44" rx="12"/>
    <text class="box-lbl" x="620" y="130">Merge 1</text>
  </g>
  <line class="ln" x1="680" y1="124" x2="750" y2="124" marker-end="url(#ah3)"/>
  <text class="lbl" x="715" y="114" text-anchor="middle">output</text>
</svg>

---

# Parallelising the work

- No need to separate the **Reco** and **Filter** steps into separate jobs.
- Could be streamed between them or ran sequentially.
- This diagram repeats N times times to produce more simulation.

<svg class="flow" style="max-width: 800px" viewBox="0 0 790 244" role="img" aria-label="Like the previous slide, but each Reco and its Filter are fused into a single two-colour job box per branch, showing the two steps run in one job">
  <defs>
    <marker id="ah10" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <g class="c-sim">
    <rect class="step" x="10" y="14" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="42">Sim 1</text>
    <rect class="step" x="10" y="66" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="94">Sim 2</text>
    <rect class="step" x="10" y="138" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="166">Sim 3</text>
    <rect class="step" x="10" y="190" width="104" height="44" rx="12"/>
    <text class="box-lbl" x="62" y="218">Sim 4</text>
  </g>
  <line class="ln" x1="114" y1="36" x2="174" y2="54" marker-end="url(#ah10)"/>
  <line class="ln" x1="114" y1="88" x2="174" y2="70" marker-end="url(#ah10)"/>
  <line class="ln" x1="114" y1="160" x2="174" y2="178" marker-end="url(#ah10)"/>
  <line class="ln" x1="114" y1="212" x2="174" y2="194" marker-end="url(#ah10)"/>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M328,40 L190,40 Q178,40 178,52 L178,72 Q178,84 190,84 L328,84 Z"/>
    <path class="mfill c-filter" d="M328,40 L466,40 Q478,40 478,52 L478,72 Q478,84 466,84 L328,84 Z"/>
  </g>
  <text class="box-lbl c-reco" x="253" y="68">Reco 1</text>
  <text class="box-lbl c-filter" x="403" y="68">Filter 1</text>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M328,164 L190,164 Q178,164 178,176 L178,196 Q178,208 190,208 L328,208 Z"/>
    <path class="mfill c-filter" d="M328,164 L466,164 Q478,164 478,176 L478,196 Q478,208 466,208 L328,208 Z"/>
  </g>
  <text class="box-lbl c-reco" x="253" y="192">Reco 2</text>
  <text class="box-lbl c-filter" x="403" y="192">Filter 2</text>
  <path class="ln" d="M478 62 Q 536 62 560 110" marker-end="url(#ah10)"/>
  <path class="ln" d="M478 186 Q 536 186 560 138" marker-end="url(#ah10)"/>
  <g class="c-merge">
    <rect class="step" x="560" y="102" width="120" height="44" rx="12"/>
    <text class="box-lbl" x="620" y="130">Merge 1</text>
  </g>
  <line class="ln" x1="680" y1="124" x2="750" y2="124" marker-end="url(#ah10)"/>
  <text class="lbl" x="715" y="114" text-anchor="middle">output</text>
</svg>

---

# Transformation

- Transformations contain many jobs which each do the same thing
- Transformations can be chained together

<svg class="flow" style="max-width: 880px" viewBox="0 30 940 372" role="img" aria-label="The transformation diagram with a third Sim, Reco-Filter and Merge chain added, and each Merge producing its own output file, so the production yields several output files">
  <defs>
    <marker id="ah6" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="tgroup" x="20" y="46" width="164" height="336" rx="16"/>
  <text class="tgroup-lbl" x="102" y="66">Transformation 1</text>
  <rect class="tgroup" x="216" y="72" width="340" height="310" rx="16"/>
  <text class="tgroup-lbl" x="386" y="92">Transformation 2</text>
  <rect class="tgroup" x="600" y="136" width="164" height="246" rx="16"/>
  <text class="tgroup-lbl" x="682" y="156">Transformation 3</text>
  <g class="c-sim">
    <rect class="step" x="32" y="76" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="104">Sim 1</text>
    <rect class="step" x="32" y="128" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="156">Sim 2</text>
    <rect class="step" x="32" y="204" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="232">Sim 3</text>
    <rect class="step" x="32" y="256" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="284">Sim 4</text>
    <rect class="step" x="32" y="326" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="354">Sim 5</text>
  </g>
  <line class="ln" x1="172" y1="98" x2="228" y2="114" marker-end="url(#ah6)"/>
  <line class="ln" x1="172" y1="150" x2="228" y2="134" marker-end="url(#ah6)"/>
  <line class="ln" x1="172" y1="226" x2="228" y2="242" marker-end="url(#ah6)"/>
  <line class="ln" x1="172" y1="278" x2="228" y2="262" marker-end="url(#ah6)"/>
  <line class="ln" x1="172" y1="348" x2="228" y2="348" marker-end="url(#ah6)"/>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,102 L242,102 Q230,102 230,114 L230,132 Q230,146 242,146 L385,146 Z"/>
    <path class="mfill c-filter" d="M385,102 L528,102 Q540,102 540,114 L540,132 Q540,146 528,146 L385,146 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="130">Reco 1</text>
  <text class="box-lbl c-filter" x="462" y="130">Filter 1</text>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,230 L242,230 Q230,230 230,242 L230,260 Q230,274 242,274 L385,274 Z"/>
    <path class="mfill c-filter" d="M385,230 L528,230 Q540,230 540,242 L540,260 Q540,274 528,274 L385,274 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="258">Reco 2</text>
  <text class="box-lbl c-filter" x="462" y="258">Filter 2</text>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,326 L242,326 Q230,326 230,338 L230,356 Q230,370 242,370 L385,370 Z"/>
    <path class="mfill c-filter" d="M385,326 L528,326 Q540,326 540,338 L540,356 Q540,370 528,370 L385,370 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="354">Reco 3</text>
  <text class="box-lbl c-filter" x="462" y="354">Filter 3</text>
  <path class="ln" d="M540 124 Q 600 124 616 176" marker-end="url(#ah6)"/>
  <path class="ln" d="M540 252 Q 600 252 616 200" marker-end="url(#ah6)"/>
  <line class="ln" x1="540" y1="348" x2="610" y2="348" marker-end="url(#ah6)"/>
  <g class="c-merge">
    <rect class="step" x="616" y="166" width="132" height="44" rx="12"/>
    <text class="box-lbl" x="682" y="194">Merge 1</text>
    <rect class="step" x="616" y="326" width="132" height="44" rx="12"/>
    <text class="box-lbl" x="682" y="354">Merge 2</text>
  </g>
  <line class="ln" x1="748" y1="188" x2="782" y2="188" marker-end="url(#ah6)"/>
  <line class="ln" x1="748" y1="348" x2="782" y2="348" marker-end="url(#ah6)"/>
  <rect class="pill" x="786" y="160" width="124" height="216" rx="24"/>
  <text class="pill-lbl" x="848" y="274">Output files</text>
</svg>

---

# Productions

- A Production groups one or more transformations together
    - Might also include data management transformations (e.g. archive output to tape)
    - I'll come to those later

<svg class="flow" style="max-width: 880px" viewBox="0 0 940 406" role="img" aria-label="The three transformations wrapped in one Production box, now with a third chain, and two output files emerging from the production">
  <defs>
    <marker id="ah7" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="prod" x="6" y="14" width="772" height="378" rx="20"/>
  <text class="prod-lbl" x="24" y="38">PRODUCTION</text>
  <rect class="tgroup" x="20" y="46" width="164" height="336" rx="16"/>
  <text class="tgroup-lbl" x="102" y="66">Transformation 1</text>
  <rect class="tgroup" x="216" y="72" width="340" height="310" rx="16"/>
  <text class="tgroup-lbl" x="386" y="92">Transformation 2</text>
  <rect class="tgroup" x="600" y="136" width="164" height="246" rx="16"/>
  <text class="tgroup-lbl" x="682" y="156">Transformation 3</text>
  <g class="c-sim">
    <rect class="step" x="32" y="76" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="104">Sim 1</text>
    <rect class="step" x="32" y="128" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="156">Sim 2</text>
    <rect class="step" x="32" y="204" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="232">Sim 3</text>
    <rect class="step" x="32" y="256" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="284">Sim 4</text>
    <rect class="step" x="32" y="326" width="140" height="44" rx="12"/>
    <text class="box-lbl" x="102" y="354">Sim 5</text>
  </g>
  <line class="ln" x1="172" y1="98" x2="228" y2="114" marker-end="url(#ah7)"/>
  <line class="ln" x1="172" y1="150" x2="228" y2="134" marker-end="url(#ah7)"/>
  <line class="ln" x1="172" y1="226" x2="228" y2="242" marker-end="url(#ah7)"/>
  <line class="ln" x1="172" y1="278" x2="228" y2="262" marker-end="url(#ah7)"/>
  <line class="ln" x1="172" y1="348" x2="228" y2="348" marker-end="url(#ah7)"/>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,102 L242,102 Q230,102 230,114 L230,132 Q230,146 242,146 L385,146 Z"/>
    <path class="mfill c-filter" d="M385,102 L528,102 Q540,102 540,114 L540,132 Q540,146 528,146 L385,146 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="130">Reco 1</text>
  <text class="box-lbl c-filter" x="462" y="130">Filter 1</text>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,230 L242,230 Q230,230 230,242 L230,260 Q230,274 242,274 L385,274 Z"/>
    <path class="mfill c-filter" d="M385,230 L528,230 Q540,230 540,242 L540,260 Q540,274 528,274 L385,274 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="258">Reco 2</text>
  <text class="box-lbl c-filter" x="462" y="258">Filter 2</text>
  <g class="mstep-grp">
    <path class="mfill c-reco" d="M385,326 L242,326 Q230,326 230,338 L230,356 Q230,370 242,370 L385,370 Z"/>
    <path class="mfill c-filter" d="M385,326 L528,326 Q540,326 540,338 L540,356 Q540,370 528,370 L385,370 Z"/>
  </g>
  <text class="box-lbl c-reco" x="308" y="354">Reco 3</text>
  <text class="box-lbl c-filter" x="462" y="354">Filter 3</text>
  <path class="ln" d="M540 124 Q 600 124 616 176" marker-end="url(#ah7)"/>
  <path class="ln" d="M540 252 Q 600 252 616 200" marker-end="url(#ah7)"/>
  <line class="ln" x1="540" y1="348" x2="610" y2="348" marker-end="url(#ah7)"/>
  <g class="c-merge">
    <rect class="step" x="616" y="166" width="132" height="44" rx="12"/>
    <text class="box-lbl" x="682" y="194">Merge 1</text>
    <rect class="step" x="616" y="326" width="132" height="44" rx="12"/>
    <text class="box-lbl" x="682" y="354">Merge 2</text>
  </g>
  <line class="ln" x1="748" y1="188" x2="782" y2="188" marker-end="url(#ah7)"/>
  <line class="ln" x1="748" y1="348" x2="782" y2="348" marker-end="url(#ah7)"/>
  <rect class="pill" x="786" y="160" width="124" height="216" rx="24"/>
  <text class="pill-lbl" x="848" y="274">Output files</text>
</svg>

---

# Becoming abstract again

- When defining a transformation the jobs don't exist
     - In workflow management terms, they form a dynamic DAG

<svg class="flow" style="max-width: 880px" viewBox="0 40 812 188" role="img" aria-label="A single abstract chain Sim, Reco, Filter, Merge with the transformation and production boxes around it">
  <defs>
    <marker id="ah8" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="prod" x="10" y="58" width="784" height="148" rx="18"/>
  <text class="prod-lbl" x="28" y="80">PRODUCTION</text>
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

---

# Connecting it all together

- Each transformation has an **input plugin**: controls when to create tasks
- Transformations with input data have an **metadata query**

<svg class="flow" style="max-width: 1140px" viewBox="22 78 1052 184" role="img" aria-label="The abstract production chain Sim, merged Reco and Filter, Merge — drawn at the same box size as the previous slide — with each input arrow annotated by its parameters, metadata query and input plugin">
  <defs>
    <marker id="ah9" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="prod" x="120" y="90" width="906" height="156" rx="18"/>
  <text class="prod-lbl" x="138" y="112">PRODUCTION</text>
  <rect class="tgroup" x="134" y="124" width="162" height="100" rx="14"/>
  <text class="tgroup-lbl" x="215" y="142">Transformation 1</text>
  <rect class="tgroup" x="402" y="124" width="342" height="100" rx="14"/>
  <text class="tgroup-lbl" x="573" y="142">Transformation 2</text>
  <rect class="tgroup" x="850" y="124" width="162" height="100" rx="14"/>
  <text class="tgroup-lbl" x="931" y="142">Transformation 3</text>
  <g class="c-sim">
    <rect class="job" x="150" y="150" width="130" height="50" rx="13"/>
    <text class="box-lbl" x="215" y="182">Sim</text>
  </g>
  <g class="c-reco">
    <path class="mjob" d="M573,150 L431,150 Q418,150 418,163 L418,187 Q418,200 431,200 L573,200 Z"/>
    <text class="box-lbl" x="495" y="182">Reco</text>
  </g>
  <g class="c-filter">
    <path class="mjob" d="M573,150 L715,150 Q728,150 728,163 L728,187 Q728,200 715,200 L573,200 Z"/>
    <text class="box-lbl" x="650" y="182">Filter</text>
  </g>
  <g class="c-merge">
    <rect class="job" x="866" y="150" width="130" height="50" rx="13"/>
    <text class="box-lbl" x="931" y="182">Merge</text>
  </g>
  <line class="ln dash" x1="40" y1="175" x2="144" y2="175" marker-end="url(#ah9)"/>
  <line class="ln dash" x1="282" y1="175" x2="414" y2="175" marker-end="url(#ah9)"/>
  <line class="ln dash" x1="730" y1="175" x2="862" y2="175" marker-end="url(#ah9)"/>
  <line class="ln" x1="998" y1="175" x2="1058" y2="175" marker-end="url(#ah9)"/>
  <text class="io-lbl" x="75" y="157">INPUT PLUGIN</text>
  <text class="io-sub" x="348" y="141">METADATA QUERY</text>
  <text class="io-lbl" x="348" y="157">INPUT PLUGIN</text>
  <text class="io-sub" x="796" y="141">METADATA QUERY</text>
  <text class="io-lbl" x="796" y="157">INPUT PLUGIN</text>
</svg>

---

# Transformation state

<!-- _class: build -->

- Transformations have **transformation input** (typically a list of LFNs)
- Periodically uses the **input plugin** to decide when to create a **task**
- One or more **transformation input(s)** are assigned to a **task**

<svg class="flow" style="max-width: 760px" viewBox="0 0 900 352" role="img" aria-label="The transformation-input box is split into unassigned, assigned and done sections; the input plugin assigns LFN3 and LFN6 are unassigned, the five assigned LFNs are grouped into three tasks, nothing is done yet">
  <defs>
    <marker id="ahD" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <text class="tsub" x="120" y="16">Transformation input</text>
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
  <text class="plugin-lbl" x="453" y="188">input plugin</text>
  <line class="ln" x1="528" y1="182" x2="590" y2="92" marker-end="url(#ahD)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="182" marker-end="url(#ahD)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="272" marker-end="url(#ahD)"/>
  <rect class="container" x="600" y="56" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="76">TASK 1</text>
  <rect class="pill" x="620" y="84" width="124" height="32" rx="16" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="682" y="105" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="752" y="84" width="124" height="32" rx="16" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="814" y="105" style="fill:#1F9D55">LFN4</text>
  <rect class="container" x="600" y="146" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="166">TASK 2</text>
  <rect class="pill" x="620" y="174" width="124" height="32" rx="16" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="682" y="195" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="752" y="174" width="124" height="32" rx="16" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="814" y="195" style="fill:#138D8D">LFN5</text>
  <rect class="container" x="600" y="236" width="288" height="72" rx="16"/>
  <text class="job-lbl" x="620" y="256">TASK 3</text>
  <rect class="pill" x="620" y="264" width="124" height="32" rx="16" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="682" y="285" style="fill:#5B53C0">LFN7</text>
</svg>

---

# Transformation tasks

- A transformation's **task** is submitted to a backend
- **Tasks** are not retryable -> added back to the pool of unassigned **transformation input(s)**
  - An input is only ever successfully processed by one **task**
- Next time the **input plugin** is run, a new **task** might be created
     - Potentially with different inputs

<svg class="flow" style="max-width: 900px" viewBox="-60 0 1220 392" role="img" aria-label="Each task is submitted as a job; job 1 succeeds so LFN1 and LFN4 move to done, jobs 2 and 3 fail so LFN2, LFN5 and LFN7 return to the unassigned section, leaving nothing assigned">
  <defs>
    <marker id="ahE" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
    <marker id="ahEr" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#C0392B"/></marker>
  </defs>
  <text class="tsub" x="120" y="16">Transformation input</text>
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
  <text class="plugin-lbl" x="453" y="188">input plugin</text>
  <line class="ln" x1="528" y1="182" x2="590" y2="92" marker-end="url(#ahE)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="182" marker-end="url(#ahE)"/>
  <line class="ln" x1="528" y1="182" x2="590" y2="272" marker-end="url(#ahE)"/>
  <rect class="container" x="600" y="56" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="76">TASK 1</text>
  <rect class="pill" x="612" y="84" width="110" height="32" rx="16" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="667" y="105" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="728" y="84" width="110" height="32" rx="16" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="783" y="105" style="fill:#1F9D55">LFN4</text>
  <rect class="container" x="600" y="146" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="166">TASK 2</text>
  <rect class="pill" x="612" y="174" width="110" height="32" rx="16" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="667" y="195" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="728" y="174" width="110" height="32" rx="16" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="783" y="195" style="fill:#138D8D">LFN5</text>
  <rect class="container" x="600" y="236" width="250" height="72" rx="16"/>
  <text class="job-lbl" x="616" y="256">TASK 3</text>
  <rect class="pill" x="612" y="264" width="110" height="32" rx="16" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="667" y="285" style="fill:#5B53C0">LFN7</text>
  <text class="lbl" x="878" y="80" text-anchor="middle">submit</text>
  <line class="ln" x1="850" y1="92" x2="918" y2="92" marker-end="url(#ahE)"/>
  <line class="ln" x1="850" y1="182" x2="918" y2="182" marker-end="url(#ahE)"/>
  <line class="ln" x1="850" y1="272" x2="918" y2="272" marker-end="url(#ahE)"/>
  <rect class="container" x="908" y="40" width="208" height="288" rx="16"/>
  <text class="job-lbl" x="920" y="60">WORKLOAD BACKEND</text>
  <rect class="step" x="924" y="70" width="180" height="48" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="box-lbl" x="1014" y="100" style="fill:#1F9D55">JOB 1 &#10003;</text>
  <rect class="step" x="924" y="160" width="180" height="48" rx="13" style="fill:#FBEAE8;stroke:#C0392B"/>
  <text class="box-lbl" x="1014" y="190" style="fill:#C0392B">JOB 2 &#10007;</text>
  <rect class="step" x="924" y="250" width="180" height="48" rx="13" style="fill:#FBEAE8;stroke:#C0392B"/>
  <text class="box-lbl" x="1014" y="280" style="fill:#C0392B">JOB 3 &#10007;</text>
  <path class="ln dash" style="stroke:#C0392B" d="M1104 184 L1142 184 L1142 372 L-34 372 L-34 112 L12 112" marker-end="url(#ahEr)"/>
  <path class="ln dash" style="stroke:#C0392B" d="M1104 274 L1142 274 L1142 372"/>
  <text class="lbl" x="554" y="366" text-anchor="middle" style="fill:#C0392B">failed &#183; inputs returned to unassigned</text>
</svg>

---

# Grouping correlated inputs

- The **input plugin** can inject additional inputs
- For example also include an ancestor file

<svg class="flow" style="max-width: 1000px" viewBox="0 0 980 320" role="img" aria-label="Each transformation-input LFN has a descendant link to its ancestor in a separate Dataset 1; the input plugin reads the transformation input and follows those links to build tasks pairing each file with its ancestor">
  <defs>
    <marker id="ahH" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <text class="tsub" x="85" y="28">Dataset 1 &#183; ancestors</text>
  <rect class="container" x="10" y="34" width="150" height="266" rx="14"/>
  <rect class="pill" x="22" y="44" width="126" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="85" y="63" style="fill:#2D6CDF;font-size:15px">LFN1</text>
  <rect class="pill" x="22" y="80" width="126" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="85" y="99" style="fill:#E8810B;font-size:15px">LFN2</text>
  <rect class="pill" x="22" y="116" width="126" height="26" rx="13" style="fill:#F1E8F4;stroke:#8B3FA0"/>
  <text class="pill-lbl" x="85" y="135" style="fill:#8B3FA0;font-size:15px">LFN3</text>
  <rect class="pill" x="22" y="152" width="126" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="85" y="171" style="fill:#1F9D55;font-size:15px">LFN4</text>
  <rect class="pill" x="22" y="188" width="126" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="85" y="207" style="fill:#138D8D;font-size:15px">LFN5</text>
  <rect class="pill" x="22" y="224" width="126" height="26" rx="13" style="fill:#F8E6F1;stroke:#C0398B"/>
  <text class="pill-lbl" x="85" y="243" style="fill:#C0398B;font-size:15px">LFN6</text>
  <rect class="pill" x="22" y="260" width="126" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="85" y="279" style="fill:#5B53C0;font-size:15px">LFN7</text>
  <text class="tsub" x="305" y="28">Transformation input</text>
  <rect class="container" x="230" y="34" width="150" height="266" rx="14"/>
  <rect class="pill" x="242" y="44" width="126" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="305" y="63" style="fill:#2D6CDF;font-size:15px">LFN:A</text>
  <rect class="pill" x="242" y="80" width="126" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="305" y="99" style="fill:#E8810B;font-size:15px">LFN:B</text>
  <rect class="pill" x="242" y="116" width="126" height="26" rx="13" style="fill:#F1E8F4;stroke:#8B3FA0"/>
  <text class="pill-lbl" x="305" y="135" style="fill:#8B3FA0;font-size:15px">LFN:C</text>
  <rect class="pill" x="242" y="152" width="126" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="305" y="171" style="fill:#1F9D55;font-size:15px">LFN:D</text>
  <rect class="pill" x="242" y="188" width="126" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="305" y="207" style="fill:#138D8D;font-size:15px">LFN:E</text>
  <rect class="pill" x="242" y="224" width="126" height="26" rx="13" style="fill:#F8E6F1;stroke:#C0398B"/>
  <text class="pill-lbl" x="305" y="243" style="fill:#C0398B;font-size:15px">LFN:F</text>
  <rect class="pill" x="242" y="260" width="126" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="305" y="279" style="fill:#5B53C0;font-size:15px">LFN:G</text>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="57" x2="160" y2="57" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="93" x2="160" y2="93" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="129" x2="160" y2="129" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="165" x2="160" y2="165" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="201" x2="160" y2="201" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="237" x2="160" y2="237" marker-end="url(#ahH)"/>
  <line class="ln" style="stroke-width:2.2" x1="240" y1="273" x2="160" y2="273" marker-end="url(#ahH)"/>
  <text class="lbl" x="200" y="22" text-anchor="middle">ancestor</text>
  <line class="ln" x1="380" y1="167" x2="438" y2="167" marker-end="url(#ahH)"/>
  <rect class="plugin" x="440" y="143" width="130" height="48" rx="14"/>
  <text class="plugin-lbl" x="505" y="174">input plugin</text>
  <line class="ln" x1="570" y1="167" x2="628" y2="80" marker-end="url(#ahH)"/>
  <line class="ln" x1="570" y1="167" x2="628" y2="186" marker-end="url(#ahH)"/>
  <line class="ln" x1="570" y1="167" x2="628" y2="275" marker-end="url(#ahH)"/>
  <rect class="container" x="630" y="34" width="300" height="92" rx="16"/>
  <text class="job-lbl" x="646" y="52">TASK 1</text>
  <rect class="pill" x="644" y="60" width="130" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="709" y="79" style="fill:#2D6CDF">LFN:A</text>
  <rect class="pill" x="782" y="60" width="130" height="26" rx="13" style="fill:#E6EEFC;stroke:#2D6CDF"/>
  <text class="pill-lbl" x="847" y="79" style="fill:#2D6CDF">LFN1</text>
  <rect class="pill" x="644" y="92" width="130" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="709" y="111" style="fill:#1F9D55">LFN:D</text>
  <rect class="pill" x="782" y="92" width="130" height="26" rx="13" style="fill:#E4F3EB;stroke:#1F9D55"/>
  <text class="pill-lbl" x="847" y="111" style="fill:#1F9D55">LFN4</text>
  <rect class="container" x="630" y="140" width="300" height="92" rx="16"/>
  <text class="job-lbl" x="646" y="158">TASK 2</text>
  <rect class="pill" x="644" y="166" width="130" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="709" y="185" style="fill:#E8810B">LFN:B</text>
  <rect class="pill" x="782" y="166" width="130" height="26" rx="13" style="fill:#FCF0E1;stroke:#E8810B"/>
  <text class="pill-lbl" x="847" y="185" style="fill:#E8810B">LFN2</text>
  <rect class="pill" x="644" y="198" width="130" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="709" y="217" style="fill:#138D8D">LFN:E</text>
  <rect class="pill" x="782" y="198" width="130" height="26" rx="13" style="fill:#E6F4F2;stroke:#138D8D"/>
  <text class="pill-lbl" x="847" y="217" style="fill:#138D8D">LFN5</text>
  <rect class="container" x="630" y="246" width="300" height="58" rx="16"/>
  <text class="job-lbl" x="646" y="264">TASK 3</text>
  <rect class="pill" x="644" y="272" width="130" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="709" y="291" style="fill:#5B53C0">LFN:G</text>
  <rect class="pill" x="782" y="272" width="130" height="26" rx="13" style="fill:#ECEAF8;stroke:#5B53C0"/>
  <text class="pill-lbl" x="847" y="291" style="fill:#5B53C0">LFN7</text>
</svg>

---

<!-- _class: build -->

# Data management transformations

- The other side of the transformation system is data management.
     - Two primitives: **Copy** and **Delete**
     - Tasks know the final data distribution state you want to obtain
- Similarities to workload management transformations:
     - Input metadata query to create tasks
     - Tasks have input LFNs
- Differences:
     - No Jobs (uses Requests instead)
     - No CWL
     - No "output"

---

<!-- _class: section -->

# Architecture

---

<!-- _class: build -->

# The three components of the transformation system

<svg class="flow" style="max-width: 600px" viewBox="0 0 720 540" role="img" aria-label="A Venn diagram: metadata management, data management and the workload backend overlap, and the transformation system sits where all three meet">
  <g style="fill-opacity: 0.22">
    <circle cx="360" cy="200" r="165" fill="#8B3FA0" stroke="#8B3FA0" stroke-width="2.5" stroke-opacity="1"/>
    <circle cx="268" cy="348" r="165" fill="#2D6CDF" stroke="#2D6CDF" stroke-width="2.5" stroke-opacity="1"/>
    <circle cx="452" cy="348" r="165" fill="#1F9D55" stroke="#1F9D55" stroke-width="2.5" stroke-opacity="1"/>
  </g>
  <text class="box-lbl" x="360" y="108" style="fill:#8B3FA0">Metadata</text>
  <text class="box-lbl" x="360" y="134" style="fill:#8B3FA0">management</text>
  <text class="box-lbl" x="205" y="372" style="fill:#2D6CDF">Data</text>
  <text class="box-lbl" x="205" y="398" style="fill:#2D6CDF">management</text>
  <text class="box-lbl" x="515" y="372" style="fill:#1F9D55">Workload/Request</text>
  <text class="box-lbl" x="515" y="398" style="fill:#1F9D55">backend</text>
  <text class="box-lbl" x="360" y="292" style="fill:#3A1772; stroke:#fff; stroke-width:4px; paint-order:stroke">Transformation</text>
  <text class="box-lbl" x="360" y="318" style="fill:#3A1772; stroke:#fff; stroke-width:4px; paint-order:stroke">system</text>
</svg>


---

# Metadata management

- Extremely experiment specific

- Basics:
     - Steers what LFNs are picked up by a transformation<sup>†</sup>
     - Output of transformations are registered

- Can also provide:
     - ancestry information for correlated input
     - descendent information for additional safety checks

<div class="footnotes">
  <div class="footnote">† LFNs can be added manually for special cases.</div>
</div>

---

# Data management

<!-- _class: build -->

- Provides information about
     - LFN availability
     - Available storage at sites
- Example uses of transformation **input plugins**:
     - Group LFNs to all have replicas at the same locations
     - Don't create tasks for LFNs that are at locations with downtime

---

<!-- _class: build -->

# Workload/Request backend

- Workload/Request backend takes care of actual **task** execution
- For workload transformations:
  - Each workload task has:
      - Matching criteria
      - Zero or more input LFNs and input sandboxes
      - An associated workflow
  - Workload backend is responsible for:
      - Scheduling the task to a worker node
      - Starting the DiracX job wrapper
- For data management transformations this is handled by **Requests**

---

<!-- _class: section -->

# Wrapping up

---

# Putting it all together

<svg class="flow" style="max-width: 1000px" viewBox="0 0 1020 446" role="img" aria-label="The whole production: Sim feeds a Reco-Filter step and also forks up to a Removal transformation; Filter fans out to two Merge transformations; Sim and Reco each emit monitoring histograms downward, the Sim ones merging while the Reco ones do not">
  <defs>
    <marker id="ahI" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6A3FA8"/></marker>
  </defs>
  <rect class="prod" x="10" y="22" width="1000" height="418" rx="20"/>
  <text class="prod-lbl" x="28" y="46">PRODUCTION</text>
  <rect class="tgroup" x="26" y="128" width="148" height="88" rx="14"/>
  <text class="tgroup-lbl" x="100" y="146">Transformation 1</text>
  <rect class="tgroup" x="256" y="128" width="238" height="88" rx="14"/>
  <text class="tgroup-lbl" x="375" y="146">Transformation 2</text>
  <rect class="tgroup" x="286" y="30" width="178" height="86" rx="14"/>
  <text class="tgroup-lbl" x="375" y="48">Transformation 3</text>
  <rect class="tgroup" x="624" y="86" width="152" height="88" rx="14"/>
  <text class="tgroup-lbl" x="700" y="104">Transformation 4</text>
  <rect class="tgroup" x="624" y="178" width="152" height="88" rx="14"/>
  <text class="tgroup-lbl" x="700" y="196">Transformation 5</text>
  <rect class="tgroup" x="150" y="236" width="134" height="82" rx="14"/>
  <text class="tgroup-lbl" x="217" y="254">Transformation 6</text>
  <rect x="300" y="60" width="150" height="46" rx="13" fill="#FBEAE8" stroke="#C0392B" stroke-width="2.6" stroke-dasharray="9 5"/>
  <text class="box-lbl" x="375" y="89" style="fill:#C0392B">Removal</text>
  <g class="c-sim">
    <rect class="job" x="40" y="158" width="120" height="50" rx="13"/>
    <text class="box-lbl" x="100" y="189">Sim</text>
  </g>
  <g class="c-reco">
    <path class="mjob" d="M375,158 L283,158 Q270,158 270,171 L270,195 Q270,208 283,208 L375,208 Z"/>
    <text class="box-lbl" x="322" y="189">Reco</text>
  </g>
  <g class="c-filter">
    <path class="mjob" d="M375,158 L467,158 Q480,158 480,171 L480,195 Q480,208 467,208 L375,208 Z"/>
    <text class="box-lbl" x="427" y="189">Filter</text>
  </g>
  <g class="c-merge">
    <rect class="job" x="640" y="116" width="120" height="50" rx="13"/>
    <text class="box-lbl" x="700" y="147">Merge</text>
  </g>
  <g class="c-merge">
    <rect class="job" x="640" y="208" width="120" height="50" rx="13"/>
    <text class="box-lbl" x="700" y="239">Merge</text>
  </g>
  <line class="ln" x1="160" y1="183" x2="268" y2="183" marker-end="url(#ahI)"/>
  <path class="ln" d="M214 183 L214 83 L298 83" marker-end="url(#ahI)"/>
  <path class="ln" d="M480 178 Q580 178 618 143" marker-end="url(#ahI)"/>
  <path class="ln" d="M480 188 Q580 188 618 231" marker-end="url(#ahI)"/>
  <line class="ln" x1="100" y1="208" x2="100" y2="268" marker-end="url(#ahI)"/>
  <g fill="#6A3FA8">
    <rect x="82" y="286" width="8" height="14"/>
    <rect x="92" y="278" width="8" height="22"/>
    <rect x="102" y="274" width="8" height="26"/>
    <rect x="112" y="282" width="8" height="18"/>
  </g>
  <text class="lbl" x="100" y="320" text-anchor="middle">monitoring</text>
  <line class="ln" x1="122" y1="288" x2="162" y2="288" marker-end="url(#ahI)"/>
  <g class="c-merge">
    <rect class="job" x="164" y="266" width="106" height="44" rx="13"/>
    <text class="box-lbl" x="217" y="294">Merge</text>
  </g>
  <line class="ln" x1="322" y1="208" x2="322" y2="268" marker-end="url(#ahI)"/>
  <g fill="#6A3FA8">
    <rect x="304" y="286" width="8" height="14"/>
    <rect x="314" y="278" width="8" height="22"/>
    <rect x="324" y="274" width="8" height="26"/>
    <rect x="334" y="282" width="8" height="18"/>
  </g>
  <text class="lbl" x="372" y="290" text-anchor="start">monitoring</text>
  <text class="lbl" x="322" y="324" text-anchor="middle">(no merge)</text>
  <text x="560" y="418" text-anchor="middle" style="font-family: var(--font-sans); font-size: 16px; font-style: italic; fill: #4A1789">Transformations 2 &amp; 6 share a custom state transition &#8212; on finishing, all monitoring is merged into a single histogram</text>
</svg>

<!-- ---

# Jobs

- There is also a use case for standalone jobs
     - Testing production requests
     - One-off jobs (e.g. the histogram merging)
- A Workload Transformation **Task** and a **Job** look very similar
     - Both can be submitted to a workload backend -->

---

# Higher level concepts

- Here I've only talked about the low-level system
- Examples in LHCb:
  - "Analysis productions": [CHEP-2026](https://indico.cern.ch/event/1471803/contributions/6970826/)
  - "mc-requests" and "LbMCSubmit": [CHEP-2023](https://indico.jlab.org/event/459/contributions/11555/) and [CHEP-2024](https://indico.cern.ch/event/1338689/contributions/6010990/)
  - Fluka simulations: [FLUKA.CERN collaboration meeting](https://indico.cern.ch/event/1696556/#41-fluka-on-the-grid)

---

# "Analysis Productions" model: Declaring workflows

<div class="cols">
<div>

- The idea is to have a high-level declarative way of declaring any workflow
- With a escape hatch to allow for deeper customization
- Or just write a DIRAC workflow directly (mostly for expert users)

</div>
<div style="--fs-code: 18px">

```yaml
sim-version: 09
name: My Analysis
WG: Charm
samples:
  - event-types:
      - 23103006
      - 27165175
      - 30000000
    data-types:
      - 2016
      - 2017
      - 2018
    num-events: 2_500_000
    fast-mc:
      redecay: yes
```

</div>
</div>

---

<!-- _class: build -->

# "Analysis Productions" model: Submission

- Submission is then Git-style CI/CD driven
- Can run tests locally (optional)
- Prior to submission, a test is ran automatically
  - Communicate back to users informaton in a friendly way
  - Measure resource requirements
  - Approval rules added automatically for restricted productions
- When merged the production runs

## We won't have time for this now, at the next workshop...

---

<!-- _class: section -->

# Questions?

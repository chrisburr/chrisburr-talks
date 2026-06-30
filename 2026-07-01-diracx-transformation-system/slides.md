---
marp: true
theme: cburr
paginate: true
title: "DiracX production system"
subtitle: ""
author: "Chris Burr"
affiliation: "CERN"
event: ""
event_url: ""
date: "2026-07-01"
description: ""
---

# Introduction

<!-- _class: build -->

- These slides aim to build a common understanding of:
     - What a production is?
     - How a production is split into transformations?
     - How to make use of these blocks in your own workflows.
- After the hackathon, an Architecture Design Review (ADR) will be prepared (~1 week).
     - Once agreed upon, start development!

---

# DIRAC vs DiracX

- Here I show the intended production system in DiracX.
- The underpinnings are almost identical to the DIRAC Transformation System.
    - With lots of little tweaks based on experience and lessons learned.

<!-- Show DIRAC and DiracX logos -->

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

<!-- Some kind of visualisation of this -->

---

# Transformation tasks

- A transformation's **task** is submitted to a backend
- **Tasks** are not retryable -> added back to the pool of unassigned **transformation input(s)**
- Next time the **input plugin** is run, a new **task** might be created
     - Potentially with different inputs

<!-- Some kind of visualisation of this -->

---

<!-- _class: section -->

# Architecture

---

<!-- _class: build -->

# The three components of the transformation system

<!-- Some kind of diagram showing the three components coming together to make the transformation system -->


---

# Metadata management

- Basics:
     - Steers what LFNs are picked up by a transformation<sup>†</sup>
     - Output of transformations are registered
     
- Can also provide:
     - ancestry information for correlated input
     - descendent information for additional safety checks

<!-- Overlay showing the RDST workflow where we have a "Filtering" payload where the input arrow is reconstruction and there is a correlated input for the raw file that is some how queried from the metadata catalog by an advanced input plugin. It should be clear that this payload is a dashed line within a box which represents a transformation. -->

<!-- Footnote, LFNs can be added manually for special cases -->
---

# Data management

- Provides information about LFN availability
- Example uses by transformation **input plugins**:
     - Group LFNs to all have replicas at the same locations
     - Don't create tasks for LFNs that are at locations with downtime

---

# Workload backend

- Workload backend takes care of actual payload execution
- Each workload task has:
     - Matching criteria
     - Zero or more input LFNs
     - Zero or more input sandboxes
     - An associated workflow
- Workload backend is responsible for:
     - Scheduling the task to a worker node
     - Starting the DiracX job wrapper

---

<!-- _class: section -->

# Generalisations

---

# Input to transformations



---

# Data management transformations

- The other side of the transformation system is data management.
- Three primitives: **Copy**, **Delete**, **Destroy**.
     - Delete removes a replica but NEVER the last replica.

<hr>

- Similarities to workload management transformations:
     - Input metadata query

<hr>

- Differences:
     - No jobs (uses requests instead)
     - No CWL

---

# Input plugin

---

# Testing

---

# State transitions

---

# Ancestry

---

# Submission

---

# Execution
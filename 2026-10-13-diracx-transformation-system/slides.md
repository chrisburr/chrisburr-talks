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

<!-- Deck-local styling. The diagrams are standalone SVGs in assets/diagrams/
     (each carries its own styles and fonts); this only lays them out. -->
<style>
section img.diagram { display: block; width: 100%; height: auto; margin: 0 auto; }

/* the split slides: two generic graphs side by side */
section .split { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-6); align-items: start; }
section .split img.diagram { max-height: 430px; width: auto; max-width: 100%; }
section .cap { text-align: center; font-weight: 700; font-size: 22px; margin: 0 0 var(--sp-3); }

/* two diagrams revealed side by side (`_class: build pair`) */
section.build.pair { flex-direction: row; align-items: flex-start; gap: var(--sp-6); }
section.build.pair .reveal-group { flex: 1 1 0; margin: 0; }
section.build.pair .reveal-group.is-faded { opacity: 1; }
section.build.pair img.diagram { max-height: 430px; width: auto; max-width: 100%; }

/* "does it do everything" reveals: a build slide with two empty marker stages
   swaps the plain generic graph (-base.svg) for the one with pink additions */
section .reveal-group:has(.rv) { display: none; }
section .stack { display: grid; margin: 0 auto; }
section .stack > img { grid-area: 1 / 1; }
section:has(.reveal-group.is-hidden .rv-add) .stack > .add { visibility: hidden; }
section:not(:has(.reveal-group.is-hidden .rv-add)) .stack > .base-only { visibility: hidden; }

/* the definition quotes: the term being introduced stands out from the grey */
section .defn { font-size: 23px; max-width: 64ch; }
section blockquote strong { color: var(--ink); }

/* transformation names in the text, coloured like their tiles in the diagrams */
section .tc-gen { color: #2D6CDF; }
section .tc-p1  { color: #E8810B; }
section .tc-p2  { color: #8B3FA0; }
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

<img class="diagram" src="assets/diagrams/wms.svg" alt="DIRAC&#x27;s WMS split into pilots and jobs; pilots become one DiracX compute backend, jobs move into the Transformation System" style="max-width: 560px">

</div>
</div>

---

# Same concept, new names

> jobs, transformation and productions are the same <cite>The future of DIRAC</cite>

- We meant that about search APIs. Turns out it goes deeper:

<img class="diagram" src="assets/diagrams/nesting.svg" alt="DIRAC nests production, transformation, task and job; DiracX nests workgraph, transformation and parcel, where a parcel runs as a job or a request" style="max-width: 980px">

---

# Grid high-throughput batch

- One program, thousands of files (or seeds), a `for` loop of submissions…
    - …then babysitting: resubmit failures, group small files, track what's done
- This is the problem we're trying to solve

<img class="diagram" src="assets/diagrams/batch.svg" alt="A grid of hand-submitted user jobs; failures and resubmissions are scattered through it" style="max-width: 980px">

---

<!-- _class: build pair -->

# Two minimal use cases

<!-- step -->

<p class="cap">Generic data processing: process + merge</p>

<img class="diagram" src="assets/diagrams/generic-proc-simple.svg" alt="Generic data processing: Process then Merge">

<!-- step -->

<p class="cap">Generic simulation: produce + process + merge</p>

<img class="diagram" src="assets/diagrams/generic-sim-simple.svg" alt="Generic simulation: Produce then Process then Merge">

---

<!-- _class: section -->

# What is it?

---

# What is it?

<blockquote class="defn">

A **workgraph** is a directed acyclic graph of **transformations**. It is what DIRAC called a production. Each transformation maintains a pool of **inputs**: a **feeder** tops up the pool from the experiment's metadata catalogue, a **packer** groups pooled inputs into **parcels**, and a **dispatcher** hands each parcel to a compute or data **backend**, which executes it as a job or a request. A workgraph is written as a **CWL document**: its dataflow declares how transformations chain, and inputs arriving from outside the workgraph carry the metadata queries that tell the feeder what to fetch.

<cite>DX-ADR-002</cite>
</blockquote>

---

# Workgraph

> **A workgraph**

- The **entire thing**: everything needed to deliver what was asked for
    - What DIRAC called a **production**
- Created in one go, with all its transformations
- Its **status is constrained** by its members', provides **control flow**
    - start, scout, drain, halt, cancel

---

# Workgraph

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-wg.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-wg.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Directed acyclic graph

> A workgraph is a **directed acyclic graph**

- Transformations **chain**: the output of one is the input of the next
- A **graph**, not a chain: real workgraphs fork and merge
- Downstream picks up outputs **as they appear**
    - No waiting for the whole upstream stage to finish

---

# Directed acyclic graph

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-dag.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-dag.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Transformation

> A workgraph is a directed acyclic graph of **transformations**.

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

<img class="diagram" src="assets/diagrams/generic-proc-tf.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-tf.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Inputs

> Each transformation maintains a pool of **inputs**

- Usually a file (LFN)
    - Sometimes a fraction of one, sometimes not a file at all (a seed)
- Processed **exactly once, or not at all**
    - `Unassigned` → `Assigned` → `Processed`
    - `Unassigned` → `Assigned` → `NotProcessed`

---

# Inputs

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-in.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-in.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Feeding

> …a **feeder** tops up the pool from the experiment's metadata catalogue

- **External** feeders bring work in from outside the workgraph
    - a metadata query, a run range that grows over time, seeds
    - Experiment-specific: this is where your catalogue plugs in
- **Internal** feeders follow the edges of the graph: you don't need to care

---

# Feeding

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-feed.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-feed.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Packing and parcels

> …a **packer** groups pooled inputs into **parcels**

- **When:** hold out for full groups while input keeps coming, pack the rest once it stops
- **How:** ~3 GB per parcel, same storage, same run, …
- A parcel is **never retried**: a failure sends its *inputs* back to the pool

---

# Packing and parcels

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-pack.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-pack.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Dispatching

> …and a **dispatcher** hands each parcel to a compute or data **backend**, which executes it as a job or a request

- Compute: native pilots, push to HPC, HTCondor, legacy DIRAC, …
- **Very flexible:** the dispatcher chooses, the packer can constrain
- User jobs take exactly the same path
- **Dedicated session tomorrow**

---

# Dispatching

<div class="split">
<div>

<img class="diagram" src="assets/diagrams/generic-proc-disp.svg" alt="Generic data processing workgraph: Process, Merge">

</div>
<div>

<img class="diagram" src="assets/diagrams/generic-sim-disp.svg" alt="Generic simulation workgraph: Produce, Process, Merge">

</div>
</div>

---

# Written down as CWL

> A workgraph is written as a **CWL document**: its dataflow declares how transformations chain, and inputs arriving from outside the workgraph carry the metadata queries that tell the feeder what to fetch

- The **same document** regardless of local tests, user parcels or workgraphs
- Specified in [DX-ADR-007](https://github.com/DIRACGrid/diracx/pull/1042) - Ryun will cover this next

---

# Workgraph state machine (idealised)

<!-- The scout further arrow can go from both here and the next slide -->

<img class="diagram" src="assets/diagrams/states.svg" alt="Idealised workgraph state machine: New, Scouting, Approving, Active, Finalizing, Completed, Archiving, Archived; New, Scouting, Active and Archived highlighted" style="max-width: 1160px">

---

# Hooks and actions

- In several places you have a limited set of hooks **OR** actions to drive the workgraph forward:
  - **Hooks** run while in a state and return changes to feeder arguments, pause, retry an input
  - **Actions** are ordered lists of steps, each recording `Passed`, `Failed` or `Pending`

<img class="diagram" src="assets/diagrams/states-hooks.svg" alt="Idealised workgraph state machine: New, Scouting, Approving, Active, Finalizing, Completed, Archiving, Archived; with the hooks and actions that run in each state" style="max-width: 1160px">

---

<!-- _class: section -->

# Does it do everything we need?

---

# Composing the pieces

- Everything so far **composes**: any number of transformations, any shape of graph
- **Everybody (VOs, or even within a VO) has slightly different needs**
- Each use case changes only:
    - the shape of the graph
    - which feeder, packer, hooks and actions are plugged in
- Next: the two generic graphs again, with the additions in pink

---

<!-- _class: build -->

# Many outputs

<div class="cols">
<div>

- One step, several outputs
- A consumer consumes one output

</div>
<div>

<div class="stack" style="max-width: 560px">
<img class="diagram base-only" src="assets/diagrams/many-base.svg" alt="Processing workgraph where Process emits three file types, each consumed by its own Merge and delivered as its own dataset">
<img class="diagram add" src="assets/diagrams/many.svg" alt="Processing workgraph where Process emits three file types, each consumed by its own Merge and delivered as its own dataset">
</div>

</div>
</div>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Forking outputs

<div class="cols">
<div>

- One output, **many consumers**
- One input per consumer
  - Each input is processed once
- Each consumer tracks it's own progress

</div>
<div>

<div class="stack" style="max-width: 540px">
<img class="diagram base-only" src="assets/diagrams/fanout-base.svg" alt="Processing workgraph where the single Process output forks: the same files go to both Merge and an extra Selection transformation with its own output">
<img class="diagram add" src="assets/diagrams/fanout.svg" alt="Processing workgraph where the single Process output forks: the same files go to both Merge and an extra Selection transformation with its own output">
</div>

</div>
</div>

<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Removing replicas after N uses

<div class="cols">
<div>

- A **removal** transformation
  - fed by the same output
- Its packer delays each file until **all N consumers** have processed it

</div>
<div>

<div class="stack" style="max-width: 560px">
<img class="diagram base-only" src="assets/diagrams/removal-base.svg" alt="Processing workgraph where the Process output forks to Merge, a removal data transformation in the middle, and a Selection; the removal waits until both Merge and Selection have processed each file">
<img class="diagram add" src="assets/diagrams/removal.svg" alt="Processing workgraph where the Process output forks to Merge, a removal data transformation in the middle, and a Selection; the removal waits until both Merge and Selection have processed each file">
</div>

</div>
</div>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Correlated processing (external)

<div class="cols">
<div>

- An file  has to be processed with its **ancestor**
- The inputs holds only one of the datasets
    - The **packer** looks up each ancestor and adds it to the parcel

</div>
<div>

<div class="stack" style="max-width: 540px">
<img class="diagram base-only" src="assets/diagrams/rdst-base.svg" alt="Processing workgraph fed by an RDST query; the Process packer looks up each RDST&#x27;s RAW ancestor in the bookkeeping and adds it to the parcel">
<img class="diagram add" src="assets/diagrams/rdst.svg" alt="Processing workgraph fed by an RDST query; the Process packer looks up each RDST&#x27;s RAW ancestor in the bookkeeping and adds it to the parcel">
</div>

</div>
</div>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Correlated processing (internal)

<div class="cols">
<div>

- The same shape, inside one workgraph
- <strong class="tc-p2">Process 2</strong> needs both:
  - <strong class="tc-p1">Process 1</strong> output
  - <strong class="tc-gen">Generate</strong> output
- Its pool is fed by <strong class="tc-p1">Process 1</strong>
    - The **packer** adds the matching <strong class="tc-gen">Generate</strong> file to the **parcel**

</div>
<div>

<div class="stack" style="max-width: 540px">
<img class="diagram base-only" src="assets/diagrams/join-base.svg" alt="Simulation workgraph: seeds, Generate, Process 1, Process 2, Merge; Process 2 also takes the Generate output that each Process 1 file came from">
<img class="diagram add" src="assets/diagrams/join.svg" alt="Simulation workgraph: seeds, Generate, Process 1, Process 2, Merge; Process 2 also takes the Generate output that each Process 1 file came from">
</div>

</div>
</div>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Staging input

<div class="cols">
<div>

- Raw data lives on **tape**
- A **data transformation** stages it
    - Shares the processing step's query
- **Packer delays** each file until on buffer
    - The input just waits in the pool
    - Same mechanism can be used for site downtime, waiting calibrations, etc.

</div>
<div>

<div class="stack" style="max-width: 560px">
<img class="diagram base-only" src="assets/diagrams/staging-base.svg" alt="Processing workgraph with a staging data transformation sharing its query; the Process packer delays each file until its staged replica exists">
<img class="diagram add" src="assets/diagrams/staging.svg" alt="Processing workgraph with a staging data transformation sharing its query; the Process packer delays each file until its staged replica exists">
</div>

</div>
</div>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Single outputs

<div class="cols">
<div>

- **Example:** Every job also writes small files e.g. monitoring histograms
- Declare a **second output** of the step
- Two options:
    - **transformation** fed by that output,
      its packer waits for feeder to finish
    - **finalizing action** runs in DiracX tasks
- Not mutually exclusive

</div>
<div>

<div class="stack" style="max-width: 540px">
<img class="diagram base-only" src="assets/diagrams/histograms-base.svg" alt="Processing workgraph where Process also emits histograms, merged by an extra histogram-merge transformation into a histograms output">
<img class="diagram add" src="assets/diagrams/histograms.svg" alt="Processing workgraph where Process also emits histograms, merged by an extra histogram-merge transformation into a histograms output">
</div>

</div>
</div>


<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Keeping intermediate files

<div class="cols">
<div>

- Intermediate outputs are **transient**
- Want to keep one?
  **Declare it as an output** of the workgraph

</div>
<div>

<div class="stack" style="max-width: 540px">
<img class="diagram base-only" src="assets/diagrams/keep-base.svg" alt="Simulation workgraph where the Process output is also declared as a workgraph output and kept as a second dataset">
<img class="diagram add" src="assets/diagrams/keep.svg" alt="Simulation workgraph where the Process output is also declared as a workgraph output and kept as a second dataset">
</div>

</div>
</div>


<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

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

<img class="diagram" src="assets/diagrams/retry.svg" alt="Inside one transformation: a parcel fails, its inputs go to the HandleFailedInput hook, which returns them to the pool or quarantines them as Problematic" style="max-width: 600px">

</div>
</div>

---

# Splitting

<div class="cols">
<div>

- A job processed **part** of its input
- Input status is `Split`, two inputs added
    - a `Processed` child
    - an `Unassigned` child
- `Unassigned` child could also be directly marked `Problematic` or `NotProcessed`

</div>
<div>

<img class="diagram" src="assets/diagrams/split.svg" alt="A parcel processes only part of its input file: the parent input becomes Split, the processed part a Processed child, the rest an Unassigned child back in the pool" style="max-width: 600px">

</div>
</div>

---

<!-- _class: build -->

# Scouting

<div class="cols">
<div>

- Run on a **small sample** first for
    - Resource estimation
    - Reliability / success rate
- **Not for testing if the workgraph works!**

<br/>

- A **hook** decides when the scout is done
- Approved → the feeder's limits are lifted
    - Nothing the scout produced is redone
- Not convinced? **Scout further**

</div>
<div>

<div class="stack" style="max-width: 520px">
<img class="diagram base-only" src="assets/diagrams/scouting-base.svg" alt="Simulation workgraph with a state strip Scouting, Approving, Active, Scouting lit; the seed feeder yields a small scouting sample first">
<img class="diagram add" src="assets/diagrams/scouting.svg" alt="Simulation workgraph with a state strip Scouting, Approving, Active, Scouting lit; the seed feeder yields a small scouting sample first">
</div>

</div>
</div>

<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Resource estimation

<div class="cols">
<div>

- Just an **approving action**
- Measures CPU, memory, disk, ...
- Writes the needs back into each transformation's **requirements**
- Too high? The action fails, a human looks
- **Hooks** can also provide realtime feedback

</div>
<div>

<div class="stack" style="max-width: 560px">
<img class="diagram base-only" src="assets/diagrams/approving-resources-base.svg" alt="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
<img class="diagram add" src="assets/diagrams/approving-resources.svg" alt="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
</div>

</div>
</div>

<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

---

<!-- _class: build -->

# Manual approval(s)

<div class="cols">
<div>

- Actions can manual sign-off steps, e.g.
    - Resource usage higher than expected?
    - Validate scouting results
    - Operations

</div>
<div>

<div class="stack" style="max-width: 560px">
<img class="diagram base-only" src="assets/diagrams/approving-ppg-base.svg" alt="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
<img class="diagram add" src="assets/diagrams/approving-ppg.svg" alt="Simulation workgraph beside its ordered list of approving actions: success rate, resource estimate, PPG approval, manual sign-off">
</div>

</div>
</div>


<span class="rv"></span>

<!-- step -->

<span class="rv rv-add"></span>

---

# …and what did we miss?

- Have a use case that **doesn't** fit? We want to hear about it this week
- Bring it to the **CWL hackathon**

---

<!-- _class: section -->

# Future plans

---

<!-- _class: build -->

# Future plans

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

---
marp: true
theme: cburr
paginate: true
title: "Packaging and distributing the HEP ecosystem on conda-forge"
subtitle: ""
author: "Chris Burr · Matthew Feickert"
affiliation: "CERN · University of Wisconsin–Madison"
extra_logos: "assets/uw-madison-logo.png|University of Wisconsin–Madison, assets/iris-hep-logo.png|IRIS-HEP"
event: "HSF Seminar — Software Packaging"
event_url: "https://indico.cern.ch/event/1692605/"
date: "2026-06-24"
description: "Distributing the HEP software ecosystem on conda-forge: shared build infrastructure, reproducible environments, and integration with CVMFS."
---

# Preface

<!-- _class: build -->

- Software packaging is a complex topic and this is a short talk
- For the purpose of this talk:
<br>

> Software packaging is a means to get software in a reproducible and reliable way

- Will break this down into three parts:

<div class="cols3">
<div>

🛠️ **Tooling**

install & manage environments

</div>
<div>

📦 **Packages**

recipes & binaries

</div>
<div>

🧑‍💻 **Development**

build & iterate

</div>
</div>

---

<!-- _class: section -->

# Tooling

---

# What is the conda **ecosystem**?

<!-- _class: build -->

<img class="overlay br" src="assets/conda-logo.svg" alt="conda" style="--overlay-h: 130px">

1. Installer tools for software packages and their dependencies:
   - `conda create ...`
   - `pixi init`
1. A channel for distributing software packages: `conda-forge`
1. A file format for binary packages: `.conda`
1. Tools for building packages:
   - `conda-build`
   - `rattler-build`
1. Distributed cyberinfrastructure for building conda packages coherently: https://github.com/conda-forge/

---

# What is the conda ecosystem **not**?

<!-- _class: build -->

1. An operating system wide package manager (like `apt` or `yum`)
    - In the context of HSF use cases these aren't very interesting

1. A language specific package manager (like `pip`)
    - Conda packaging format is **language agnostic**
    - Can package C/C++, Fortran, Rust, Python, Go, R ...

1. Anaconda, Inc. (the company)
    - Conda is a community project with a varied elected steering council
    - Conda-forge packages are **free and open source**
    - Anaconda supports conda-forge, but is only a small fraction of the community
    - Anaconda's paid offerings are not interesting to HEP users

1. Something new

---

# It's been a while...

> Looking back at your PyHEP 2019 conda-forge talk (interesting to see how much has stayed the same over 6+ years)

<figure>
  <img src="assets/pyhep2019-conda-forge-talk.jpg" alt="The PyHEP 2019 conda-forge talk">
  <figcaption><a href="https://indico.cern.ch/event/833895/contributions/3577783/">Packaging for Python and Beyond &mdash; PyHEP 2019</a></figcaption>
</figure>

---

<!-- _class: build -->

# What has changed?

- Compiler toolchains are now much more mature
    - Originally hard to use outside of conda builds
    - Now they're very mature and well maintained, including CUDA
- Tooling is much faster
    - Used to advertise getting ROOT in under 5 minutes
    - Now it can be ~10 seconds
- Pixi provides a lot of "user experience" improvements

---

# What does Pixi give you?

<!-- _class: build -->

<img class="overlay tr" src="assets/pixi.png" alt="Pixi">

- Workspace model of working
  - Add a `pixi.toml` to describe the software you need
  - Can contain multiple environments for different use cases
  - Can also describe commands to run in the environment ("tasks")

- Pixi then takes care of generating a lock file
  - Ensures that everyone has the same software installed<sup>*</sup>
  - This should typically be committed to the repository<sup>†</sup>

<div class="footnotes">
  <div class="footnote">* Assuming the same OS (Linux/macOS) and CPU architecture.</div>
  <div class="footnote">† Tools like renovate can be used to automatically update the lock file periodically.</div>
</div>

- 🪄 Pixi takes care of managing all of the software environments for you 🪄

---

<!-- _class: section -->

# But where do the packages come from?

---

# Getting packages

- How to build software ("recipes")
- How to avoid building software ("binaries")
- How to know it will work together

---

# Binary distribution

<!-- _class: build -->

- Conda is primarily a binary package manager
     - Recipes are used to build binaries for multiple platforms
     - Binaries are distributed via channels, the most popular of which is conda-forge
- Potentially a different model that what you're used to, but is a very pragmatic approach
- For two binaries to be compatible it doesn't matter:<sup>†</sup>
     - Which C++ compiler was used to build them
     - Which C++ standard is used
     - Which Linux distribution you use

<div class="footnotes">
  <div class="footnote">† This is massively over simplified but we don't have time to go into the details here.</div>
</div>

---

# conda-forge

<img class="overlay tr" src="assets/conda-forge-logo.svg" alt="conda-forge" style="--overlay-h: 80px">

- Shared CI and distribution infrastructure.
- ~7800 contributors, 33,000+ packages, 43 billion+ downloads
     - contributors maintain one or more packages
     - core team maintains the infrastructure keeps the ecosystem healthy
- Heavy use of automation to manage version updates and rebuilds
- Isn't frozen, you can contribute to add / update / fix packages

---

# The HEP Packaging Coordination project

<div class="cols">
<div>

- A community project to get **as much HEP software as possible** onto conda-forge.
- Contributors across HEP: ATLAS, Belle II, CMS, LHCb, IRIS-HEP, LEGEND, ROOT, Scikit-HEP, SHiP, ROOT, DIRAC, theory/pheno...
- **120+ HEP packages** already: ROOT, Pythia8, FastJet, awkward, Rivet, cms-combine, ...
- Installing should be trivial

</div>
<div>

<figure>
  <img src="assets/hep-packaging-coordination.png" alt="HEP Packaging Coordination package categories">
  <figcaption><a href="https://github.com/hep-packaging-coordination">hep-packaging-coordination</a></figcaption>
</figure>

</div>
</div>

---

<!-- _class: section -->

# Development

---

# What is development?

<!-- _class: build -->

- Someone writing
     - libraries for general use (e.g. ROOT, FastJet, Rivet, Pythia, ...).
     - software for a specific experiment (e.g. LHCb, ATLAS, CMS, Belle II, ...).
     - a niche analysis tool for use inside an experiment
- Someone doing
     - analysis for physics
     - quick one-off detector study

---

# Pixi-build

<!-- _class: build -->

- The workspace model mentioned works really well for all of these cases
     - No global state which can prevent you from working on multiple projects
     - Collaborate effectively by having the same software everywhere
- Pixi-build takes this a step further: you can depend on unreleased software
     - Point to branches in git repositories
     - Point to local clones of your dependencies
- Kind of like Python's editable installs except for any language

---

# An aside: Use of Conda in LHCb

- Most LHCb software is on conda-forge (even extremely LHCb-specific software)
- Already used for:
     - User login environment on CVMFS/lxplus
     - All grid middleware
     - Hosting web services
     - User analysis environments on CVMFS (lb-conda)
     - Local user environments
- Notably exception is the "physics stack"
     - Have been experimenting with this more recently
     - Extremely promising, main questions are around the nicest way to integrate it

---

# Summary

- Conda-forge provides the recipes/binaries
- The Conda community provides the tooling
- HEP packaging coordination coordinates efforts within HEP

<div class="fineprint">

Links:

- HEP Packaging Coordination — <https://github.com/hep-packaging-coordination>
- Matthew's CHEP 2026 talk — <https://matthewfeickert-talks.github.io/talk-chep-2026/>
- "Conda, Pixi and RattlerFS" — <https://talks.chrisburr.me/2026-06-22-pixi-and-rattlerfs/>

</div>

---

<!-- _class: section -->

# Questions?

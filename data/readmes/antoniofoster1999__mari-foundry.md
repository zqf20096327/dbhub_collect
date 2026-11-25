<h1 align="center">Mari Foundry - Modular Asset Pipeline Toolkit for Windows 10/11</h1>

<p align="center"><i>Mari Foundry is a Windows desktop workspace for building, validating, and exporting game-ready assets through a modular foundry pipeline. Artists, technical artists, and small studios use it to move meshes, materials, and metadata from source files to engine-ready packages without leaving one window. This page covers what the app does, what it needs, and how to get productive fast.</i></p>

<p align="center"><img src="https://img.shields.io/badge/Status-Working-2ea44f?style=flat" alt="Status Working">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Windows-10%20%7C%2011-3178c6?style=flat&logo=windows&logoColor=white" alt="Windows 10 | 11">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Type-Reference-7e57c2?style=flat" alt="Type Reference">&nbsp;&nbsp;<img src="https://img.shields.io/badge/License-MIT-2b8a3e?style=flat" alt="License MIT">&nbsp;&nbsp;<img src="https://img.shields.io/badge/Version-v1.0-4c9a2a?style=flat" alt="Version v1.0"></p>

<p align="center"><img src="./assets/cover.png" alt="Mari Foundry on Windows, reference page banner" width="100%"></p>

<p align="center">
  <a href="https://antoniofoster1999.github.io/mari-foundry/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./assets/Click-dark.svg">
      <img src="./assets/Click-light.svg" alt="Open reference page" width="300">
    </picture>
  </a>
</p>

## Overview

Mari Foundry is a desktop application that turns raw source assets into validated, engine-ready packages. You import meshes, textures, and material definitions, run them through a configurable chain of processing modules, preview the result in a real-time viewport, and export a clean bundle for your target engine or runtime. It handles the repetitive middle of the pipeline: naming conventions, scale normalization, texture channel packing, LOD generation, and manifest writing, so the same rules apply to every asset that leaves your project.

It is built for technical artists, indie teams, and pipeline engineers who need a predictable asset handoff without maintaining a stack of one-off scripts. On Windows 10/11 it runs natively, keeps project state on disk in plain folders you can version, and exposes every module's settings so you can tune the foundry to your studio's conventions. If your workflow involves hand-checking exports or re-running the same batch of fixes every sprint, Mari Foundry is worth a look.

## Requirements

| Spec | Minimum | Recommended |
| --- | --- | --- |
| OS | Windows 10 version 1909 (64-bit) | Windows 11 22H2 or later |
| CPU | 4-core x64, SSE4.2 | 8-core x64 with AVX2 |
| RAM | 8 GB | 16 GB or more |
| GPU or display | DirectX 11 GPU, 1920x1080 | DirectX 12 GPU with 4 GB VRAM, 2560x1440 |
| Storage | 2 GB free for install | 20 GB free SSD for project caches |
| Asset throughput | Single-file import only | Batch queue of 500+ assets per run |

## Key Features

* **Module Pipeline** , chain import, transform, validate, and export modules into a reusable profile you apply to any folder of assets.
* **Real-Time Preview** , inspect meshes, UVs, and packed textures in a PBR viewport before committing an export.
* **Validation Rules** , define naming, scale, and material checks that block a batch from exporting until every asset passes.
* **Batch Queue** , drop hundreds of source files into a queue and let the foundry process them unattended with per-file logs.
* **Manifest Export** , write engine-ready manifest files alongside your bundles so downstream tools know exactly what shipped.
* **Profile Versioning** , keep pipeline profiles in plain files under your project so teammates share identical settings.
* **Channel Packing** , combine roughness, metallic, and occlusion maps into a single texture with configurable channel order.
* **LOD Builder** , generate decimated mesh levels with preserved UV seams and per-level export naming.

## Tips and Best Practices

* Store pipeline profiles inside your project repository so profile changes ship with the assets they affect.
* Run a validation-only pass on a new folder before exporting, it catches naming and scale issues in seconds instead of at import time.
* Keep the texture cache on an SSD separate from the install drive, batch runs spend most of their time reading and writing it.
* Set channel packing order per target engine rather than per project, this keeps packed textures portable across projects on the same engine.
* Enable per-file logs when debugging a batch, and keep them off for routine runs to avoid log spam in the project folder.
* Generate LODs from the highest-resolution source mesh, decimating an already-reduced mesh loses UV seams faster.
* Pin a project to a specific foundry profile version so a mid-sprint profile edit does not silently change exports.

## Main Tools

* **Import Foundry** , load source meshes and textures with format-specific options, pick this first in any pipeline.
* **Module Editor** , assemble and reorder processing modules into a pipeline, use it when your studio conventions change.
* **Preview Viewport** , inspect the current asset with lighting and material toggles, reach for it before exporting.
* **Validation Console** , review rule failures grouped by asset and rule, open it when a batch is blocked.
* **Batch Queue** , queue folders or file lists and monitor progress per asset, use it for overnight runs.
* **Export Packager** , choose a target bundle layout and write manifests, this is the final step before handoff.

## Supported Content

* Mesh and texture source formats including FBX, OBJ, glTF, PNG, TGA, and EXR.
* Target bundle layouts for Unity, Unreal Engine, and Godot projects.
* PBR material definitions with metallic, roughness, normal, and occlusion maps.
* Windows file shares and local project folders used as source or destination roots.
* Version control checkouts (Git and Perforce workspaces) as project roots for profile files.
* Multi-monitor setups for keeping the viewport and validation console side by side.

## FAQ

### Does Mari Foundry work fully offline?

Yes. Import, processing, validation, and export all run locally with no network access required. Only optional update checks touch the network, and those can be disabled in settings.

### Where do saved projects and pipeline profiles live?

Projects are plain folders you choose on disk, so you can place them anywhere you like. Pipeline profiles live inside the project folder under a profiles subdirectory, which is why they version cleanly with source control.

### Can I run a large batch unattended?

Yes. Add folders or file lists to the Batch Queue, start the run, and leave it going. Per-file logs are written to the queue folder so you can review failures the next morning.

### How much disk space do batch caches take?

Caches scale with batch size, so plan for roughly 20 GB free on the cache drive for a few hundred assets. You can point the cache at a different drive than the install drive in settings.

### Does it support multi-monitor setups?

Yes. The preview viewport, module editor, and validation console can each be moved to a separate display. Window layouts are remembered per project.

### Can I migrate an existing pipeline from an older version?

Older profiles are imported automatically on first open, and you can also import them manually through the Module Editor. Rules that reference removed modules are flagged for review rather than silently dropped.

## Notes

Batch processing writes caches and logs beside your project unless you redirect them in settings, so check the cache drive before long runs. Engine and file format names referenced here are trademarks of their respective owners and are used only to describe import and export targets.
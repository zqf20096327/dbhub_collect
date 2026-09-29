# OpenGaussian

A GNOME-native Gaussian-splatting studio for Linux — capture a scene with
your camera, and OpenGaussian turns it into a 3D Gaussian splat you can
inspect live and export. Think [Postshot]-style workflow, but free software,
built with GTK4/libadwaita, and running end-to-end on your own machine.

<!-- TODO: screenshot of the main window once the UI is stable -->

[Postshot]: https://www.jawset.com/

## What it does (v1)

The whole pipeline runs locally, driven from a four-stage workflow:

1. **Import** — bring in a folder of photos, or a video from a local file or
   a YouTube URL. Video opens a picker that plays the clip and lets you mark
   any number of sections on a timeline, so only the parts of the walkthrough
   you actually want become frames. Frames are extracted with GStreamer and
   scored for sharpness so blurry frames are dropped automatically. YouTube
   downloads need `yt-dlp`; if it isn't installed, the app offers to install
   a managed copy for the current user (and to update it later, since a stale
   `yt-dlp` is the usual cause of download failures). Downloaded videos are
   kept in the project's `source/` folder and reused: pasting a URL whose
   video is already there reopens the picker without downloading it again,
   so re-picking sections costs no second download.
2. **Poses** — camera poses are recovered with a bundled [COLMAP] build:
   feature extraction, matching, then the global mapper (the former GLOMAP
   pipeline, merged into COLMAP 4.0 when the standalone tool was retired),
   with live progress, per-phase stats and logs in the app. No system-wide
   installs needed
   (`scripts/fetch-sfm.sh` fetches CPU builds into `vendor/`).
3. **Train** — a 3D Gaussian splat is trained on the GPU via [brush]
   (burn/wgpu — works on any Vulkan-capable GPU, no CUDA required), with a
   live splat preview, PSNR/SSIM metrics, and pause/resume/stop control.
4. **Export** — save the result as standard binary **PLY**, compact **[SPZ]**,
   **[SOG]** (a web-friendly bundle, several times smaller than PLY on the
   scenes measured so far), or **[glTF]** with the `KHR_gaussian_splatting`
   extension. The SOG and glTF writers follow the published specs but have not
   yet been opened in a third-party viewer, and the glTF extension is a
   Khronos release candidate that may change before ratification.

Once a model is trained, the 3D view also does the finishing work:

- **Camera animation** — fly to a view, drop a keyframe, repeat. Keys are
  interpolated with a Catmull-Rom spline (adjustable smoothness, with
  ease in/out), and the move plays back live in the viewport.
- **Effects** — drop effect clips on the three lanes under the camera keys and
  drag them like clips in an editor: dissolves (sphere, box or plane), a scale
  build from dust, a crop sweep, noise and wave distortion, explode, a point
  cloud collapse, plus fade, vignette, light leak, grain, RGB split and block
  glitch. Click a clip to tune it. Effects show while you scrub, not only on
  playback, and are baked into the exported video.
- **Colour grading** — exposure, contrast, saturation, white balance,
  shadow/midtone/highlight wheels, an ACES tone-map toggle and a background
  colour. The grade is applied by the same shader that draws the viewport,
  so what you see is what renders.
- **Video export** — render the move to MP4 (H.264 or H.265), WebM (VP9) or
  a PNG sequence with alpha. Video encoding shells out to `ffmpeg`; the PNG
  sequence needs nothing but OpenGaussian, and formats your ffmpeg cannot
  write are greyed out rather than failing mid-render.

Everything is a plain directory on disk (`project.json`, `images/`,
`sparse/`, `checkpoints/`, `source/`, `camera.json`), so intermediate results are inspectable and
reusable with other 3DGS tooling.

[COLMAP]: https://colmap.github.io
[brush]: https://github.com/ArthurBrussee/brush
[SPZ]: https://github.com/nianticlabs/spz
[SOG]: https://developer.playcanvas.com/user-manual/gaussian-splatting/formats/sog/
[glTF]: https://github.com/KhronosGroup/glTF/blob/main/extensions/2.0/Khronos/KHR_gaussian_splatting

## Install / build

There are no packaged builds yet (Flatpak is on the roadmap). To build from
source you need Rust (edition 2024), GTK4 + libadwaita, and GStreamer
development packages — see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for
the full prerequisite list and troubleshooting. In short:

```sh
git clone https://github.com/silkepilon/OpenGaussian
cd OpenGaussian
scripts/fetch-sfm.sh        # bundled COLMAP 4.1+ into vendor/sfm
cargo run --release
```

## Quickstart

1. Launch OpenGaussian and create a project (a folder that will hold
   everything the pipeline produces).
2. **Import**: drop in 20–200 photos of a scene, or add a video walkthrough
   from a file or a YouTube link and mark the sections worth keeping.
   Move around the subject as you capture — parallax is what makes the
   reconstruction work; avoid pure rotation from one spot.
3. **Poses**: pick the matcher (*Sequential* for video frames, *Exhaustive*
   for unordered photos) and run it. You want most of your images
   registered; if too few register, capture with more overlap.
4. **Train**: start training and watch the splat take shape in the live
   preview. The defaults (30k steps) give good quality; a few thousand
   steps is enough for a rough preview. PSNR/SSIM curves show convergence.
5. **Export**: save as PLY (interoperable, big), SPZ (compressed), SOG
   (smallest, web-friendly), or provisional glTF, and drop the file into a
   splat viewer that supports the format.

## Roadmap

| Milestone | Theme                                                              |
| --------- | ------------------------------------------------------------------ |
| **M1**    | v1 pipeline: import → poses → train → export (this release)        |
| **M2**    | Camera-path waypoints and video export of splat flythroughs        |
| **M3**    | Advanced training profiles (quality/speed presets, more knobs)     |
| **M4**    | Flatpak packaging and Flathub release                              |

## Testing

`cargo test --workspace` runs GPU-free unit tests. A full end-to-end
pipeline test (real photos → SfM → GPU training → export) is gated behind
`--ignored`; see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#running-tests)
for how to fetch the small test dataset and run it.

## License

OpenGaussian is free software, licensed under the
**GNU General Public License v3.0 or later** (GPL-3.0-or-later).

It stands on:

- [brush] — Gaussian-splat training/rendering, **Apache-2.0**;
- [COLMAP] — feature extraction, matching & global mapping, **new BSD
  (BSD-3-Clause)**.

COLMAP is not linked in; it is a separate executable invoked as a
subprocess (fetched by `scripts/fetch-sfm.sh`, not distributed with this
repository).

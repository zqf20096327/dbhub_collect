<div align="center">

<img src="../opengaussian/logo.png" alt="OpenGaussian" width="128">

# OpenGaussian

**Train, view, edit and export 3D Gaussian Splatting scenes on Windows.**

Part of the [Open3D suite](https://github.com/carlesllavata/Open3D) · Based on [LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio) · GPL-3.0-or-later

</div>

OpenGaussian is [LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio) under another name, built and
shipped for free as part of the Open3D suite. It keeps LichtFeld Studio's features and follows its development
closely; the differences are listed below.

> **Status:** early development (0.x). The current version is **0.1.0**, based on LichtFeld Studio 0.5.5 in
> development.

## What it does

- Train 3D Gaussian Splatting scenes from photos (COLMAP and other dataset layouts) and resume from checkpoints.
- Watch the scene while it trains and inspect it in real time afterwards.
- Select, transform and edit splats, with undo and redo.
- Export to `PLY`, `SOG`, `SPZ`, `USD` or a standalone HTML viewer.
- Extend it with Python plugins from the plugin catalogue, and automate it with embedded Python or MCP.
- Run training without the interface from the command line (`OpenGaussian.exe --help`).

## Differences from LichtFeld Studio

- Name, icon and version: `OpenGaussian.exe`, version 0.x. The About window also shows the LichtFeld Studio
  version it is based on.
- No accounts: the LichtFeld Portal account, the online Gallery and the in-app bug report form are switched off.
  *Help > Report a bug* opens this repository's issues.
- The start screen has no links to LichtFeld Studio's community, donations or sponsors.
- Interface in English and Spanish only.
- Settings, plugins, logs and caches live in `%USERPROFILE%\.opengaussian`, so it does not share them with an
  installed LichtFeld Studio.
- GPU JPEG decoding works without installing the CUDA Toolkit (nvJPEG ships with the program).

## Requirements

- Windows 10 or 11, 64-bit.
- An NVIDIA GPU with compute capability 7.5 or newer (GTX 16 series, RTX 20 series and later). AMD, Intel and
  GTX 10 series or older GPUs are not supported.
- NVIDIA driver 570 or newer.
- About 700 MB of disk space, plus room for your projects.

The first start on a computer takes longer than the next ones: the GPU code is compiled for your graphics card
and kept for later.

## Install and uninstall

Download `opengaussian-<version>-windows-x64.zip` from the
[releases](https://github.com/carlesllavata/OpenGaussian/releases), unzip it anywhere and run
`bin\OpenGaussian.exe`. Keep the folders together: the program needs them. To uninstall, delete the folder.
Your settings in `%USERPROFILE%\.opengaussian` are kept; delete that folder to remove them too.

The [Open3D launcher](https://github.com/carlesllavata/Open3D) will install, update and uninstall OpenGaussian
once it lists it; it is not in the launcher yet.

## Build from source

You need Visual Studio 2022 (17.10 or newer, with the C++ workload and the *C++ Clang Compiler for Windows*
component), CUDA Toolkit 12.8 or newer, CMake 3.30 or newer, Ninja and [vcpkg](https://github.com/microsoft/vcpkg)
(`VCPKG_ROOT` set). From an *x64 Native Tools Command Prompt for VS 2022*:

```bat
set VCPKG_ROOT=C:\path\to\vcpkg
set VCPKG_BUILD_TYPE=release
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_PORTABLE=ON -DBUILD_PYTHON_STUBS=OFF ^
      -DCMAKE_TOOLCHAIN_FILE=%VCPKG_ROOT%/scripts/buildsystems/vcpkg.cmake
cmake --build build
```

`vcvars64.bat` sets `VCPKG_ROOT` to the copy of vcpkg bundled with Visual Studio, which is why it is set again
afterwards. The first build compiles about 80 dependencies and takes a while. The program ends up in
`build\OpenGaussian.exe`. To make the release zip, run
`powershell -ExecutionPolicy Bypass -File opengaussian\package.ps1 -BuildDir build -OutDir dist` on a committed
tree. Everything specific to OpenGaussian lives in [`opengaussian/`](../opengaussian); see
LichtFeld Studio's [build guide](../docs/building_and_distribution.md) for more options.

## License

OpenGaussian is licensed under the GNU General Public License v3.0 or later (`GPL-3.0-or-later`), like
LichtFeld Studio; see [`LICENSE`](../LICENSE). It includes LichtFeld Studio's additional permission for NVIDIA GPU
libraries, see [`LICENSE-EXCEPTION.txt`](../LICENSE-EXCEPTION.txt). Third-party components keep their own
licenses; release packages list them in `THIRD-PARTY-LICENSES.md`.

## Credits

OpenGaussian is built on [LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio) by the LichtFeld Studio
Authors. All the training, rendering and editing work is theirs; please support the original project.
Version history: [`CHANGELOG.md`](../CHANGELOG.md).

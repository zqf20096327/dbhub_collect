# OpenGaussSplat (OGS)

A high-performance, compute-driven Gaussian Splatting rendering library built in pure C.

## Overview
OpenGaussSplat provides a minimalist, "bare-metal" API to render and process Gaussian Splats directly on the GPU. By bypassing traditional rasterization pipelines, OGS utilizes Vulkan Compute queues for tile-based splatting, providing a streamlined alternative to complex graphics frameworks.

## Key Features
- **Compute-Only:** Zero overhead from vertex/fragment pipelines.
- **C-Native:** ABI-stable API, easy to bind to any language.
- **Zero-Copy:** Designed for high-speed streaming of `.ogs` files.
- **Lean:** No heavy dependencies—just the Vulkan loader (`volk`).

## Quick Start
```c
#include <ogs.h>

int main() {
    OgsContext* ctx = ogsInit();
    OgsBuffer buffer = ogsLoadBuffer(ctx, "scene.ogs");

    // Main Loop
    while (running) {
        ogsRender(ctx, buffer, camera);
    }

    ogsShutdown(ctx);
    return 0;
}
```

## Building
OGS uses CMake to ensure cross-platform compatibility.
```bash
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release # Or omit for Debug
cmake --build build
```

## Development Status
- Backend: Vulkan Compute (SPIR-V)
- Status: VERY Early development. API subject to LARGE changes.
- Target: Cross platform, but focused and tested on Linux with NVIDIA for now (because that's what I have, contributor testing welcome and appreciated).



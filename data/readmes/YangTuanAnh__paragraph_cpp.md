# Paragraph (C++)

## Why?

Detailed post: [Alpha release of Paragraph - The Good, The Bad, The Whimsy, The 4%](https://www.yangtuananh.dev/posts/alpha_release_of_paragraph)

Original post: [I'm releasing Paragraph (soon)!](https://www.yangtuananh.dev/posts/im_releasing_paragraph)

Windows Release: [Paragraph-0.1.0-win64.zip](https://github.com/YangTuanAnh/paragraph_cpp/releases/tag/pre-release)

TODO:
- [ ] Markdown notes editor
- [ ] MCP Server
- [ ] More unit, E2E tests
- [ ] R&D for graph theoretic functionalities

## Getting started - How to build the code

You'll need to have installed the following:
- A compiler (e.g., Visual Studio Code, Visual Studio on Windows, XCode on MacOS X, or GCC)
- CMake - download from https://cmake.org/download/

If you're using Visual Studio Code, then install the following extensions:
- C/C++ (make sure it's the one written by Microsoft)
- CMake Tools

Open a shell window, and type the following:
```
mkdir build
cd build
cmake ..
cmake --build .
```

## Authors and acknowledgment
Thanks to:
- Hans de Ruiter - [Building a Cross-Platform C++ GUI App with CMake, Raylib, and Dear ImGui
](https://keasigmadelta.com/blog/building-a-cross-platform-c-gui-app-with-cmake-raylib-and-dear-imgui/)
- Jeffery Myers - the creator of rlImGui (the glue between Raylib and Dear IMGUI)
- Omar Cornut - the creator of Dear IMGUI
- Ramon Santamaria - for creating Raylib
- All contributors to Raylib, rlImGui, & Dear IMGUI

## License
See [LICENSE.md](LICENSE.md)

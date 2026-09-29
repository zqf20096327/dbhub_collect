# SharpShort

A lightweight, zero-dependency URL shortener built with **C#**, **ASP.NET Core Minimal APIs**, and **Entity Framework Core with SQLite**.

SharpShort demonstrates how to build a high-performance web API in a single C# file using top-level statements, modern async patterns, and base-62 encoding to turn database auto-increment IDs into compact short codes.

---

## Features

- **Minimal APIs**: Built on ASP.NET Core for low memory footprint and fast request processing.
- **SQLite Database**: Persistent data storage with zero setup required via EF Core (`EnsureCreated()`).
- **Base62 Encoding**: Custom encoder that converts integer primary keys (`1`, `1005`) into short, alphanumeric codes (`1`, `gd`).
- **URL Validation**: Verifies incoming URLs for valid HTTP/HTTPS schemes before saving.
- **302 Temporary Redirects**: Ensures redirection while allowing click tracking and analytics.

---

## Project Structure

The entire application runs from a single file, structured according to C# top-level statement requirements:

```text
SharpShort/
├── Program.cs           # Main application entry point & types
├── shortener.db         # Auto-generated SQLite database (created on first run)
└── sharpshort.csproj    # Project dependencies
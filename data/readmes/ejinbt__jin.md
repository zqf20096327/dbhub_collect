<p align="center">
  <img src="logo.png" alt="jin" width="200">
</p>

# jin

A performance-oriented, reactive version control system written in Go. Built on top of [GoldenDB](https://github.com/ejinbt/goldendb) — a reactive, SQLite-backed embedded database — as its storage and sync engine.

Git's `status`, `diff`, and `log` are slow on large codebases because they scan the working tree on demand. jin inverts this: a file watcher pushes changes into GoldenDB reactively, so `status` is always O(1), never O(n).

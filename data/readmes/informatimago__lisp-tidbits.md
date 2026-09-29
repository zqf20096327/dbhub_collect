;; -*- mode:org;coding:utf-8 -*-

* Common Lisp Tidbits

This repository contains small useless lisp programs and tidbits.


* Build System

You can build all the programs with GNU `make` in the root directory.

The `Makefile` in the root directory has four targets: `all`, `test`, `run`, and `clean`,
and it runs make in each of the subdirectories.

The `Makefile`s in the subdirectories include `generate.mk` which
contains implicit rules to compile the programs.

The rule to compile those lisp programs run a CL implementation
without loading the user environment (rc files), following a
`generate-${program}.lisp` scrip, that loads `generate.lisp`.

`generate.lisp` loads quicklisp and contains code to configure asdf,
compile and load the program, and save an executable image.

It is called from `generate-${program}.lisp` with the right parameter
for each program.


* License

All this code is released under the AGPL3 license, as if it was of any use to anybody.

Copyright 2020 Pascal J. Bourguignon <pjb@informatimago.com>


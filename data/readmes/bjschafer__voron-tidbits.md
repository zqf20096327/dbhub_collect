# Voron Tidbits

This repo contains thing(s) I've created or unearthed that are useful when doing Voron things.

## `generate-csv.sh`

This script is run against a tree of STLs as found in many of the Voron repos. It spits out a CSV in a useful-ish format
designed to be imported into GSheets or Excel.

Requirements: `bash`, GNU `awk`.

Invocation: `./generate-csv.sh ~/Downloads/Voron-Trident/STLs`

Useful notes:

- If you want the links to generate correctly, update the link path in the beginning of `process-path.awk`. Then they'll import all clicky-like.
- To add more sheets to the same Sheet (lol), go to File -> Import -> Upload -> Insert new sheet(s) and ensure the "Convert text to numbers, dates, and formulas" is checked.

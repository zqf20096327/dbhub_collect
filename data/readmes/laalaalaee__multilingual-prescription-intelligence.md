# AI-Powered Multilingual Prescription Intelligence System

Upload a photo of a handwritten prescription. The app reads it, picks out the medicines, warns about known drug interactions, and can translate the result into Hindi or French.

Made by [@laalaalaee](https://github.com/laalaalaee) and [@RishabRathi](https://github.com/RishabRathi) for our NTCC (in-house practical training) project, summer 2026.

This is a student prototype, not a medical tool. Don't use it to make real medical decisions.

## How it works

1. The browser uploads the image to a FastAPI server, which checks the file and rejects blurry photos straight away.
2. A background worker cleans the image, splits the page into lines, and reads each line with TrOCR.
3. Words in the text are fuzzy-matched against known medicine names (RapidFuzz).
4. Every pair of medicines found is looked up in a MySQL/MariaDB table of known interactions.
5. The text can be translated to Hindi or French with MarianMT.
6. The page polls the server for the result, and every request is logged to the database.

The dashboard is served by the same FastAPI process at `/dashboard`, so one command runs everything.

## Running it

You need Python 3.11+, a MySQL or MariaDB server, and preferably an NVIDIA GPU.

```bash
git clone https://github.com/laalaalaee/multilingual-prescription-intelligence
cd multilingual-prescription-intelligence

python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/macOS: source .venv/bin/activate

# PyTorch first. With an NVIDIA GPU:
pip install torch --index-url https://download.pytorch.org/whl/cu128
# Without one (works, but is slow):
# pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements.txt

# Database: create an empty one, then load the tables
mysql -u <user> -p -e "CREATE DATABASE prescriptions;"
mysql -u <user> -p prescriptions < db/schema.sql

# Settings: copy the template and fill in your database details
cp .env.example .env            # PowerShell: copy .env.example .env

python app.py                   # then open http://localhost:8000/dashboard
```

The first start downloads the AI models (a few GB) and takes a couple of minutes. The console says `Loading OCR model on cuda...` when the GPU is used and `... on cpu...` when it isn't.

If something goes wrong:

- `KeyError: 'DB_HOST'` on start means `.env` is missing or empty.
- "Failed to process the prescription image" after an upload is usually the database being unreachable or the schema not loaded. The real error is in the console.
- `on cpu` when you have a GPU means PyTorch can't see it: reinstall with the CUDA command above and update your NVIDIA driver.

To run the tests: `pip install pytest` and then `python -m pytest tests`. They cover the medicine matching and don't need a database or the models.

## Speed

Reading one page with four handwritten lines took about 2 to 3 seconds on an RTX 4060 and 36 to 60 seconds on a desktop CPU, with identical output. The GPU is used automatically when PyTorch can see one.

## How well does it work?

We haven't tested on a large set of real prescriptions, so there is no overall accuracy figure. This is what we did measure:

| Test | Result |
|---|---|
| Medicine matching: the 10 rulebook drugs with 0, 1, 2 and 3 random typos (200 each) | 100%, 100%, 57% and 25% found; never matched to the wrong drug |
| False alarms: 80 other drug names and common prescription words | 0 matched to a rulebook drug |
| OCR on two test pages (10 lines) | 5.6% of characters wrong on the medicine lines; 4 of 6 medicine names exactly right. The "Rx:" header and signature are read worst: 16.3% over all lines |
| Blur check on a sharp page | accepted at every size tested, from 445 to 3560 px wide |
| Blur check on blurred copies | accepted up to a blur of 1.5 px, rejected from 2 px. Reading errors grow from 3.5% (sharp) to 8-12% (slightly blurred) and 18-64% (heavily blurred) |

The two test pages are digitally made handwriting-style images, not photos of real prescriptions, and ten lines is a very small sample. Real handwriting will be harder. The matching numbers can be reproduced with `python evaluation/matcher_benchmark.py`.

## Limitations

- The rulebook has five interaction pairs. "No known interaction found" means "not one of those five", not "safe".
- OCR works well on clean, well-lit handwriting. Phone photos and messy writing give much worse results.
- Medicine names are matched approximately, so a misread name can be missed or, rarely, matched to the wrong medicine.
- Translation is general-purpose and runs on the OCR text, so OCR mistakes get translated too.
- Every analysed image's text is saved in `prescription_logs`. Don't run real patients' prescriptions through a copy you don't control.
- There are no user accounts, rate limiting or HTTPS. It is built to run on your own machine, not to be put on the internet as it is.

## Project layout

```
api/        FastAPI app: upload checks, job queue, endpoints
models/     preprocessing, OCR, interaction matching, translation
db/         connection settings, logging, schema.sql (tables and the five rules)
frontend/   the dashboard (index.html, app.js)
tests/      unit tests for the matching logic
app.py      entry point
```

## Credits

Handwriting recognition uses Microsoft's [TrOCR](https://huggingface.co/microsoft/trocr-large-handwritten) (MIT) and translation uses Helsinki-NLP's [opus-mt](https://huggingface.co/Helsinki-NLP/opus-mt-en-hi) models (CC-BY 4.0), downloaded from Hugging Face on first run. Name matching uses [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz) (MIT). During development we used the [IAM Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-handwriting-database), which can't be redistributed, so it isn't included.

## Licence

MIT, see [LICENSE](LICENSE). It covers this repository's own code, not the models above.

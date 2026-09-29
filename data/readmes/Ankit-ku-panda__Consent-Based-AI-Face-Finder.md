# Consent-Based AI Face Finder

A privacy-focused Python and OpenCV project that finds **possible face matches only inside a private, consented database**. It does not scrape social media, search the public internet, identify arbitrary strangers, or locate someone in the real world.

## Main features

- Enroll a participant using one to three authorized photos
- Require explicit consent before enrollment
- Detect and align faces with OpenCV YuNet
- Generate facial features with OpenCV SFace
- Encrypt facial features and thumbnails before SQLite storage
- Process query photos in memory without saving them
- Rank possible candidates using cosine similarity
- Delete an enrolled profile using its reference code
- Maintain a privacy audit log
- Reject photos containing zero or multiple faces

## Important safety boundary

Use this project only for your own photos, opted-in participants, or datasets you are legally authorized to process. Do not use it for stalking, surveillance, scraping websites, policing, employment, lending, housing, healthcare, or any other high-impact decision.

A similarity score is **not proof of identity**. Every result requires human verification. Real-world performance varies with lighting, pose, age, camera quality, occlusion, and the population being evaluated.

## Project structure

```text
consent-face-finder/
├── app.py                    # Streamlit user interface
├── download_models.py        # Downloads official OpenCV models
├── src/
│   ├── config.py             # Paths and conservative defaults
│   ├── database.py           # Encrypted SQLite profile storage
│   ├── face_engine.py        # Detection, alignment and feature extraction
│   ├── matching.py           # Normalization and cosine ranking
│   └── security.py           # Local Fernet encryption
├── tests/                    # Automated unit tests
├── data/                     # Local database and key; ignored by Git
├── models/                   # Downloaded ONNX models; ignored by Git
├── requirements.txt
└── LICENSE
```

## Requirements

- Windows, Linux, or macOS
- Python 3.10 or 3.11 recommended
- Internet access once to download the two official model files
- No GPU is required

## Installation on Windows PowerShell

```powershell
cd consent-face-finder
py -3.11 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python download_models.py
streamlit run app.py
```

Open the local address printed in the terminal, normally `http://localhost:8501`.

## Installation on Linux or macOS

```bash
cd consent-face-finder
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python download_models.py
streamlit run app.py
```

## How to use it

1. Open **Enroll**.
2. Enter the participant's approved name.
3. Upload one to three clear photos containing exactly one face each.
4. Record the participant's consent and create the encrypted profile.
5. Save the generated reference code for future deletion requests.
6. Open **Search** and upload an authorized query photo.
7. Review possible candidates manually; never treat the score as confirmed identity.
8. Use **Manage data** to inspect or delete enrolled profiles.

## Similarity threshold

The app uses a conservative default cosine threshold of `0.50`. The OpenCV SFace documentation reports different thresholds for different evaluation datasets, so a production deployment must calibrate its threshold on a representative, consented validation set. Raising the threshold generally reduces false positives but increases false negatives.

Do not convert similarity into a made-up “identity confidence percentage.”

## Storage and privacy

- `data/facefinder.db` contains encrypted facial features and aligned thumbnails.
- `data/.facefinder.key` is generated automatically on first run.
- Query images are not inserted into the database.
- Original enrollment photos are not stored; only one aligned face thumbnail is retained.
- The `data` directory and ONNX files are excluded from Git.

Back up the database and key together if you need recovery. Losing the key makes the encrypted records unreadable. Never commit or share the key.

For a shared environment, set an admin PIN before starting Streamlit:

```powershell
$env:FACEFINDER_ADMIN_PIN="use-a-long-random-secret"
streamlit run app.py
```

```bash
export FACEFINDER_ADMIN_PIN="use-a-long-random-secret"
streamlit run app.py
```

This demo PIN protects only the management screen. Before any real deployment, add proper authentication, HTTPS, role-based authorization, rate limits, retention rules, backups, monitoring, and a jurisdiction-specific privacy review.

## Run the tests

```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
pytest -q
ruff check .
```

## Model sources and licenses

The download script retrieves model files from the official OpenCV Zoo:

- [YuNet face detector](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)
- [SFace face recognizer](https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface)
- [OpenCV face detection and recognition documentation](https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html)

The model files have their own upstream licenses and are not included in this project archive.

## License

The application code is available under the MIT License. This does not grant permission to collect or process another person's biometric data.

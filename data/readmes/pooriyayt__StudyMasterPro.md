# StudyMaster Pro


🚀 StudyMaster Pro is a desktop application designed to help users manage their study sessions effectively. It includes a Pomodoro timer ⏱️, subject tracking with progress visualization 📊, a Jalali (Persian) calendar for viewing study history 📅, customizable themes 🎨, and a SQLite database for storing sessions. Built with Python 3 and PyQt5, it's ideal for students and professionals looking to improve productivity 💪.

**Note:** ⚠️ This project is released under a custom license. All rights reserved. No copying, modification, or distribution is allowed without explicit permission from the author.

## Features 📋
- **Pomodoro Timer:** ⏳ Customizable study sessions (15, 25, or 50 minutes) with pause, reset, and save functionality.
- **Subject Management:** 📚 Add, delete, and track subjects with target minutes and progress tracking.
- **Progress Charts:** 📈 Visual pie charts showing completion percentages for subjects.
- **Jalali Calendar:** 🗓️ View monthly study calendars with highlighted study days, daily/weekly/monthly summaries.
- **Themes:** 🌈 Multiple light and dark themes (e.g., green, blue, purple) for a personalized UI.
- **Statistics:** 📉 View detailed session history and export to CSV.
- **Persian Support:** 🇮🇷 Full support for Persian text and Fingilish transliteration.
- **Cross-Platform:** 🖥️ Runs on Windows, macOS, and Linux (tested on Python 3.12).

## Prerequisites ✅
- Python 3.12+ (download from [python.org](https://www.python.org/))
- PyQt5 and other dependencies (listed in requirements.txt)

## Installation 🛠️
1. **Clone the Repository:** 📥
```bash
git clone https://github.com/pooriyayt/StudyMasterPro.git
```
```bash
cd study-master-pro
```

3. **Create a Virtual Environment (Recommended):** 🐍
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Linux/macOS
```
```bash
venv\Scripts\activate     # On Windows
```
3. **Install Dependencies:** 📦

Create a `requirements.txt` file with the following content (or use the one if provided):
```
PyQt5==5.15.10
numpy==1.26.4
matplotlib==3.9.2
```
Then run:
```bash
pip install -r requirements.txt
```

**Note:** ℹ️ The app uses additional libraries like `sqlite3` (built-in), `datetime`, etc., which don't need installation. For Persian font support, ensure `Vazir.ttf` is in the `font/` directory (or fallback to Tahoma).

4. **Prepare Resources:** 🗂️
- Place `Vazir.ttf` in a `font/` folder in the project root.
- (Optional) Add an icon file like `icon.png` in the root for the app icon.

## Running the App ▶️
1. Activate the virtual environment (if used).
2. Run the main script:
```bash
python main.py
```
4. The app will launch. Add subjects, start timers, and track your progress! 🎉

## Building an Executable (Optional) 🏗️
To create a standalone executable (e.g., for Windows):
1. Install PyInstaller:
```bash
pip install pyinstaller
```
3. Run:
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```
- This creates a `.exe` in the `dist/` folder.
- Ensure resource paths (fonts, icons) are handled correctly via the `resource_path` function in the code.

## Troubleshooting ❓
- **Font Issues:** 🔤 If Persian text doesn't display correctly, ensure `Vazir.ttf` is present and the path is correct.
- **Dependencies Errors:** ⚙️ Check Python version and reinstall packages if needed.
- **Calendar Errors:** 📆 Jalali date conversions are custom—report issues if dates are off.
- **Windows Icon:** 🖼️ The app sets a custom icon; if it doesn't show, ensure `icon.png` or `icon.ico` is in the root.

## Contributing 🤝
This project is not open for contributions due to the custom license. If you have suggestions, contact the author.

## License 📜
See [LICENSE](LICENSE) for details. All rights reserved.

## Author 👤
[Pouriya Parniyan](https://pouriyaparniyan.ir) / [@pooriyayt](https://github.com/pooriyayt/)

If you find this useful, star the repo! ⭐

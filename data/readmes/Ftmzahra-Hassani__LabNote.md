# LabNote

LabNote is an offline desktop application for organizing scientific experiments,
recording numeric measurements, calculating descriptive statistics, and fitting
a simple linear model.

## Features

- Tkinter desktop interface
- SQLite database with experiment/measurement relationships
- Create, edit, search, and delete experiments
- Add and delete numeric measurements
- Mean, median, variance, and standard deviation
- Least-squares linear regression and R-squared
- Scatter plot and regression line drawn with Tkinter Canvas
- Export experiment data to CSV
- Unit tests for the calculation functions

## Requirements

- Python 3.10 or newer recommended
- Tkinter available in the Python installation
- No third-party packages are required

## Run

```bash
python main.py
```

The SQLite database (`labnote.db`) is created automatically in the project folder.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Sample data

The `sample_data/ohms_law.csv` file contains example values for Ohm's law.
Create an experiment named `Ohm's Law` and enter the values from this file
manually through the Measurements window.

## Project structure

- `database/`: SQLite schema and database operations
- `core/`: validation and scientific calculations
- `ui/`: Tkinter application and styling
- `utils/`: CSV export
- `tests/`: automated tests
- `sample_data/`: sample measurement data

## License

MIT

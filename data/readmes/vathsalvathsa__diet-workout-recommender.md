# Diet and Workout Recommendation System

A full-stack-style Python project that recommends a **workout plan** and a **diet plan** from a person's body metrics, activity level, goal and food preference. It combines machine learning (KNN and Decision Trees), a REST API (Flask) and a SQL database (SQLite), and it exports data for dashboards in Power BI or Excel.

> **About the data:** all training and demo data is **synthetic**. Plan labels come from simple, documented rules (see `src/generate_data.py`) with 5% random label noise. The model accuracy shown below therefore measures how well the models learn those rules, **not** how effective the plans are for real people. This is a learning project, not medical advice.

## Features

- **Body metrics:** BMI, BMR (Mifflin-St Jeor), daily energy needs (TDEE), calorie target and protein/fat/carb targets.
- **ML recommendations:** KNN and Decision Tree classifiers predict the workout plan and diet plan. The better model on the test set is used, and both predictions are returned.
- **Safety rules:** underweight users never get a calorie deficit, and calorie targets never drop below a floor (1200 kcal for women, 1500 kcal for men).
- **Meal suggestions** for vegetarian, vegan and non-vegetarian preferences, split across breakfast, lunch, snack and dinner.
- **REST API** with input validation and clear error messages.
- **SQL database** storing users and recommendation history, plus an aggregate stats query.
- **BI export:** a flat CSV joined from the SQL tables, ready to load into Power BI or Excel.

## Model results (synthetic data, 1,500 users, 80/20 split)

| Target | KNN test accuracy | Decision Tree test accuracy | Model used |
|---|---|---|---|
| Workout plan | 0.843 | 0.923 | Decision Tree |
| Diet plan | 0.950 | 0.967 | Decision Tree |

Cross-validation scores are in `models/metrics.json`, and `output/feature_importance.png` shows which inputs the trees rely on.

## Project structure

```
├── src/
│   ├── config.py           # constants, limits, calorie factors
│   ├── features.py         # BMI, BMR, TDEE, macros, input validation
│   ├── generate_data.py    # synthetic dataset + labelling rules
│   ├── train.py            # trains KNN and Decision Tree, saves models
│   ├── plans.py            # workout schedules and meal suggestions
│   ├── recommender.py      # profile -> full recommendation
│   ├── db.py               # SQLite schema, history, stats, CSV export
│   ├── app.py              # Flask REST API
│   └── seed_demo.py        # fill a demo DB through the API and export CSV
├── tests/test_recommender.py
├── data/synthetic_users.csv
├── models/                 # trained models + metrics
└── output/                 # feature importance chart, sample BI export
```

## Quick start

```bash
pip install -r requirements.txt

python -m src.generate_data      # optional: data is already included
python -m src.train              # optional: trained model is already included
python -m src.app                # API at http://127.0.0.1:5000
```

Get a recommendation:

```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo", "age": 22, "gender": "male", "height_cm": 175, "weight_kg": 68,
       "activity_level": "moderate", "goal": "build_muscle", "diet_preference": "vegetarian"}'
```

Allowed values: `gender` = female | male; `activity_level` = sedentary | light | moderate | active; `goal` = lose_weight | maintain | build_muscle; `diet_preference` = vegetarian | vegan | non_vegetarian. Age 18-75, height 120-220 cm, weight 30-200 kg.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service check |
| POST | `/recommend` | Get and save a recommendation (optional `user_id` to add to an existing user's history, optional `name`) |
| GET | `/users/<id>/history` | Past recommendations for a user |
| GET | `/stats` | Recommendation counts and averages by plan (SQL `GROUP BY`) |

Tests:

```bash
python -m unittest discover -s tests -t .
```

## Power BI / Excel

```bash
python -m src.seed_demo --users 200
```

This creates `output/recommendations_export.csv` (synthetic demo users). Load it in Power BI or Excel to build charts such as plan mix by goal or average target calories by BMI category.

## Limitations

- Synthetic data and rule-based labels, so results are illustrative only.
- Not a substitute for advice from a doctor or dietitian.
- The API has no authentication, and it is meant for local use and learning.

## Skills demonstrated

Python, pandas, scikit-learn (KNN, Decision Trees, cross-validation), Flask REST API design, SQL (SQLite schema, joins, aggregates), input validation, unit testing, data export for BI tools, documentation.

## Licence

MIT. See `LICENSE`.

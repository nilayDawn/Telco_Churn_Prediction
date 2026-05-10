# Student Exam Performance Indicator (Math Score Prediction)

This project trains a regression model to predict a student’s **Math score** based on exam and demographic features. It also includes a **Flask** web app to make predictions using the trained model.

---

## Project Structure

- **app.py** – Flask application (HTML form + `/predictdata` endpoint)
- **src/** – ML pipeline code
  - **src/components/**
    - `data_ingestion.py` – loads raw dataset and creates train/test CSVs in `artifacts/`
    - `data_transformation.py` – builds and saves a preprocessing pipeline (`preprocessor.pkl`)
    - `model_trainer.py` – trains multiple regressors (with GridSearchCV) and saves best model (`model.pkl`)
  - **src/pipeline/**
    - `train_pipeline.py` – end-to-end training script logic (ingest → transform → train)
    - `predict_pipeline.py` – loads model + preprocessor and performs prediction
  - `utils.py` – helpers for saving/loading pickles and evaluating models
- **templates/** – Flask HTML templates
  - `index.html` – landing page
  - `home.html` – prediction form
- **artifacts/** – persisted model/preprocessor and generated datasets
- **notebook/** – notebooks used during development

---

## Dataset

The training dataset is expected at:

- `notebook/data/stud.csv`

The target column used in training is:

- **`math_score`**

Input features:

- Categorical:
  - `gender`
  - `race_ethnicity`
  - `parental_level_of_education`
  - `lunch`
  - `test_preparation_course`
- Numerical:
  - `reading_score`
  - `writing_score`

---

## Training Pipeline

### What the training does
1. **Data ingestion**: reads `notebook/data/stud.csv`, then writes
   - `artifacts/data.csv` (raw copy)
   - `artifacts/train.csv`
   - `artifacts/test.csv`
2. **Data transformation**: builds a `ColumnTransformer`:
   - Numerical pipeline: `SimpleImputer(median)` + `StandardScaler`
   - Categorical pipeline: `SimpleImputer(most_frequent)` + `OneHotEncoder` + `StandardScaler(with_mean=False)`
   - Fits on train features and saves preprocessing to:
     - `artifacts/preprocessor.pkl`
3. **Model training**:
   - Trains several regressors (Random Forest, Decision Tree, Gradient Boosting, Linear Regression, XGBoost, CatBoost, AdaBoost)
   - Uses **GridSearchCV** for hyperparameters
   - Selects the best model based on test **R²**
   - Saves the best estimator to:
     - `artifacts/model.pkl`

### Run training
You can run training via the notebook or by executing the pipeline module.

> Note: The repository includes a `src/pipeline/train_pipeline.py`. Training is typically initiated there through the pipeline components.

---

## Prediction Pipeline (Inference)

Prediction is handled by:

- `src/pipeline/predict_pipeline.py`

At inference time, it:
1. Loads:
   - `artifacts/model.pkl`
   - `artifacts/preprocessor.pkl`
2. Transforms incoming features with the saved preprocessor
3. Produces a single predicted value for **Math score**

---

## Web App (Flask)

### Endpoints
- `GET /` – renders `templates/index.html`
- `GET/POST /predictdata`
  - **GET**: renders the input form (`templates/home.html`)
  - **POST**: reads form values, predicts math score, and renders the result in `home.html`

### Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open:

- http://127.0.0.1:5000/

---

## Docker

Build and run the container:

```bash
docker build -t student-math-predictor .
docker run -p 5000:5000 student-math-predictor
```

Open:

- http://127.0.0.1:5000/

---

## Requirements

Python dependencies (from `requirements.txt`):

- pandas, numpy
- seaborn, matplotlib
- scikit-learn
- catboost, xgboost
- dill
- flask

---

## Notes / Known Considerations

- The preprocessing + model are serialized with `pickle`.
- The HTML form fields must match the feature names expected by `CustomData`:
  `gender`, `ethnicity` (race_ethnicity), `parental_level_of_education`, `lunch`, `test_preparation_course`, `reading_score`, `writing_score`.


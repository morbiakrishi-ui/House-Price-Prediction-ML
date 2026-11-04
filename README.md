# EstateIQ — House Price Prediction

A Streamlit dashboard for the House Price Prediction notebook supplied with this project.

## Included
- `Houseprediction.ipynb` — your supplied Jupyter notebook.
- `app.py` — premium multi-page Streamlit dashboard.
- `kc_house_data.csv` — King County House Sales dataset.
- `linear_regression_model.pkl`, `random_forest_model.pkl`, `preprocessing_artifacts.pkl` — trained model and preprocessing files.
- `requirements.txt` — deployment dependencies.

## Run locally
1. Keep all files in the same folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app: `streamlit run app.py`

## Deploy on Streamlit Community Cloud
1. Upload all files in this folder to one GitHub repository.
2. Open Streamlit Community Cloud and create a new app.
3. Select the repository, branch, and `app.py` as the main file.
4. Deploy.

## Important dataset note
The dataset contains historical house sales in King County, Washington, from 2014–2015. Prices and predictions are in US dollars (USD). This model is for academic demonstration and should not be used as a current appraisal or to estimate Indian property prices.

## Models
Only the two algorithms used in the notebook are included:
- Linear Regression
- Random Forest Regression

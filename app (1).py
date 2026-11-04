import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="EstateIQ | King County Property Intelligence",
    page_icon="⌂",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

# =========================================================
# 2. PREMIUM UI STYLING
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink:#172d28; --muted:#71827b; --green:#174d40; --green2:#276c58;
    --mint:#dcebe3; --gold:#c29a62; --paper:#f4f6f2; --line:#e4eae4;
}
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:var(--paper); color:var(--ink);}
.block-container {max-width:1440px; padding-top:1.25rem; padding-bottom:3rem;}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
[data-testid="stSidebar"] {background:#102f29; border-right:1px solid #24483e;}
[data-testid="stSidebar"] * {color:#eaf3ee !important;}
[data-testid="stSidebar"] .stRadio label {font-size:14px; padding:4px 0;}
[data-testid="stSidebar"] hr {border-color:#35574d;}
.brand-mark {
    width:42px;height:42px;border-radius:13px;background:#dcebe3;color:#174d40;
    display:flex;align-items:center;justify-content:center;font-size:25px;font-weight:800;
}
.brand-name {font-family:Manrope,sans-serif;font-size:20px;font-weight:800;color:white;letter-spacing:-.5px;}
.brand-caption {font-size:10px;color:#a9c6b9;letter-spacing:2px;text-transform:uppercase;}
.sidebar-note {background:#1b4036;border:1px solid #31594c;border-radius:13px;padding:13px;margin-top:20px;font-size:11px;color:#c6d9d0;}
.hero {
    background:linear-gradient(115deg,#102f29 0%,#174d40 58%,#2a715b 100%);
    border-radius:24px;padding:34px 38px;color:white;position:relative;overflow:hidden;
    box-shadow:0 16px 38px rgba(21,63,51,.14); margin-bottom:22px;
}
.hero:after {content:"⌂";position:absolute;right:50px;top:-72px;font-size:260px;line-height:1;color:rgba(255,255,255,.055);}
.hero-kicker {font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:#b7d7c8;font-weight:700;margin-bottom:12px;}
.hero h1 {font-family:Manrope,sans-serif;color:white;font-size:36px;line-height:1.15;letter-spacing:-1.3px;margin:0 0 10px 0;font-weight:800;}
.hero p {color:#d5e7df;font-size:14px;line-height:1.7;max-width:660px;margin:0;}
.hero-chip {display:inline-block;margin-top:18px;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.09);border-radius:30px;padding:7px 12px;font-size:10px;letter-spacing:.7px;color:#e8f4ee;}
.page-kicker {font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#668078;font-weight:800;margin:10px 0 5px;}
.page-title {font-family:Manrope,sans-serif;font-size:25px;font-weight:800;letter-spacing:-.7px;color:#173b33;margin:0 0 4px;}
.page-sub {font-size:13px;color:#75857e;margin:0 0 18px;}
.kpi {background:white;border:1px solid var(--line);border-radius:17px;padding:17px 18px;min-height:110px;box-shadow:0 5px 16px rgba(23,59,51,.035);}
.kpi-label {font-size:10px;letter-spacing:1.2px;text-transform:uppercase;color:#7b8b83;font-weight:700;}
.kpi-value {font-family:Manrope,sans-serif;font-size:25px;font-weight:800;letter-spacing:-.8px;color:#173b33;margin-top:8px;}
.kpi-foot {font-size:10px;color:#9aa69f;margin-top:3px;}
.panel {background:white;border:1px solid var(--line);border-radius:18px;padding:18px 20px;box-shadow:0 5px 16px rgba(23,59,51,.03);}
.panel-title {font-family:Manrope,sans-serif;font-size:15px;font-weight:800;color:#1c4036;margin-bottom:3px;}
.panel-sub {font-size:11px;color:#8a9891;margin-bottom:12px;}
div[data-testid="stForm"] {background:white;border:1px solid var(--line);border-radius:18px;padding:22px 24px;box-shadow:0 5px 16px rgba(23,59,51,.03);}
label {font-size:12px!important;font-weight:600!important;color:#40574e!important;}
.stNumberInput input,.stSelectbox div[data-baseweb="select"] {border-radius:9px!important;}
div.stButton>button,div[data-testid="stFormSubmitButton"]>button {
    background:#174d40;color:white;border:0;border-radius:10px;padding:12px 18px;
    font-weight:700;min-height:44px;transition:.2s;
}
div.stButton>button:hover,div[data-testid="stFormSubmitButton"]>button:hover {background:#236a55;color:white;border:0;transform:translateY(-1px);}
.result-hero {background:linear-gradient(120deg,#e3f0e8,#f7faf6);border:1px solid #d4e6d9;border-radius:20px;padding:24px 27px;margin:14px 0 18px;}
.result-label {font-size:10px;letter-spacing:1.8px;text-transform:uppercase;color:#638174;font-weight:800;}
.result-price {font-family:Manrope,sans-serif;font-size:42px;font-weight:800;letter-spacing:-1.5px;color:#174d40;margin:7px 0 2px;}
.result-caption {font-size:11px;color:#748b80;}
div[data-testid="stMetric"] {background:white;border:1px solid var(--line);border-radius:14px;padding:14px 16px;}
div[data-testid="stMetricLabel"] {color:#7c8d84;}
div[data-testid="stMetricValue"] {font-family:Manrope,sans-serif;color:#174d40;}
div[data-testid="stExpander"] {background:white;border:1px solid var(--line);border-radius:12px;}
div[data-testid="stAlert"] {border-radius:12px;}
.footer {text-align:center;color:#98a49d;font-size:10px;letter-spacing:.8px;padding-top:30px;}
hr {border-color:#e3eae4;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. LOAD DATA AND TRAINED MODELS
# =========================================================
@st.cache_data
def load_dataset():
    data = pd.read_csv(BASE_DIR / "kc_house_data.csv")
    return data

@st.cache_resource
def load_models():
    lr = joblib.load(BASE_DIR / "linear_regression_model.pkl")
    rf = joblib.load(BASE_DIR / "random_forest_model.pkl")
    prep = joblib.load(BASE_DIR / "preprocessing_artifacts.pkl")
    return lr, rf, prep

try:
    df = load_dataset()
    linear_model, random_forest_model, preprocessing = load_models()
    feature_columns = preprocessing["feature_columns"]
except Exception as error:
    st.error("Project files could not be loaded. Keep the CSV and all three .pkl files beside app.py.")
    st.exception(error)
    st.stop()

# =========================================================
# 4. SIDEBAR NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("""
    <div style="display:flex;gap:11px;align-items:center;margin:8px 0 8px;">
      <div class="brand-mark">⌂</div>
      <div><div class="brand-name">EstateIQ</div><div class="brand-caption">Property intelligence</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;letter-spacing:2px;color:#9bbbad;font-weight:700;margin-bottom:8px;'>WORKSPACE</div>", unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Predict a Price", "Market Explorer", "Model Insights"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("<div style='font-size:10px;letter-spacing:2px;color:#9bbbad;font-weight:700;'>DATA SOURCE</div>", unsafe_allow_html=True)
    st.markdown("**King County · Washington**")
    st.caption("May 2014 — May 2015")
    st.markdown(f"<div class='sidebar-note'>✦ &nbsp; {len(df):,} property transactions<br>✦ &nbsp; {df['zipcode'].nunique()} ZIP codes<br>✦ &nbsp; Two regression algorithms</div>", unsafe_allow_html=True)

# =========================================================
# 5. SHARED HEADER
# =========================================================
st.markdown("""
<div class="hero">
  <div class="hero-kicker">REAL ESTATE · DATA SCIENCE · MACHINE LEARNING</div>
  <h1>Understand the market.<br>Estimate with intelligence.</h1>
  <p>Explore historical King County property sales, discover housing patterns and estimate a property's value using two machine learning models.</p>
  <span class="hero-chip">KING COUNTY DATASET &nbsp; / &nbsp; 21,613 TRANSACTIONS</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 6. REUSABLE DATASET METRICS
# =========================================================
def show_kpis():
    cols = st.columns(4)
    metrics = [
        ("TOTAL TRANSACTIONS", f"{len(df):,}", "Historical property sales"),
        ("MEDIAN SALE PRICE", f"${df['price'].median():,.0f}", "Dataset median"),
        ("AVG. LIVING AREA", f"{df['sqft_living'].mean():,.0f} sq ft", "Interior living space"),
        ("LOCATIONS COVERED", f"{df['zipcode'].nunique()}", "Unique ZIP codes")
    ]
    for col, (label, value, foot) in zip(cols, metrics):
        col.markdown(f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div><div class='kpi-foot'>{foot}</div></div>", unsafe_allow_html=True)

# =========================================================
# 7. OVERVIEW PAGE
# =========================================================
if page == "Overview":
    st.markdown("<div class='page-kicker'>MARKET AT A GLANCE</div><div class='page-title'>Your housing market dashboard</div><div class='page-sub'>A data-led snapshot of the properties represented in the training dataset.</div>", unsafe_allow_html=True)
    show_kpis()
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])
    with left:
        st.markdown("<div class='panel'><div class='panel-title'>Sale price distribution</div><div class='panel-sub'>How transaction prices are spread across the dataset</div>", unsafe_allow_html=True)
        fig = px.histogram(df, x="price", nbins=55, color_discrete_sequence=["#28715d"])
        fig.update_layout(height=310, margin=dict(l=5,r=5,t=5,b=5), paper_bgcolor="white",plot_bgcolor="white",
                          xaxis_title="Sale price (USD)",yaxis_title="Number of homes",showlegend=False,
                          font=dict(family="DM Sans",color="#52675e",size=10))
        fig.update_xaxes(showgrid=False,tickprefix="$",tickformat="~s")
        fig.update_yaxes(gridcolor="#edf1ed")
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'><div class='panel-title'>Median price by construction grade</div><div class='panel-sub'>Relationship between build grade and median sale price</div>", unsafe_allow_html=True)
        grade_data = df.groupby("grade",as_index=False)["price"].median()
        fig2 = px.bar(grade_data,x="grade",y="price",color_discrete_sequence=["#c29a62"])
        fig2.update_layout(height=310,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="white",plot_bgcolor="white",
                           xaxis_title="Construction grade",yaxis_title="Median price (USD)",
                           font=dict(family="DM Sans",color="#52675e",size=10))
        fig2.update_xaxes(showgrid=False)
        fig2.update_yaxes(gridcolor="#edf1ed",tickprefix="$",tickformat="~s")
        st.plotly_chart(fig2,use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("<div class='panel'><div class='panel-title'>Living area and sale price</div><div class='panel-sub'>Sample of 2,000 transactions</div>",unsafe_allow_html=True)
        sample = df.sample(min(2000,len(df)),random_state=42)
        fig3 = px.scatter(sample,x="sqft_living",y="price",color="grade",
                          color_continuous_scale=["#d9e9df","#28715d","#c29a62"],opacity=.55)
        fig3.update_layout(height=300,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="white",plot_bgcolor="white",
                           xaxis_title="Living area (sq ft)",yaxis_title="Sale price (USD)",
                           font=dict(family="DM Sans",color="#52675e",size=10),coloraxis_colorbar=dict(title="Grade"))
        fig3.update_yaxes(tickprefix="$",tickformat="~s",gridcolor="#edf1ed")
        fig3.update_xaxes(gridcolor="#edf1ed")
        st.plotly_chart(fig3,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='panel'><div class='panel-title'>Where the homes are located</div><div class='panel-sub'>Geographic distribution of sampled King County properties</div>",unsafe_allow_html=True)
        # Use a standard Plotly scatter chart instead of scatter_mapbox.
        # This avoids Plotly-version / Mapbox compatibility errors on Streamlit Cloud.
        map_sample = df[["lat","long","price"]].dropna()
        map_sample = map_sample.sample(min(1500,len(map_sample)),random_state=7) if len(map_sample) else map_sample
        fig4 = px.scatter(map_sample,x="long",y="lat",color="price",
                          color_continuous_scale=["#dcebe3","#28715d","#c29a62"],opacity=.65,
                          labels={"long":"Longitude","lat":"Latitude","price":"Sale price (USD)"},
                          hover_data={"price":":$,.0f","lat":":.4f","long":":.4f"})
        fig4.update_layout(height=300,margin=dict(l=8,r=8,t=8,b=8),paper_bgcolor="white",plot_bgcolor="white",
                           coloraxis_colorbar=dict(title="Price",tickprefix="$"),
                           font=dict(family="DM Sans",color="#52675e",size=10),
                           xaxis_title="Longitude",yaxis_title="Latitude")
        fig4.update_xaxes(gridcolor="#edf1ed")
        fig4.update_yaxes(gridcolor="#edf1ed",scaleanchor="x",scaleratio=1)
        st.plotly_chart(fig4,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)

    st.info("Dataset context: King County, Washington house sales from May 2014 to May 2015. All prices are in US dollars; this historical dataset is not a current Indian property valuation source.")

# =========================================================
# 8. PRICE PREDICTION PAGE
# =========================================================
elif page == "Predict a Price":
    st.markdown("<div class='page-kicker'>AI PROPERTY VALUATION</div><div class='page-title'>Estimate your property's value</div><div class='page-sub'>Random Forest is the primary model because it achieved stronger test-set results. Linear Regression is shown as a benchmark.</div>",unsafe_allow_html=True)

    with st.form("property_form"):
        st.markdown("**01 / Property essentials**")
        a,b,c,d = st.columns(4)
        with a: bedrooms=st.number_input("Bedrooms",0,15,3,1)
        with b: bathrooms=st.number_input("Bathrooms",0.0,8.0,2.25,.25)
        with c: sqft_living=st.number_input("Living area (sq ft)",290,13540,1910,50)
        with d: sqft_lot=st.number_input("Lot area (sq ft)",520,1651359,7600,100)

        a,b,c,d = st.columns(4)
        with a: floors=st.number_input("Floors",1.0,3.5,1.5,.5)
        with b: waterfront=st.selectbox("Waterfront", [0,1],format_func=lambda x:"Yes" if x else "No")
        with c: view=st.number_input("View rating (0–4)",0,4,0,1)
        with d: condition=st.number_input("Condition (1–5)",1,5,3,1)

        st.markdown("---")
        st.markdown("**02 / Construction and condition**")
        a,b,c,d=st.columns(4)
        with a: grade=st.number_input("Construction grade (1–13)",1,13,7,1)
        with b: sqft_above=st.number_input("Area above ground",290,9410,1560,50)
        with c: sqft_basement=st.number_input("Basement area",0,4820,0,50)
        with d: yr_built=st.number_input("Year built",1900,2015,1975,1)

        a,b,c,d=st.columns(4)
        with a: yr_renovated=st.number_input("Year renovated (0 = never)",0,2015,0,1)
        with b: sqft_living15=st.number_input("Nearby avg. living area",399,6210,1840,50)
        with c: sqft_lot15=st.number_input("Nearby avg. lot area",651,871200,7620,100)
        with d: zipcode=st.number_input("ZIP code",98001,98199,98065,1)

        st.markdown("---")
        st.markdown("**03 / Location and sale period**")
        a,b,c,d=st.columns(4)
        with a: lat=st.number_input("Latitude",47.1559,47.7776,47.5718,format="%.4f")
        with b: long=st.number_input("Longitude",-122.519,-121.315,-122.230,format="%.4f")
        with c: sale_year=st.number_input("Sale year",2014,2015,2015,1)
        with d: sale_month=st.number_input("Sale month",1,12,5,1)

        st.markdown("---")
        submitted=st.form_submit_button("✦  Generate property valuation",use_container_width=True)

    if submitted:
        was_renovated=1 if yr_renovated>0 else 0
        house_age=sale_year-yr_built
        years_since_renovation=sale_year-yr_renovated if yr_renovated>0 else 0
        values={
            "bedrooms":bedrooms,"bathrooms":bathrooms,"sqft_living":sqft_living,"sqft_lot":sqft_lot,
            "floors":floors,"waterfront":waterfront,"view":view,"condition":condition,"grade":grade,
            "sqft_above":sqft_above,"sqft_basement":sqft_basement,"yr_built":yr_built,
            "yr_renovated":yr_renovated,"zipcode":zipcode,"lat":lat,"long":long,
            "sqft_living15":sqft_living15,"sqft_lot15":sqft_lot15,"sale_year":sale_year,
            "sale_month":sale_month,"house_age":house_age,"was_renovated":was_renovated,
            "years_since_renovation":years_since_renovation
        }
        input_df=pd.DataFrame([values]).reindex(columns=feature_columns)
        for column in preprocessing["numerical_columns"]:
            if column in input_df.columns:
                input_df[column]=input_df[column].fillna(preprocessing["numerical_medians"][column])

        lr_price=float(linear_model.predict(input_df)[0])
        rf_price=float(random_forest_model.predict(input_df)[0])
        chosen_price=rf_price

        st.markdown("<div class='page-kicker'>VALUATION REPORT</div><div class='page-title'>Your prediction results</div>",unsafe_allow_html=True)

        # Primary result: Random Forest performed better on the held-out test set.
        st.markdown(f"""
        <div class="result-hero" style="border:2px solid #b9d8c5;box-shadow:0 8px 24px rgba(23,77,64,.08);">
          <div class="result-label">★ PRIMARY MODEL · RANDOM FOREST REGRESSION</div>
          <div class="result-price">${rf_price:,.0f}</div>
          <div class="result-caption">Main estimated sale price · Test R² 0.8533 · MAE $72,677.67</div>
        </div>
        """,unsafe_allow_html=True)

        st.markdown("**Secondary model comparison**")
        left, right = st.columns(2)
        with left:
            st.metric("Linear Regression · Benchmark", f"${lr_price:,.0f}", help="Comparison estimate from the Linear Regression model.")
        with right:
            st.metric("Difference between estimates", f"${abs(rf_price-lr_price):,.0f}", help="Absolute difference between model outputs; not a confidence interval.")
        st.caption("Random Forest is highlighted as the primary estimate because it performed better on the notebook's test set. Linear Regression remains visible as a comparison model.")

        compare=pd.DataFrame({"Model":["Random Forest · Primary","Linear Regression · Benchmark"],"Predicted price":[rf_price,lr_price]})
        fig=px.bar(compare,x="Model",y="Predicted price",color="Model",
                   color_discrete_map={"Random Forest · Primary":"#28715d","Linear Regression · Benchmark":"#c29a62"},text_auto="$.3s")
        fig.update_layout(height=300,showlegend=False,margin=dict(l=5,r=5,t=20,b=5),
                          paper_bgcolor="white",plot_bgcolor="white",
                          yaxis_title="Predicted price (USD)",xaxis_title="",
                          font=dict(family="DM Sans",color="#52675e",size=11))
        fig.update_yaxes(gridcolor="#edf1ed",tickprefix="$",tickformat="~s")
        st.plotly_chart(fig,use_container_width=True)
        st.info("These estimates are based on historical King County sales data (May 2014–May 2015). They are in USD and should not be interpreted as current market prices or Indian property valuations.")

# =========================================================
# 9. MARKET EXPLORER PAGE
# =========================================================
elif page == "Market Explorer":
    st.markdown("<div class='page-kicker'>EXPLORE THE DATA</div><div class='page-title'>Discover King County housing patterns</div><div class='page-sub'>Filter the dataset and explore how property characteristics relate to sale prices.</div>",unsafe_allow_html=True)
    low,high=int(df["price"].quantile(.01)),int(df["price"].quantile(.99))
    price_range=st.slider("Filter sale price range (USD)",min_value=low,max_value=high,value=(low,high),step=25000)
    filtered=df[df["price"].between(price_range[0],price_range[1])]
    st.caption(f"Showing {len(filtered):,} of {len(df):,} transactions")
    x,y=st.columns(2)
    with x:
        grade_filter=st.multiselect("Construction grade",sorted(filtered["grade"].dropna().unique()),default=[])
    with y:
        bedroom_filter=st.multiselect("Bedrooms",sorted(filtered["bedrooms"].dropna().unique()),default=[])
    if grade_filter:
        filtered=filtered[filtered["grade"].isin(grade_filter)]
    if bedroom_filter:
        filtered=filtered[filtered["bedrooms"].isin(bedroom_filter)]
    left,right=st.columns(2)
    with left:
        st.markdown("<div class='panel'><div class='panel-title'>Price by bedrooms</div><div class='panel-sub'>Median transaction price for each bedroom count</div>",unsafe_allow_html=True)
        data=filtered.groupby("bedrooms",as_index=False)["price"].median()
        f=px.bar(data,x="bedrooms",y="price",color_discrete_sequence=["#28715d"])
        f.update_layout(height=320,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="white",plot_bgcolor="white",xaxis_title="Bedrooms",yaxis_title="Median price",font=dict(family="DM Sans",size=10,color="#52675e"))
        f.update_yaxes(tickprefix="$",tickformat="~s",gridcolor="#edf1ed")
        st.plotly_chart(f,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with right:
        st.markdown("<div class='panel'><div class='panel-title'>Waterfront and non-waterfront homes</div><div class='panel-sub'>Sale price distribution by waterfront status</div>",unsafe_allow_html=True)
        box=filtered.copy()
        box["Waterfront"]=box["waterfront"].map({0:"No waterfront",1:"Waterfront"})
        f2=px.box(box,x="Waterfront",y="price",color="Waterfront",color_discrete_map={"No waterfront":"#28715d","Waterfront":"#c29a62"})
        f2.update_layout(height=320,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="white",plot_bgcolor="white",showlegend=False,xaxis_title="",yaxis_title="Sale price (USD)",font=dict(family="DM Sans",size=10,color="#52675e"))
        f2.update_yaxes(tickprefix="$",tickformat="~s",gridcolor="#edf1ed")
        st.plotly_chart(f2,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("**Filtered dataset preview**")
    st.dataframe(filtered[["price","bedrooms","bathrooms","sqft_living","grade","condition","zipcode","yr_built"]].head(15),use_container_width=True,hide_index=True)

# =========================================================
# 10. MODEL INSIGHTS PAGE
# =========================================================
elif page == "Model Insights":
    st.markdown("<div class='page-kicker'>MODEL EXPLAINABILITY</div><div class='page-title'>Understand what influences price</div><div class='page-sub'>Explore the features used by the Random Forest model and how the two algorithms differ.</div>",unsafe_allow_html=True)
    st.markdown("<div class='panel'><div class='panel-title'>Random Forest feature importance</div><div class='panel-sub'>Relative contribution of input features in the trained Random Forest model; importance is not causation.</div>",unsafe_allow_html=True)
    if hasattr(random_forest_model,"feature_importances_"):
        importance=pd.DataFrame({"Feature":feature_columns,"Importance":random_forest_model.feature_importances_})
        importance=importance.sort_values("Importance",ascending=True).tail(15)
        fig=px.bar(importance,x="Importance",y="Feature",orientation="h",color_discrete_sequence=["#28715d"])
        fig.update_layout(height=500,margin=dict(l=5,r=5,t=5,b=5),paper_bgcolor="white",plot_bgcolor="white",
                          xaxis_title="Relative importance",yaxis_title="",font=dict(family="DM Sans",size=11,color="#52675e"))
        fig.update_xaxes(gridcolor="#edf1ed")
        st.plotly_chart(fig,use_container_width=True)
    else:
        st.warning("Feature importance is not available for the loaded model.")
    st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.markdown("<div class='panel'><div class='panel-title'>Linear Regression</div><div class='panel-sub'>A linear model that estimates price using a weighted combination of features.</div><ul><li>Simple and interpretable baseline</li><li>Models linear relationships</li><li>Useful for comparison</li></ul></div>",unsafe_allow_html=True)
    with b:
        st.markdown("<div class='panel'><div class='panel-title'>Random Forest Regression</div><div class='panel-sub'>An ensemble of decision trees that can capture more complex patterns.</div><ul><li>Captures nonlinear patterns</li><li>Combines predictions from multiple trees</li><li>Provides feature importance</li></ul></div>",unsafe_allow_html=True)
    st.markdown("### Test-set performance comparison")
    st.caption("Metrics below are from the executed notebook evaluation. Lower MAE/RMSE is better; higher R² is better.")
    performance = pd.DataFrame({
        "Model": ["Random Forest · Primary", "Linear Regression · Benchmark"],
        "MAE (USD)": [72677.67, 126638.33],
        "RMSE (USD)": [148917.42, 211490.21],
        "Test R²": [0.8533, 0.7041]
    })
    st.dataframe(performance, use_container_width=True, hide_index=True)
    st.success("Random Forest is selected as the primary model because it has lower test MAE and RMSE and a higher test R² in this evaluation.")
    st.caption("Random Forest train R² is 0.9834 versus test R² 0.8533, so some overfitting may be present. Test-set performance is used for this comparison.")

# =========================================================
# 11. FOOTER
# =========================================================
st.markdown("<div class='footer'>ESTATEIQ &nbsp; · &nbsp; HOUSE PRICE PREDICTION &nbsp; · &nbsp; LINEAR REGRESSION + RANDOM FOREST</div>",unsafe_allow_html=True)
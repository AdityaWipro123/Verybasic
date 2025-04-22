import streamlit as st
import numpy as np
import pandas as pd
import joblib

# === Load the trained model ===
model = joblib.load("./VeryBasic.pkl")

# === Define encoding mappings ===

bearing_map = {'N': 0, 'Y': 1}


# === Define input headers (must match training model) ===
input_headers = [
    "Pressure", "Bore", "Rod diameter", "Stroke","BearingY-N"
]

st.set_page_config(page_title="Hydraulic Cost Estimator", layout="centered")
st.title("🔩 Hydraulic Cylinder Cost Estimator")

st.markdown("### Enter parameters below to predict the cost:")

# === Slider + Manual Input Function ===
def slider_with_input(label, min_val, max_val, step, default):
    col1, col2 = st.columns([3, 1])
    with col1:
        slider_val = st.slider(label, min_value=min_val, max_value=max_val, step=step, value=default, key=label+"_slider")
    with col2:
        box_val = st.number_input("Enter manually", min_value=min_val, max_value=max_val, step=step, value=slider_val, key=label+"_input")
    return box_val

# === Numeric Inputs ===
pressure = slider_with_input("Pressure", 100, 500, 10, 250)
bore = slider_with_input("Bore", 10, 500, 1, 100)
rod_dia = slider_with_input("Rod diameter", 10, 500, 1, 75)
stroke = slider_with_input("Stroke", 100, 5000, 1, 750)


#----
bearing = st.selectbox("BearingY-N", options=list(bearing_map.keys()))


# === Predict ===
if st.button("Predict Cost 💰"):
    # Prepare the input in the correct order and format
    input_data = pd.DataFrame([[
        pressure, bore, rod_dia, stroke,bearing_map[bearing]
    ]], columns=input_headers)

    # Predict
    predicted_cost = model.predict(input_data)[0]

    # Show result
    st.success(f"🧾 Estimated Cost: ₹ {predicted_cost:,.2f}")

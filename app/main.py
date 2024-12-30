import streamlit as st
import folium
from streamlit_folium import st_folium
import xgboost as xgb
import pickle
import os
import numpy as np

from utils import (
    determine_borough,
    determine_victim_age,
    determine_victim_race,
    determine_victim_gender,
    get_offense_description
)

st.set_page_config(page_title="NYC Crime Prediction", layout="wide")

def load_model():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xgboost_model.pkl")
    with open(model_path, 'rb') as f:
        return pickle.load(f)

xgb_model = load_model()

st.title("NYC Crime Prediction ")

col1, col2 = st.columns([3, 2]) 


with col1:

    if "clicked_location" not in st.session_state:
        st.session_state.clicked_location = [40.7128, -74.0060]  # NYC center
    
    m = folium.Map(location=st.session_state.clicked_location, zoom_start=12)
    folium.Marker(
        location=st.session_state.clicked_location,
        popup="Selected Location",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    st.write("**Click on the map to select a location**")
    
    map_data = st_folium(m, width=700, height=500, key="map")  

    if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.session_state.clicked_location = [lat, lon]

        m = folium.Map(location=st.session_state.clicked_location, zoom_start=12)
        folium.Marker(
            location=st.session_state.clicked_location,
            popup="Selected Location",
            icon=folium.Icon(color="red"),
        ).add_to(m)
        
        st_folium(m, width=700, height=500, key="updated_map")

    st.write(f"**Latitude:** {st.session_state.clicked_location[0]}")
    st.write(f"**Longitude:** {st.session_state.clicked_location[1]}")


with col2:
    st.subheader("Select Additional Details")

    location_type = st.radio(
        "Location Type:",
        ["None", "In PSA Housing", "In Transport", "In Park"],
        index=0
    )
    in_psa_housing = 1 if location_type == "In PSA Housing" else 0
    in_transport = 1 if location_type == "In Transport" else 0
    in_park = 1 if location_type == "In Park" else 0

    selected_date = st.date_input("Select Date")
    hour = st.selectbox("Select Hour (0-23)", list(range(24)), index=12)

    age = st.number_input("Age (0 = 'Undesired to Tell')", min_value=0, max_value=120, step=1, value=0)

    race_options = [
        'Undesired to Tell',
        'AMERICAN INDIAN/ALASKAN NATIVE',
        'ASIAN / PACIFIC ISLANDER',
        'BLACK',
        'BLACK HISPANIC',
        'WHITE',
        'WHITE HISPANIC'
    ]
    race_selected = st.selectbox("Race", options=race_options, index=0)

    gender_selected = st.selectbox("Gender", ['UNDEFINED', 'F', 'M'], index=0)

    year, month, day = selected_date.year, selected_date.month, selected_date.day
    borough, borough_code = determine_borough(
        st.session_state.clicked_location[0],
        st.session_state.clicked_location[1]
    )

    age_category, age_code = determine_victim_age(None if age == 0 else age)
    race_categ, race_code = determine_victim_race(
        race_selected if race_selected != 'Undesired to Tell' else 'UNKNOWN'
    )
    final_gender, gender_code = determine_victim_gender(
        'U' if gender_selected == 'UNDEFINED' else gender_selected
    )

    day_of_week = selected_date.weekday()  
    is_weekend = 1 if day_of_week in [5, 6] else 0

    input_data = [
        st.session_state.clicked_location[0],
        st.session_state.clicked_location[1],
        borough_code,
        age_code,
        race_code,
        gender_code,
        year,
        month,
        day,
        hour,
        day_of_week,
        is_weekend,
        in_psa_housing,
        in_transport,
        in_park
    ]
    input_array = np.array(input_data).reshape(1, -1)

    if st.button("Predict"):
        prediction = xgb_model.predict(input_array)
        offense_code = prediction[0]
        offense_type = get_offense_description(offense_code)
        st.success(f"You have a high likelihood of becoming a victim of {offense_type} Crime.")

import streamlit as st
import folium
from streamlit_folium import st_folium

from utils import (
    determine_borough,
    determine_victim_age,
    determine_victim_race,
    determine_victim_gender
)

st.title("NYC Crime Prediction")

nyc_coordinates = [40.7128, -74.0060]

if "clicked_location" not in st.session_state:
    st.session_state.clicked_location = nyc_coordinates  

m = folium.Map(location=st.session_state.clicked_location, zoom_start=12)

folium.Marker(
    location=st.session_state.clicked_location,
    popup="Selected Location",
    icon=folium.Icon(color="red"),
).add_to(m)

st.write("Click on the map to pin a Desired Location")
map_data = st_folium(m, width=700, height=500, key="map")

if map_data is not None and "last_clicked" in map_data and map_data["last_clicked"] is not None:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.session_state.clicked_location = [lat, lon]

    m = folium.Map(location=st.session_state.clicked_location, zoom_start=12)
    folium.Marker(
        location=st.session_state.clicked_location,
        popup="Selected Location",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    map_data = st_folium(m, width=700, height=500, key="updated_map")

st.write(f"Latitude: {st.session_state.clicked_location[0]}")
st.write(f"Longitude: {st.session_state.clicked_location[1]}")

# Inputs
location_type = st.radio(
    "Select the location type:",
    options=["None", "In PSA Housing", "In Transport", "In Park"],
    index=0
)

# Convert Selection to Values
in_psa_housing = 1 if location_type == "In PSA Housing" else 0
in_transport = 1 if location_type == "In Transport" else 0
in_park = 1 if location_type == "In Park" else 0 

selected_date = st.date_input("Select a date")
year, month, day = selected_date.year, selected_date.month, selected_date.day
hour = st.selectbox("Select Hour", options=list(range(0, 24)), index=12)
minute = st.selectbox("Select Minute", options=list(range(0, 60)), index=0)

age = st.number_input("Enter your age (default: Undesired to Tell)", min_value=0, max_value=120, step=1, value=0)

race_options = [
    'Undesired to Tell',
    'AMERICAN INDIAN/ALASKAN NATIVE',
    'ASIAN / PACIFIC ISLANDER',
    'BLACK',
    'BLACK HISPANIC',
    'WHITE',
    'WHITE HISPANIC'
]

race = st.selectbox("Select Victim Race", options=race_options, index=0)

gender = st.selectbox("Select Victim Gender", options=['UNDEFINED', 'F', 'M'], index=0)

borough, borough_code = determine_borough(
    st.session_state.clicked_location[0], 
    st.session_state.clicked_location[1]
)

age_category, age_code = determine_victim_age(None if age == 0 else age)

race_categ, race_code = determine_victim_race(race if race != 'Undesired to Tell' else 'UNKNOWN')

gender, gender_code = determine_victim_gender('U' if gender == 'UNDEFINED' else gender)

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

st.write(input_data)

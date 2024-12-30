import geopandas as gpd
from shapely.geometry import Point

def determine_borough(lat, lon):
    gdf = gpd.read_file("boundries.geojson")
    point = Point(lon, lat)
    selected = gdf[gdf.geometry.contains(point)]

    borough_mapping = {
        'Bronx': 0,
        'Brooklyn': 1,
        'Manhattan': 2,
        'Queens': 3,
        'Staten Island': 4,
        'UNKNOWN': 5
    }

    if not selected.empty:
        borough_name = selected.iloc[0]['boro_name']  
        borough_code = borough_mapping.get(borough_name)
        return borough_name, borough_code
    else:
        return "UNKNOWN", borough_mapping['UNKNOWN']
    

def determine_victim_age(age):
    if age is None:
        return "UNKNOWN", 5
    elif 18 <= age <= 24:
        return "18-24", 0
    elif 25 <= age <= 44:
        return "25-44", 1
    elif 45 <= age <= 64:
        return "45-64", 2
    elif age >= 65:
        return "65+", 3
    elif age < 18:
        return "<18", 4
    return "UNKNOWN", 5


def determine_victim_race(race):
    race_mapping = {
        'AMERICAN INDIAN/ALASKAN NATIVE': 0,
        'ASIAN / PACIFIC ISLANDER': 1,
        'BLACK': 2,
        'BLACK HISPANIC': 3,
        'UNKNOWN': 4,
        'WHITE': 5,
        'WHITE HISPANIC': 6
    }
    mapping_code = race_mapping.get(race, race_mapping['UNKNOWN'])
    return race, mapping_code  


def determine_victim_gender(gender):
    gender_mapping = {
        'F': 0,
        'M': 1,
        'U': 2
    }
    mapping_code = gender_mapping.get(gender, gender_mapping['U'])
    return gender, mapping_code  

def get_offense_description(code: int) -> str:
    mapping = {
        0: "ADMINISTRATIVE_RELATED",
        1: "DRUGS/ALCOHOL_RELATED",
        2: "PERSONAL_RELATED",
        3: "PROPERTY_RELATED",
        4: "SEXUAL_RELATED"
    }
    
    return mapping.get(code, "UNKNOWN_OFFENSE")


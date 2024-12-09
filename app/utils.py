def determine_borough(lat, lon):
    borough_boundaries = {
        'BROOKLYN': {'lat_min': 40.5700, 'lat_max': 40.7400, 'lon_min': -74.0400, 'lon_max': -73.8500},
        'MANHATTAN': {'lat_min': 40.7000, 'lat_max': 40.8800, 'lon_min': -74.0200, 'lon_max': -73.9100},
        'BRONX': {'lat_min': 40.7900, 'lat_max': 40.9200, 'lon_min': -73.9300, 'lon_max': -73.7900},
        'QUEENS': {'lat_min': 40.5500, 'lat_max': 40.8000, 'lon_min': -73.9600, 'lon_max': -73.7200},
        'STATEN ISLAND': {'lat_min': 40.5000, 'lat_max': 40.6500, 'lon_min': -74.2500, 'lon_max': -74.0500}
    }
    
    borough_mapping = {
        'BRONX': 0,
        'BROOKLYN': 1,
        'MANHATTAN': 2,
        'QUEENS': 3,
        'STATEN ISLAND': 4,
        'UNKNOWN': 5
    }
    
    for borough, bounds in borough_boundaries.items():
        if (bounds['lat_min'] <= lat <= bounds['lat_max']) and (bounds['lon_min'] <= lon <= bounds['lon_max']):
            return borough, borough_mapping[borough]
    
    # If no match, return UNKNOWN
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
    return race, mapping_code  # Return both race and its code


def determine_victim_gender(gender):
    gender_mapping = {
        'F': 0,
        'M': 1,
        'U': 2
    }
    mapping_code = gender_mapping.get(gender, gender_mapping['U'])
    return gender, mapping_code  # Return both the gender and its code


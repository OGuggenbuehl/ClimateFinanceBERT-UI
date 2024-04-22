import requests

# URL to the GeoJSON file

GEOJSON_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
GEOJSON_BASE = requests.get(GEOJSON_URL).json()

# Initial map center and zoom level
INITIAL_CENTER = [51.4934, 0.0098]
INITIAL_ZOOM = 2
COUNTRY_IDS = [feature["id"] for feature in GEOJSON_BASE["features"]]

if __name__ == "__main__":
    print(f"There are {len(COUNTRY_IDS)} countries in the list:")
    print(COUNTRY_IDS)

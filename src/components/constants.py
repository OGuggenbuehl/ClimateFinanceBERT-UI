import pandas as pd
import requests

# URL to the GeoJSON file
GEOJSON_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
)
GEOJSON_BASE = requests.get(GEOJSON_URL).json()

# ClimateFinance-DataFrame for prod
RAW_SOURCE = "./data/all_crs_labelled.csv"
PARQUET_SOURCE = "./data/ClimFinBERT_DB.parquet"
DUCKDB_PATH = "./data/ClimFinBERT_DB.duckdb"

# # small files for dev
# RAW_SOURCE = "./data/sampled_df.csv"
# PARQUET_SOURCE = "./data/sampled_df.parquet"
# DUCKDB_PATH = "./data/db_small.duckdb"

COLUMN_TYPES = {
    "Year": "INTEGER",
    "DEDonorcode": "VARCHAR",
    "DonorName": "VARCHAR",
    "DERecipientcode": "VARCHAR",
    "RecipientName": "VARCHAR",
    "FlowCode": "BIGINT",
    "FlowName": "VARCHAR",
    "USD_Commitment": "DOUBLE",
    "USD_Disbursement": "DOUBLE",
    "USD_Received": "DOUBLE",
    "USD_Commitment_Defl": "DOUBLE",
    "USD_Disbursement_Defl": "DOUBLE",
    "USD_Received_Defl": "DOUBLE",
    "Biodiversity": "DOUBLE",
    "ClimateMitigation": "DOUBLE",
    "ClimateAdaptation": "DOUBLE",
    "Desertification": "DOUBLE",
    "climate_relevance": "DOUBLE",
    "climate_class_number": "DOUBLE",
    "climate_class": "VARCHAR",
    "meta_category": "VARCHAR",
    "labelled_bilateral": "BIGINT",
    "DonorType": "VARCHAR",
}

# Initial map center and zoom level
INITIAL_CENTER = [51.4934, 0.0098]
INITIAL_ZOOM = 2
COUNTRY_IDS = [feature["id"] for feature in GEOJSON_BASE["features"]]

CATEGORIES_DF = pd.DataFrame(
    {
        "climate_class": [
            "Adaptation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Mitigation",
            "Environment",
            "Environment",
            "Environment",
            "Environment",
        ],
        "meta_category": [
            "Adaptation",
            "Solar-energy",
            "Other-mitigation-projects",
            "Renewables-multiple",
            "Hydro-energy",
            "Wind-energy",
            "Bioenergy",
            "Geothermal-energy",
            "Energy-efficiency",
            "Marine-energy",
            "Biodiversity",
            "Nature_conservation",
            "Other-environment-projects",
            "Sustainable-land-use",
        ],
    }
)

CATEGORIES = [
    "Adaptation",
    "Mitigation",
    "Environment",
]

SUBCATEGORIES = [
    "Adaptation",
    "Solar-energy",
    "Other-mitigation-projects",
    "Biodiversity",
    "Nature_conservation",
    "Other-environment-projects",
    "Sustainable-land-use",
    "Renewables-multiple",
    "Hydro-energy",
    "Wind-energy",
    "Bioenergy",
    "Geothermal-energy",
    "Energy-efficiency",
    "Marine-energy",
]
FLOW_TYPES = [
    "ODA Grants",
    "ODA Loans",
    "Other Official Flows (non Export Credit)",
    "Private Development Finance",
    "Equity Investment",
]

if __name__ == "__main__":
    print(f"There are {len(COUNTRY_IDS)} countries in the list:")
    print(COUNTRY_IDS)

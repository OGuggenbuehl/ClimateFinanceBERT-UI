"""
Constants for the ClimateFinanceBERT-UI application.

This module contains various configuration constants organized by category:
- Data sources and paths
- Database schema definitions
- Visualization settings
- Category definitions for climate finance
"""

from typing import Any, Dict, Optional

import pandas as pd

# ====================================
# Data Sources Configuration
# ====================================


class DataSources:
    """Data source paths for different environments"""

    class Production:
        """Production data sources"""

        RAW_SOURCE = "./data/all_crs_labelled.csv"
        PARQUET_SOURCE = "./data/ClimFinBERT_DB.parquet"
        DUCKDB_PATH = "./data/ClimFinBERT_DB.duckdb"

    class Development:
        """Development data sources (smaller files)"""

        RAW_SOURCE = "./data/sampled_df.csv"
        PARQUET_SOURCE = "./data/sampled_df.parquet"
        DUCKDB_PATH = "./data/db_small.duckdb"


# Use development sources by default
# To use production sources, import and modify:
# from src.components.constants import DataSources
# RAW_SOURCE = DataSources.Production.RAW_SOURCE
RAW_SOURCE = DataSources.Development.RAW_SOURCE
PARQUET_SOURCE = DataSources.Development.PARQUET_SOURCE
DUCKDB_PATH = DataSources.Development.DUCKDB_PATH

# ====================================
# GeoJSON Configuration
# ====================================

# Local GeoJSON file path (transformed from Natural Earth 1:50m)
# Source: Natural Earth 1:50m Cultural Vectors - Admin 0 Countries
# Public domain data from naturalearthdata.com
# Using 50m (medium resolution) to include small island nations important for climate finance
GEOJSON_LOCAL_PATH = "./data/countries.geo.json"

# Cache for the GeoJSON data
_geojson_cache: Optional[Dict[str, Any]] = None


def get_geojson_base() -> Dict[str, Any]:
    """Lazily load and cache the GeoJSON data from local file.

    Loads transformed Natural Earth 1:50m data with standardized ISO A3 codes.
    The local file must be present before starting the application.

    Returns:
        Dictionary containing GeoJSON data with country geometries

    Raises:
        FileNotFoundError: If the local GeoJSON file is not found
        RuntimeError: If GeoJSON data cannot be parsed
    """
    global _geojson_cache

    if _geojson_cache is None:
        import json
        import logging
        import os

        logger = logging.getLogger(__name__)

        if not os.path.exists(GEOJSON_LOCAL_PATH):
            msg = (
                f"GeoJSON file not found at {GEOJSON_LOCAL_PATH}. "
                f"Ensure the file exists before starting the application."
            )
            logger.error(msg)
            raise FileNotFoundError(msg)

        try:
            logger.info(f"Loading GeoJSON data from local file: {GEOJSON_LOCAL_PATH}")
            with open(GEOJSON_LOCAL_PATH, "r", encoding="utf-8") as f:
                _geojson_cache = json.load(f)
            logger.info(
                f"GeoJSON data successfully loaded from local file: "
                f"{len(_geojson_cache.get('features', []))} countries"
            )
        except (IOError, ValueError) as e:
            msg = f"Failed to load or parse GeoJSON file at {GEOJSON_LOCAL_PATH}: {e}"
            logger.error(msg)
            raise RuntimeError(msg) from e

    return _geojson_cache


# ====================================
# Database Schema Configuration
# ====================================


class ColumnType:
    """SQL column types for DuckDB"""

    INTEGER = "INTEGER"
    VARCHAR = "VARCHAR"
    BIGINT = "BIGINT"
    DOUBLE = "DOUBLE"


class SchemaDefinition:
    """Database schema definitions"""

    COLUMN_TYPES = {
        # Entity identifiers
        "Year": ColumnType.INTEGER,
        "DEDonorcode": ColumnType.VARCHAR,
        "DonorName": ColumnType.VARCHAR,
        "DERecipientcode": ColumnType.VARCHAR,
        "RecipientName": ColumnType.VARCHAR,
        # Flow information
        "FlowCode": ColumnType.BIGINT,
        "FlowName": ColumnType.VARCHAR,
        # Financial metrics (nominal values)
        "USD_Commitment": ColumnType.DOUBLE,
        "USD_Disbursement": ColumnType.DOUBLE,
        "USD_Received": ColumnType.DOUBLE,
        # Financial metrics (deflated values)
        "USD_Commitment_Defl": ColumnType.DOUBLE,
        "USD_Disbursement_Defl": ColumnType.DOUBLE,
        "USD_Received_Defl": ColumnType.DOUBLE,
        # Environmental markers
        "Biodiversity": ColumnType.DOUBLE,
        "ClimateMitigation": ColumnType.DOUBLE,
        "ClimateAdaptation": ColumnType.DOUBLE,
        "Desertification": ColumnType.DOUBLE,
        # Climate classification
        "climate_relevance": ColumnType.DOUBLE,
        "climate_class_number": ColumnType.DOUBLE,
        "climate_class": ColumnType.VARCHAR,
        "meta_category": ColumnType.VARCHAR,
        # Other attributes
        "labelled_bilateral": ColumnType.BIGINT,
        "DonorType": ColumnType.VARCHAR,
    }


# For backward compatibility
COLUMN_TYPES = SchemaDefinition.COLUMN_TYPES

# ====================================
# Map and Visualization Settings
# ====================================


class MapSettings:
    """Default settings for the map visualization"""

    # Year range for the time slider
    YEAR_RANGE = {
        "min": 2000,
        "max": 2022,
    }

    # Initial map center and zoom level
    INITIAL_CENTER = [51.4934, 0.0098]  # London coordinates
    INITIAL_ZOOM = 2

    @classmethod
    def get_country_ids(cls):
        """Get list of country IDs from GeoJSON data"""
        geojson_data = get_geojson_base()
        return [feature["id"] for feature in geojson_data["features"]]


# For backward compatibility
YEAR_RANGE = MapSettings.YEAR_RANGE
INITIAL_CENTER = MapSettings.INITIAL_CENTER
INITIAL_ZOOM = MapSettings.INITIAL_ZOOM
COUNTRY_IDS = MapSettings.get_country_ids()

# ====================================
# Climate Categories & Flow Types
# ====================================


class ClimateCategories:
    """Climate finance category definitions"""

    # Main categories
    MAIN = [
        "Adaptation",
        "Mitigation",
        "Environment",
    ]

    # Sub-categories with more specific climate finance types
    SUB = [
        # Adaptation
        "Adaptation",
        # Mitigation sub-categories
        "Solar-energy",
        "Other-mitigation-projects",
        "Renewables-multiple",
        "Hydro-energy",
        "Wind-energy",
        "Bioenergy",
        "Geothermal-energy",
        "Energy-efficiency",
        "Marine-energy",
        # Environment sub-categories
        "Biodiversity",
        "Nature_conservation",
        "Other-environment-projects",
        "Sustainable-land-use",
    ]

    # DataFrame mapping sub-categories to main categories
    MAPPING = pd.DataFrame(
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


class FlowTypes:
    """Financial flow type definitions"""

    TYPES = [
        "ODA Grants",
        "ODA Loans",
        "Other Official Flows (non Export Credit)",
        "Private Development Finance",
        "Equity Investment",
    ]


# For backward compatibility
CATEGORIES_DF = ClimateCategories.MAPPING
CATEGORIES = ClimateCategories.MAIN
SUBCATEGORIES = ClimateCategories.SUB
FLOW_TYPES = FlowTypes.TYPES


# ====================================
# Module Exports & Testing
# ====================================

if __name__ == "__main__":
    # Simple test to verify country data
    country_ids = MapSettings.get_country_ids()
    print(f"There are {len(country_ids)} countries in the list:")
    print(country_ids)

    # Print category count information
    print(f"\nMain categories ({len(ClimateCategories.MAIN)}):")
    print(ClimateCategories.MAIN)

    print(f"\nSub-categories ({len(ClimateCategories.SUB)}):")
    print(ClimateCategories.SUB)

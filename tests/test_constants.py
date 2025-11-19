"""Tests for constants module."""

import os


def test_geojson_lazy_loading():
    """Test that GeoJSON is loaded lazily and cached."""
    from components import constants

    # Clear cache
    constants._geojson_cache = None

    # First call should load data
    data1 = constants.get_geojson_base()
    assert data1 is not None
    assert "features" in data1
    assert len(data1["features"]) > 0

    # Second call should return cached data (same object)
    data2 = constants.get_geojson_base()
    assert data1 is data2


def test_geojson_fallback_file_exists():
    """Test that local fallback file exists."""
    from components.constants import GEOJSON_LOCAL_PATH

    assert os.path.exists(GEOJSON_LOCAL_PATH), (
        f"Local GeoJSON fallback not found at {GEOJSON_LOCAL_PATH}. "
        "This file is required for offline operation."
    )


def test_geojson_has_valid_structure():
    """Test that loaded GeoJSON has expected structure."""
    from components.constants import get_geojson_base

    data = get_geojson_base()
    assert data["type"] == "FeatureCollection"
    assert isinstance(data["features"], list)
    assert len(data["features"]) == 180


def test_country_ids_from_geojson():
    """Test that country IDs can be extracted from GeoJSON."""
    from components.constants import MapSettings

    country_ids = MapSettings.get_country_ids()
    assert isinstance(country_ids, list)
    assert len(country_ids) == 180
    assert all(isinstance(cid, str) for cid in country_ids)

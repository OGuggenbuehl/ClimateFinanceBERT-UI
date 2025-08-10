"""Tests for data operations module."""

import pandas as pd
import pytest

from utils.data_operations import reshape_by_type


def test_reshape_by_type_donors(sample_finance_data):
    """Test reshape_by_type function with donors."""
    # Act
    result = reshape_by_type(sample_finance_data, "donors")

    # Assert
    assert "CountryCode" in result.columns
    assert "CountryName" in result.columns
    assert "DERecipientcode" not in result.columns
    assert "RecipientName" not in result.columns
    assert result["CountryCode"].tolist() == sample_finance_data["DEDonorcode"].tolist()
    assert result["CountryName"].tolist() == sample_finance_data["DonorName"].tolist()


def test_reshape_by_type_recipients(sample_finance_data):
    """Test reshape_by_type function with recipients."""
    # Act
    result = reshape_by_type(sample_finance_data, "recipients")

    # Assert
    assert "CountryCode" in result.columns
    assert "CountryName" in result.columns
    assert "DEDonorcode" not in result.columns
    assert "DonorName" not in result.columns
    assert (
        result["CountryCode"].tolist()
        == sample_finance_data["DERecipientcode"].tolist()
    )
    assert (
        result["CountryName"].tolist() == sample_finance_data["RecipientName"].tolist()
    )


def test_reshape_by_type_invalid():
    """Test reshape_by_type function with invalid type."""
    # Arrange
    df = pd.DataFrame(
        {
            "DEDonorcode": ["USA"],
            "DonorName": ["United States"],
            "DERecipientcode": ["IND"],
            "RecipientName": ["India"],
        }
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid selected type"):
        reshape_by_type(df, "invalid_type")

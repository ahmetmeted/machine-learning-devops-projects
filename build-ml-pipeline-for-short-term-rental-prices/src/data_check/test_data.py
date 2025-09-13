import pandas as pd
import numpy as np
from scipy import stats

def test_row_count(data):
    """
    Test that the dataset has a reasonable number of rows
    """
    assert 15000 < data.shape[0] < 1000000, f"Dataset has {data.shape[0]} rows, which is not in the expected range (15000, 1000000)"

def test_price_range(data, min_price, max_price):
    """
    Test that the price range is between min_price and max_price
    """
    assert data['price'].between(min_price, max_price).all(), f"Price range is not within expected bounds ({min_price}, {max_price})"

def test_proper_boundaries(data):
    """
    Test that the data points are within proper geographical boundaries
    """
    assert data['longitude'].between(-74.25, -73.50).all(), "Longitude values are outside NYC boundaries"
    assert data['latitude'].between(40.5, 41.2).all(), "Latitude values are outside NYC boundaries"

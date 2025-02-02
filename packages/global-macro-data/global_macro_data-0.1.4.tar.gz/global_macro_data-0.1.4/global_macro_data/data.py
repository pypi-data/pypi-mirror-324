import requests
import pandas as pd
import os
import io

CSV_URL = "https://www.globalmacrodata.com/GMD.csv"

def get_data(start_year=None, end_year=None, country=None, ISO3=None):
    """
    Download global macroeconomic data with optional filtering.

    Parameters:
        start_year (int): Filter data from this starting year (inclusive).
        end_year (int): Filter data up to this ending year (inclusive).
        country (str, list, or comma-separated string): Filter data by country name(s).
        ISO3 (str or list): Filter data by ISO3 country code(s).

    Returns:
        pandas.DataFrame: Filtered dataset.
    """
    print(f"Downloading data from {CSV_URL} ...")
    response = requests.get(CSV_URL)
    
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text)) 
    else:
        raise Exception(f"Download failed, HTTP status code: {response.status_code}")
    
    # Ensure columns are correctly formatted
    df.columns = df.columns.str.strip().str.lower()
    
    # Validate input values
    valid_years = df['year'].unique()
    valid_countries = df['countryname'].unique()
    valid_iso3 = df['iso3'].unique()

    if start_year is not None and start_year not in valid_years:
        raise ValueError("Error: Please enter a valid year.")
    if end_year is not None and end_year not in valid_years:
        raise ValueError("Error: Please enter a valid year.")
    if country is not None:
        if isinstance(country, str):
            country = [c.strip() for c in country.split(",")]
        invalid_countries = [c for c in country if c not in valid_countries]
        if invalid_countries:
            raise ValueError("Error: Please enter a valid country name.")
    if ISO3 is not None:
        if isinstance(ISO3, list):
            invalid_iso3 = [code for code in ISO3 if code not in valid_iso3]
            if invalid_iso3:
                raise ValueError("Error: Please enter a valid ISO3 code.")
        elif ISO3 not in valid_iso3:
            raise ValueError("Error: Please enter a valid ISO3 code.")
    
    # Apply filtering
    if start_year is not None:
        df = df[df['year'] >= start_year]
        print(f"Filtered data for year >= {start_year}")
    if end_year is not None:
        df = df[df['year'] <= end_year]
        print(f"Filtered data for year <= {end_year}")
    if country is not None:
        df = df[df['countryname'].isin(country)]
        print(f"Filtered data for countries: {', '.join(country)}")
    if ISO3 is not None:
        if isinstance(ISO3, list):
            df = df[df['iso3'].isin(ISO3)]
        else:
            df = df[df['iso3'] == ISO3]
        print(f"Filtered data for ISO3: {ISO3}")
    
    return df

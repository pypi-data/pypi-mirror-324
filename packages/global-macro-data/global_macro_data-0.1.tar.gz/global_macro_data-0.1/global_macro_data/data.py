import requests
import pandas as pd
import os
import io

CSV_URL = "https://www.globalmacrodata.com/GMD.csv"

def get_data(cache=True, cache_dir="data/", filename=None, start_year=None, end_year=None, country=None, ISO3=None):
    """
    Download global macroeconomic data with optional caching and filtering.

    Parameters:
        cache (bool): Whether to use cached data if available. Default is True.
        cache_dir (str): Directory to store cached data. Default is "data/".
        filename (str): Custom filename for the cached file. Default is "GMD_latest.csv".
        start_year (int): Filter data from this starting year (inclusive).
        end_year (int): Filter data up to this ending year (inclusive).
        country (str or list): Filter data by country name(s).
        ISO3 (str or list): Filter data by ISO3 country code(s).

    Returns:
        pandas.DataFrame: Filtered dataset.
    """
    if cache:
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        if filename is None:
            filename = "GMD_latest.csv"
        
        file_path = os.path.join(cache_dir, filename)

        # If cache exists, load the data
        if os.path.exists(file_path):
            print(f"Using cached data: {file_path}")
            df = pd.read_csv(file_path)
        else:
            # Download the data
            print(f"Downloading data from {CSV_URL} ...")
            response = requests.get(CSV_URL)

            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text)) 
                df.to_csv(file_path, index=False)
                print(f"Data cached at: {file_path}")
            else:
                raise Exception(f"Download failed, HTTP status code: {response.status_code}")
    else:
        # Download fresh data
        print(f"Downloading fresh data from {CSV_URL} ...")
        response = requests.get(CSV_URL)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text)) 
        else:
            raise Exception(f"Download failed, HTTP status code: {response.status_code}")

    # Apply filtering
    if start_year is not None:
        df = df[df['year'] >= start_year]
    if end_year is not None:
        df = df[df['year'] <= end_year]
    if country is not None:
        if isinstance(country, list):
            df = df[df['countryname'].isin(country)]
        else:
            df = df[df['countryname'] == country]
    if ISO3 is not None:
        if isinstance(ISO3, list):
            df = df[df['ISO3'].isin(ISO3)]
        else:
            df = df[df['ISO3'] == ISO3]

    return df

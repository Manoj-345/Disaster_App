# utils.py
import pandas as pd

def load_data(path="Disasters.csv"):
    """
    Load dataset and reshape into tidy format.
    - Detects year columns (1980-2024) and melts into a single 'Year' column.
    - Ensures 'Year' is numeric for trend analysis.
    """
    df = pd.read_csv(path)

    # Detect year columns (1980-2024)
    year_cols = [c for c in df.columns if str(c).isdigit() and 1980 <= int(c) <= 2024]

    if year_cols:  # Wide format -> convert to long format
        df = df.melt(
            id_vars=[c for c in df.columns if c not in year_cols],
            value_vars=year_cols,
            var_name="Year",
            value_name="Value"
        )
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # Ensure Year column exists
    if "Year" not in df.columns:
        df["Year"] = None

    return df


def get_key_columns(df):
    """
    Detect key columns: Year, Country, Disaster, Numeric.
    Returns dictionary with standardized keys.
    """
    year_col, country_col, disaster_col = None, None, None

    for c in df.columns:
        cl = c.lower()
        if year_col is None and "year" in cl:
            year_col = c
        if country_col is None and ("country" in cl or "nation" in cl or "state" in cl):
            country_col = c
        if disaster_col is None and (
            "disaster" in cl or "type" in cl or "hazard" in cl or "indicator" in cl
        ):
            disaster_col = c

    # Detect numeric columns (exclude Year if present)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if year_col in numeric_cols:
        numeric_cols.remove(year_col)

    return {
        "year": year_col,
        "country": country_col,
        "disaster": disaster_col,
        "numeric": numeric_cols,
    }


def filter_data(df, year=None, countries=None, disasters=None,
                year_col="Year", country_col="Country", disaster_col="Disaster Type"):
    """
    Utility function to filter dataset by year, countries, or disasters.
    - year: int or list of years
    - countries: list of countries
    - disasters: list of disaster types
    """
    if year and year_col in df.columns:
        if isinstance(year, list):
            df = df[df[year_col].isin(year)]
        else:
            df = df[df[year_col] == year]

    if countries and country_col in df.columns:
        df = df[df[country_col].isin(countries)]

    if disasters and disaster_col in df.columns:
        df = df[df[disaster_col].isin(disasters)]

    return df

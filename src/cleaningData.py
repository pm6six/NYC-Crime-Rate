import pandas as pd

USECOLS = [
    "CMPLNT_NUM",
    "CMPLNT_FR_DT",
    "CMPLNT_FR_TM",
    "CMPLNT_TO_DT",
    "CMPLNT_TO_TM",
    "OFNS_DESC",
    "LAW_CAT_CD",
    "BORO_NM",
    "ADDR_PCT_CD",
    "Latitude",
    "Longitude",
]

DTYPES = {
    "CMPLNT_NUM": "string",
    "OFNS_DESC": "string",
    "LAW_CAT_CD": "category",
    "BORO_NM": "category",
    "ADDR_PCT_CD": "Int64",
}

NYC_LAT_BOUNDS = (40.45, 40.95)
NYC_LON_BOUNDS = (-74.30, -73.65)

def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """
    Load, validate, and lightly clean the NYPD complaints CSV:
    - parse dates
    - standardize offense text
    - drop rows missing precinct, borough, or coordinates (for maps)
    - clip to NYC lat/lon bounds
    - add MONTH column for optional trend analysis
    """
    df = pd.read_csv(
        csv_path,
        usecols=USECOLS,
        dtype=DTYPES,
        on_bad_lines="skip",
        low_memory=False,
    )

    # Dates
    df["CMPLNT_FR_DT"] = pd.to_datetime(df["CMPLNT_FR_DT"], errors="coerce")
    df["CMPLNT_TO_DT"] = pd.to_datetime(df["CMPLNT_TO_DT"], errors="coerce")
    df = df.dropna(subset=["CMPLNT_FR_DT"])

    # Strings (upper is used for consistent matching)
    df["OFNS_DESC"] = df["OFNS_DESC"].fillna("UNKNOWN").str.upper().str.strip()
    df["BORO_NM"] = df["BORO_NM"].astype("string").str.upper().str.strip()

    # Precinct numeric
    df = df.dropna(subset=["ADDR_PCT_CD", "BORO_NM"])
    df["ADDR_PCT_CD"] = df["ADDR_PCT_CD"].astype(int)

    # Coordinates: keep all rows for choropleth; for heatmap we’ll drop NaN later
    # Also clip to reasonable NYC bounds to avoid stray points
    if "Latitude" in df.columns and "Longitude" in df.columns:
        df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
        df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

        lat_ok = df["Latitude"].between(*NYC_LAT_BOUNDS)
        lon_ok = df["Longitude"].between(*NYC_LON_BOUNDS)

        # combine into a single mask to avoid reindex warning
        mask = (lat_ok & lon_ok) | df["Latitude"].isna() | df["Longitude"].isna()
        df = df[mask]

    # Month bucket
    df["MONTH"] = df["CMPLNT_FR_DT"].dt.to_period("M").dt.to_timestamp()

    print(f"Cleaned data: {len(df):,} rows, {df['BORO_NM'].nunique()} boroughs")
    return df

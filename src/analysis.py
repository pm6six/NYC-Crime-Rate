import pandas as pd

def summarize_by_precinct(df: pd.DataFrame) -> pd.DataFrame:
    """Total complaints per precinct (all offenses)."""
    out = (
        df.groupby("ADDR_PCT_CD")
          .size()
          .reset_index(name="crime_count")
          .sort_values("ADDR_PCT_CD")
          .reset_index(drop=True)
    )
    return out

def summarize_by_precinct_offense(df: pd.DataFrame) -> pd.DataFrame:
    """Complaints per precinct offense."""
    out = (
        df.groupby(["ADDR_PCT_CD", "OFNS_DESC"])
          .size()
          .reset_index(name="crime_count")
    )
    return out

def top_offenses(df: pd.DataFrame, n: int = 6) -> list[str]:
    """Top N offense names by overall frequency."""
    return (
        df["OFNS_DESC"]
        .value_counts()
        .head(n)
        .index
        .tolist()
    )

def monthly_borough_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Monthly crime counts per borough.

    Expects df to already have a 'MONTH' column (Timestamp at month start),
    which is already created in load_and_clean_data().

    Returns columns:
        - MONTH (Timestamp)
        - BORO_NM (str)
        - crime_count (int)
    """
    out = (
        df.groupby(["MONTH", "BORO_NM"])
          .size()
          .reset_index(name="crime_count")
          .sort_values(["MONTH", "BORO_NM"])
          .reset_index(drop=True)
    )
    return out

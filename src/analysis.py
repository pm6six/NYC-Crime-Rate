import pandas as pd

def summarize_by_precinct(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("ADDR_PCT_CD")
          .size()
          .reset_index(name="crime_count")
          .sort_values("ADDR_PCT_CD")
          .reset_index(drop=True)
    )
    return out

def summarize_by_precinct_offense(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby(["ADDR_PCT_CD", "OFNS_DESC"])
          .size()
          .reset_index(name="crime_count")
    )
    return out

def top_offenses(df: pd.DataFrame, n: int = 6) -> list[str]:
    return (
        df["OFNS_DESC"]
        .value_counts()
        .head(n)
        .index
        .tolist()
    )

def monthly_borough_series(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby(["MONTH", "BORO_NM"])
          .size()
          .reset_index(name="crime_count")
          .sort_values(["MONTH", "BORO_NM"])
          .reset_index(drop=True)
    )
    return out

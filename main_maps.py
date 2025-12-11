import os
from src.cleaningData import load_and_clean_data
from src.analysis import summarize_by_precinct, top_offenses
from src.map_visualization import create_heatmap_by_offense

# adjust file name
CURRENT_CSV = "data/NYPD_Complaint_Data_Current_(Year_To_Date)_20251029.csv"
PRECINCT_GEO = "data/Police_Precincts_20251109.geojson"

def main():
    os.makedirs("output", exist_ok=True)

    df = load_and_clean_data(CURRENT_CSV)

    by_pct = summarize_by_precinct(df)
    print(by_pct.head())

    offenses = top_offenses(df, n=6)

    create_heatmap_by_offense(
        df,
        precinct_geojson_path=PRECINCT_GEO,
        out_html="output/nyc_crime_heatmap_by_offense.html",
        offenses=offenses,
    )

if __name__ == "__main__":
    main()

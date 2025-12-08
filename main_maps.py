# # main_maps.py
# import os
# from src.cleaningData import load_and_clean_data
# from src.analysis import summarize_by_precinct, top_offenses
# from src.map_visualization import (
#     create_precinct_choropleth,
#     create_heatmap_by_offense,
#     create_precinct_choropleth_by_offense,
# )

# # 🔧 filenames – adjust if your names differ
# CURRENT_CSV = "data/NYPD_Complaint_Data_Current_(Year_To_Date)_20251029.csv"
# PRECINCT_GEO = "data/Police_Precincts_20251109.geojson"


# def main():
#     os.makedirs("output", exist_ok=True)

#     # 1) Load & clean current-year data
#     df = load_and_clean_data(CURRENT_CSV)

#     # 2) Quick console summary
#     by_pct = summarize_by_precinct(df)
#     print(by_pct.head())

#     # 3) Choropleth (all crimes, one map)
#     create_precinct_choropleth(
#         df,
#         precinct_geojson_path=PRECINCT_GEO,
#         out_html="output/nyc_crime_by_precinct.html",
#         offense=None,
#     )

#     # 4) Choropleth with offense selector
#     offenses = top_offenses(df, n=6)
#     create_precinct_choropleth_by_offense(
#         df,
#         precinct_geojson_path=PRECINCT_GEO,
#         out_html="output/nyc_crime_by_precinct_by_offense.html",
#         offenses=offenses,
#     )

#     # 5) Heatmap with offense selector
#     create_heatmap_by_offense(
#         df,
#         precinct_geojson_path=PRECINCT_GEO,
#         out_html="output/nyc_crime_heatmap_by_offense.html",
#         offenses=offenses,
#     )


# if __name__ == "__main__":
#     main()

# main_maps.py
import os
from src.cleaningData import load_and_clean_data
from src.analysis import summarize_by_precinct, top_offenses
from src.map_visualization import create_heatmap_by_offense

# 🔧 filenames – adjust if your names differ
CURRENT_CSV = "data/NYPD_Complaint_Data_Current_(Year_To_Date)_20251029.csv"
PRECINCT_GEO = "data/Police_Precincts_20251109.geojson"


def main():
    os.makedirs("output", exist_ok=True)

    # 1) Load & clean current-year data
    df = load_and_clean_data(CURRENT_CSV)

    # 2) Quick console summary by precinct (tabular, no map)
    by_pct = summarize_by_precinct(df)
    print(by_pct.head())

    # 3) Pick top offenses for layers
    offenses = top_offenses(df, n=6)

    # 4) Heatmap with offense selector (only map we generate now)
    create_heatmap_by_offense(
        df,
        precinct_geojson_path=PRECINCT_GEO,
        out_html="output/nyc_crime_heatmap_by_offense.html",
        offenses=offenses,
    )


if __name__ == "__main__":
    main()

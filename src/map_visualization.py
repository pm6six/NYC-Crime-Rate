import pandas as pd
import folium
from folium import FeatureGroup
from folium.plugins import HeatMap


def create_heatmap_by_offense(
    df: pd.DataFrame,
    precinct_geojson_path: str,   # kept for API symmetry; not used here
    out_html: str = "output/nyc_crime_heatmap_by_offense.html",
    offenses: list[str] | None = None,
    top_k: int = 6,
):
    """
    One heatmap layer per offense + a LayerControl selector.

    This map shows *crime density*, not per-precinct totals.
    Legend explains intensity (hotspots), not numeric precinct counts.
    Also computes an approximate mapping from "light/medium/dark" to
    example ranges of incident counts in small spatial bins.
    """
    # --- filter to rows with coordinates in NYC bounds ---
    pts = df.dropna(subset=["Latitude", "Longitude"]).copy()
    pts = pts[
        (pts["Latitude"].between(40.45, 40.95)) &
        (pts["Longitude"].between(-74.3, -73.65))
    ]

    if offenses is None:
        offenses = (
            pts["OFNS_DESC"]
            .value_counts()
            .head(top_k)
            .index
            .tolist()
        )

    # ---------- APPROXIMATE COUNT RANGES FOR LEGEND ----------
    # Make a simple grid by rounding lat/lon (≈ 100–150m cells)
    grid = pts.copy()
    grid["lat_bin"] = grid["Latitude"].round(3)
    grid["lon_bin"] = grid["Longitude"].round(3)

    cell_counts = grid.groupby(["lat_bin", "lon_bin"]).size()

    # If there are counts, compute quantiles for low/medium/high
    if not cell_counts.empty:
        q20, q50, q80 = cell_counts.quantile([0.2, 0.5, 0.8]).astype(int).tolist()
        low_max = max(q20, 1)
        med_max = max(q50, low_max + 1)
        high_max = max(q80, med_max + 1)
    else:
        low_max, med_max, high_max = 1, 2, 3  # fallback

    # ---------- BUILD THE MAP ----------
    m = folium.Map(location=[40.73, -73.96], zoom_start=12, tiles="cartodbpositron")

    # All crimes = neutral green
    all_gradient = {
        0.2: "#b2df8a",
        0.4: "#66c2a5",
        0.6: "#41ae76",
        0.8: "#238b45",
        1.0: "#005824",
    }

    # Distinct gradients for each offense
    offense_gradients = [
        {
            0.2: "#fcae91",
            0.4: "#fb6a4a",
            0.6: "#ef3b2c",
            0.8: "#cb181d",
            1.0: "#99000d",
        },
        {
            0.2: "#bdd7e7",
            0.4: "#6baed6",
            0.6: "#3182bd",
            0.8: "#08519c",
            1.0: "#08306b",
        },
        {
            0.2: "#dadaeb",
            0.4: "#bcbddc",
            0.6: "#9e9ac8",
            0.8: "#756bb1",
            1.0: "#54278f",
        },
        {
            0.2: "#fdd0a2",
            0.4: "#fdae6b",
            0.6: "#fd8d3c",
            0.8: "#e6550d",
            1.0: "#a63603",
        },
        {
            0.2: "#c7e9c0",
            0.4: "#74c476",
            0.6: "#41ab5d",
            0.8: "#238b45",
            1.0: "#005a32",
        },
        {
            0.2: "#cccccc",
            0.4: "#969696",
            0.6: "#636363",
            0.8: "#252525",
            1.0: "#000000",
        },
    ]

    # All crimes (default visible)
    fg_all = FeatureGroup(name="All crimes", show=True)
    HeatMap(
        data=pts[["Latitude", "Longitude"]].values.tolist(),
        radius=12,
        blur=20,
        min_opacity=0.55,
        max_zoom=14,
        gradient=all_gradient,
    ).add_to(fg_all)
    fg_all.add_to(m)

    # One layer per offense
    for idx, name in enumerate(offenses):
        sub = pts[pts["OFNS_DESC"] == name]
        if sub.empty:
            continue

        gradient = offense_gradients[idx % len(offense_gradients)]

        fg = FeatureGroup(name=name, show=False)
        HeatMap(
            data=sub[["Latitude", "Longitude"]].values.tolist(),
            radius=12,
            blur=20,
            min_opacity=0.60,
            max_zoom=14,
            gradient=gradient,
        ).add_to(fg)
        fg.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    # ---------- LEGEND WITH NUMERIC EXAMPLE ----------
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index:9999;
        background:white;
        padding:10px 14px;
        border:2px solid #555;
        border-radius:6px;
        font-size:13px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
        <div style="font-weight:bold;margin-bottom:6px;">
            Crime heatmap intensity (2025 YTD)
        </div>
        <div style="font-size:12px;line-height:1.4;">
            This map shows <b>where</b> 2025 incidents are concentrated.<br>
            • Lighter color ≈ grid cells with about 1–{low_max} incidents.<br>
            • Medium color ≈ cells with ~{low_max+1}–{med_max} incidents.<br>
            • Darker hotspots ≈ cells with &gt;{high_max} incidents.<br>
            (Counts are approximate; the heatmap uses smoothing.)
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save(out_html)
    print(f"Filterable heatmap saved -> {out_html}")

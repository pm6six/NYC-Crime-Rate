# main_forecasting.py
import os
from src.cleaningData import load_and_clean_data
from src.analysis import monthly_borough_series
from src.time_series import make_borough_series, fit_arima_forecast, plot_forecast

# 🔧 your new historic file (filtered to 2013–2019 + 2023–2025)
HISTORIC_CSV = "data/NYPD_Complaint_2022_2025.csv"


# Borough names in your dataset (use upper-case strings)
BOROUGHS = [
    "MANHATTAN",
    "BROOKLYN",
    "BRONX",
    "QUEENS",
    "STATEN ISLAND",
]

def main():
    os.makedirs("output", exist_ok=True)
    df = load_and_clean_data(HISTORIC_CSV)

    monthly_df = monthly_borough_series(df)
    monthly_csv_path = "output/monthly_borough_counts_historic.csv"
    monthly_df.to_csv(monthly_csv_path, index=False)
    print(f"Saved monthly borough table -> {monthly_csv_path}")
    print(monthly_df.head())

    for boro in BOROUGHS:
        print(f"\n=== Forecasting for {boro} ===")
        series = make_borough_series(monthly_df, boro)

        # Skip if not enough data
        if len(series) < 36:
            print(f"Skipping {boro}: series too short ({len(series)} months)")
            continue

        result_df, model_fit = fit_arima_forecast(
            series,
            order=(1, 1, 1),      # simple starting point; can be tuned
            forecast_horizon=12,  # next 12 months
            holdout=12,           # last 12 months as test set
        )

        # Save forecast table
        csv_out = f"output/forecast_{boro.replace(' ', '_').lower()}.csv"
        result_df.to_csv(csv_out)
        print(f"Forecast table saved -> {csv_out}")

        # Save plot
        png_out = f"output/forecast_{boro.replace(' ', '_').lower()}.png"
        plot_forecast(result_df, borough=boro, out_path=png_out)

if __name__ == "__main__":
    main()

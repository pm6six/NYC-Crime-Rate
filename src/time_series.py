import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


def make_borough_series(
    monthly_df: pd.DataFrame,
    borough: str,
    freq: str = "MS",
) -> pd.Series:
    """
    Build a univariate monthly time series for one borough.

    monthly_df columns:
        - MONTH
        - BORO_NM
        - crime_count
    """
    s = (
        monthly_df[monthly_df["BORO_NM"] == borough]
        .set_index("MONTH")["crime_count"]
        .sort_index()
    )

    # monthly index, fill missing months with 0
    s = s.asfreq(freq).fillna(0)

    return s

def fit_arima_forecast(
    series: pd.Series,
    order: tuple[int, int, int] = (1, 1, 1),
    forecast_horizon: int = 12,
    holdout: int = 12,
) -> tuple[pd.DataFrame, ARIMA]:
    """
    Fit an ARIMA model, keep last `holdout` months as test, and forecast.

    Returns:
        result_df: index = dates, columns:
            - 'actual'   (observed counts; NaN for future)
            - 'forecast' (model predictions)
        model_fit: fitted ARIMA object
    """
    if len(series) <= holdout + 5:
        raise ValueError("Series too short for train/test split.")

    train = series.iloc[:-holdout]
    test = series.iloc[-holdout:]

    model = ARIMA(train, order=order)
    model_fit = model.fit()

    # Forecast for test period
    forecast_test = model_fit.forecast(steps=holdout)

    # Forecast further into the future
    forecast_future = model_fit.forecast(steps=holdout + forecast_horizon)[-forecast_horizon:]

    # Build combined DataFrame
    future_index = pd.date_range(
        series.index[-1] + series.index.freq,
        periods=forecast_horizon,
        freq=series.index.freq,
    )

    idx = series.index.append(future_index)
    result_df = pd.DataFrame(index=idx, columns=["actual", "forecast"])

    result_df.loc[series.index, "actual"] = series.values
    result_df.loc[test.index, "forecast"] = forecast_test.values
    result_df.loc[future_index, "forecast"] = forecast_future.values

    return result_df, model_fit


def plot_forecast(
    result_df: pd.DataFrame,
    borough: str,
    out_path: str,
):
    """
    Save a simple line plot of actual vs forecast.
    """
    ax = result_df[["actual", "forecast"]].astype("float").plot(figsize=(10, 5))
    ax.set_title(f"Monthly crime counts forecast – {borough.title()}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of complaints")
    ax.legend(["Actual", "Forecast"])
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Forecast plot saved -> {out_path}")

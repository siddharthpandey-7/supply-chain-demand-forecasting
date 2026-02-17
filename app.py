from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model & feature list
model = joblib.load("models/final_model.joblib")
feature_cols = joblib.load("models/feature_columns.joblib")

# Load historical data
df = pd.read_csv("data/retail_demand.csv")
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date", "Order_Demand"])
df = df.sort_values("Date")

# Weekly aggregation (same as training)
weekly_df = (
    df
    .resample("W", on="Date")["Order_Demand"]
    .sum()
    .reset_index()
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        year = int(data["year"])
        month = int(data["month"])
        week = int(data["week"])

        # Use last 3 weeks from history
        recent = weekly_df.tail(3)

        lag_1 = recent.iloc[-1]["Order_Demand"]
        lag_2 = recent.iloc[-2]["Order_Demand"]
        lag_3 = recent.iloc[-3]["Order_Demand"]

        rolling_mean_3 = recent["Order_Demand"].mean()
        rolling_std_3 = recent["Order_Demand"].std()

        base_input = {
            "lag_1": lag_1,
            "lag_2": lag_2,
            "lag_3": lag_3,
            "rolling_mean_3": rolling_mean_3,
            "rolling_std_3": rolling_std_3,
            "week": week,
            "month": month,
            "year": year
        }

        # Single-week prediction
        X = pd.DataFrame([base_input])[feature_cols]
        prediction = model.predict(X)[0]

        # Multi-week forecast (next 4 weeks)
        future_preds = []
        temp_lags = [lag_1, lag_2, lag_3]

        for i in range(1, 5):
            rm = np.mean(temp_lags)
            rs = np.std(temp_lags)

            future_input = {
                "lag_1": temp_lags[0],
                "lag_2": temp_lags[1],
                "lag_3": temp_lags[2],
                "rolling_mean_3": rm,
                "rolling_std_3": rs,
                "week": min(week + i, 53),
                "month": month,
                "year": year
            }

            X_future = pd.DataFrame([future_input])[feature_cols]
            pred = model.predict(X_future)[0]

            future_preds.append(round(float(pred), 2))
            temp_lags = [pred] + temp_lags[:2]

        # Feature importance (top 5)
        importance = dict(zip(feature_cols, model.feature_importances_))
        top_features = sorted(
            importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        explanation = [
            {"feature": f, "importance": round(i * 100, 2)}
            for f, i in top_features
        ]

        return jsonify({
            "success": True,
            "prediction": round(float(prediction), 2),
            "future_predictions": future_preds,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

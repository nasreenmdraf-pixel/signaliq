import pandas as pd
import numpy as np

def load_data():
    return pd.read_csv("data/ads_data.csv")

# Model A - Temporal (Best Time to Post)
def temporal_model(df):
    hourly = df.groupby("hour").agg({
        "conversions": "mean",
        "spend": "mean",
        "ctr": "mean"
    }).reset_index()
    hourly["score"] = (hourly["conversions"] * 0.5) + (hourly["ctr"] * 0.3) - (hourly["spend"] * 0.001)
    best_hours = hourly.sort_values("score", ascending=False).head(5)
    return best_hours[["hour", "score"]].to_dict("records")

# Model B - Creative Signal
def creative_model(df):
    creative = df.groupby("creative_format").agg({
        "ctr": "mean",
        "conversions": "mean",
        "cpa": "mean"
    }).reset_index()
    creative["score"] = (creative["ctr"] * 0.4) + (creative["conversions"] * 0.4) - (creative["cpa"] * 0.2)
    best = creative.sort_values("score", ascending=False)
    return best.to_dict("records")

# Model C - Targeting Advisor (Simple version)
def targeting_model(df):
    total_conversions = df["conversions"].sum()
    avg_cpa = df["cpa"].mean()
    
    if total_conversions > 2000 and avg_cpa < 15:
        return "Broaden targeting – signal quality is high"
    elif total_conversions < 500:
        return "Keep targeting narrow – still learning"
    else:
        return "Maintain current targeting"

# Model D - Seasonal (Simple version)
def seasonal_model(df):
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby("date")["conversions"].sum().reset_index()
    recent = daily.tail(14)["conversions"].mean()
    older = daily.head(30)["conversions"].mean()
    
    if recent > older * 1.3:
        return "Demand is rising – good time to increase budget"
    else:
        return "Demand is stable – normal budget is fine"

# Final Scorecard
def generate_scorecard():
    df = load_data()
    
    temporal = temporal_model(df)
    creative = creative_model(df)
    targeting = targeting_model(df)
    seasonal = seasonal_model(df)
    
    # Simple readiness score
    score = 72  # You can make this smarter later
    
    recommendations = [
        f"Best posting hours: {', '.join([str(h['hour'])+':00' for h in temporal[:3]])}",
        f"Best creative format: {creative[0]['creative_format']}",
        targeting,
        seasonal
    ]
    
    return {
        "readiness_score": score,
        "recommendations": recommendations,
        "best_hours": temporal[:3],
        "best_creative": creative[0]
    }

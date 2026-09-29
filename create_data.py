import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create 90 days of fake Meta Ads data
dates = [datetime.now() - timedelta(days=x) for x in range(90)]
hours = list(range(24))

data = []
for d in dates:
    for h in hours:
        data.append({
            "date": d.strftime("%Y-%m-%d"),
            "hour": h,
            "day_of_week": d.strftime("%A"),
            "spend": round(np.random.uniform(50, 500), 2),
            "impressions": np.random.randint(1000, 20000),
            "clicks": np.random.randint(20, 800),
            "conversions": np.random.randint(1, 50),
            "creative_format": np.random.choice(["single_image", "carousel", "video", "reel"]),
            "region": np.random.choice(["US", "IN", "UK", "EU"])
        })

df = pd.DataFrame(data)
df["ctr"] = (df["clicks"] / df["impressions"] * 100).round(2)
df["cpa"] = (df["spend"] / df["conversions"]).round(2)

df.to_csv("data/ads_data.csv", index=False)
print("Fake data created successfully! File saved at data/ads_data.csv")

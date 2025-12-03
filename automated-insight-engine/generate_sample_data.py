import polars as pl
import numpy as np
from pathlib import Path

# Generate sample AdTech campaign data
np.random.seed(42)
n_rows = 1000

data = {
    "campaign_id": [f"CAMP_{i:04d}" for i in range(n_rows)],
    "impressions": np.random.randint(1000, 50000, n_rows),
    "clicks": np.random.randint(10, 2000, n_rows),
    "conversions": np.random.randint(0, 100, n_rows),
    "cost": np.random.uniform(100, 5000, n_rows).round(2),
    "revenue": np.random.uniform(200, 8000, n_rows).round(2),
}

# Inject some anomalies
anomaly_indices = np.random.choice(n_rows, 50, replace=False)
for idx in anomaly_indices:
    data["clicks"][idx] = int(data["clicks"][idx] * 0.1)
    data["cost"][idx] = data["cost"][idx] * 3

df = pl.DataFrame(data)

# Save to CSV
output_path = Path("data/sample_data.csv")
df.write_csv(output_path)
print(f"✓ Sample data generated: {output_path}")

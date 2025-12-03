import polars as pl
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Detect anomalies using Isolation Forest algorithm"""
    
    def __init__(self):
        self.model = IsolationForest(
            contamination=Config.CONTAMINATION_FACTOR,
            n_estimators=Config.N_ESTIMATORS,
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        
    def detect(self, df: pl.DataFrame) -> dict:
        """Detect anomalies in the dataset"""
        try:
            logger.info("🔍 Running anomaly detection...")
            
            # Get numeric columns only
            numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]]
            
            if len(numeric_cols) == 0:
                logger.warning("⚠️ No numeric columns for anomaly detection")
                return {"anomalies": [], "anomaly_count": 0}
            
            # Convert to numpy for sklearn
            X = df.select(numeric_cols).to_numpy()
            
            # Fit and predict
            predictions = self.model.fit_predict(X)
            anomaly_scores = self.model.score_samples(X)
            
            # -1 indicates anomaly, 1 indicates normal
            anomaly_indices = np.where(predictions == -1)[0]
            
            anomalies = []
            
            # Convert DataFrame to pandas for easier indexing
            df_pandas = df.to_pandas()
            
            for idx in anomaly_indices:
                anomaly_data = {
                    "row_index": int(idx),
                    "anomaly_score": float(anomaly_scores[idx]),
                    "values": {}
                }
                
                # Capture the anomalous values using pandas indexing
                for col in numeric_cols:
                    anomaly_data["values"][col] = float(df_pandas[col].iloc[idx])
                
                anomalies.append(anomaly_data)
            
            # Sort by severity (most anomalous first)
            anomalies = sorted(anomalies, key=lambda x: x["anomaly_score"])
            
            logger.info(f"✓ Detected {len(anomalies)} anomalies ({len(anomalies)/len(df)*100:.1f}% of data)")
            
            return {
                "anomalies": anomalies[:10],  # Return top 10 anomalies
                "anomaly_count": len(anomalies),
                "total_rows": len(df),
                "anomaly_percentage": round(len(anomalies) / len(df) * 100, 2)
            }
            
        except Exception as e:
            logger.error(f"❌ Anomaly detection failed: {str(e)}")
            raise

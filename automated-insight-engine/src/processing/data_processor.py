import polars as pl
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Data transformation and aggregation using Polars"""
    
    @staticmethod
    def calculate_metrics(df: pl.DataFrame) -> dict:
        """Calculate key business metrics"""
        try:
            # Identify numeric columns for analysis
            numeric_cols = [col for col in df.columns if df[col].dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]]
            
            if not numeric_cols:
                raise ValueError("No numeric columns found for analysis")
            
            metrics = {
                "total_rows": len(df),
                "columns": df.columns,
                "numeric_columns": numeric_cols,
                "summary_stats": {}
            }
            
            # Calculate summary statistics for each numeric column
            for col in numeric_cols:
                metrics["summary_stats"][col] = {
                    "mean": df[col].mean(),
                    "median": df[col].median(),
                    "std": df[col].std(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "sum": df[col].sum()
                }
            
            logger.info(f"✓ Calculated metrics for {len(numeric_cols)} numeric columns")
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Metric calculation failed: {str(e)}")
            raise
    
    @staticmethod
    def prepare_for_ml(df: pl.DataFrame) -> pl.DataFrame:
        """Prepare data for machine learning (handle nulls, encode if needed)"""
        # Fill nulls with column mean for numeric columns
        for col in df.columns:
            if df[col].dtype in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]:
                if df[col].null_count() > 0:
                    mean_val = df[col].mean()
                    df = df.with_columns(pl.col(col).fill_null(mean_val))
        
        logger.info("✓ Data prepared for ML processing")
        return df

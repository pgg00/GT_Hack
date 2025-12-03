import polars as pl
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Handle data loading from various sources"""
    
    @staticmethod
    def load_csv(file_path: Path) -> pl.DataFrame:
        """Load CSV file using Polars for faster processing"""
        try:
            logger.info(f"📊 Loading data from {file_path.name}")
            
            # Polars provides faster CSV reading than Pandas
            df = pl.read_csv(
                file_path,
                infer_schema_length=10000,  # Scan more rows for better type inference
                try_parse_dates=True
            )
            
            logger.info(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"❌ Failed to load CSV: {str(e)}")
            raise
    
    @staticmethod
    def validate_data(df: pl.DataFrame) -> bool:
        """Basic data validation"""
        if df.is_empty():
            raise ValueError("DataFrame is empty")
            
        if df.height < 10:
            logger.warning("⚠️ Dataset has fewer than 10 rows - results may be unreliable")
            
        logger.info("✓ Data validation passed")
        return True

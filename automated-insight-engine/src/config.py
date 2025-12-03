import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management"""
    
    # Base directories
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    TEMPLATE_DIR = BASE_DIR / "src" / "templates"
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
    
    # ML Model Configuration
    CONTAMINATION_FACTOR = float(os.getenv("CONTAMINATION_FACTOR", "0.1"))
    N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", "100"))
    
    # Ensure directories exist
    @classmethod
    def setup_directories(cls):
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        print("✓ Configuration validated successfully")
        return True

# Setup directories on import
Config.setup_directories()

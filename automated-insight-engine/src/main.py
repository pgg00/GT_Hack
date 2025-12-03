import logging
from pathlib import Path
from src.config import Config
from src.ingestion.file_watcher import FileWatcher
from src.ingestion.data_loader import DataLoader
from src.processing.data_processor import DataProcessor
from src.processing.anomaly_detector import AnomalyDetector
from src.analysis.ai_analyzer import AIAnalyzer
from src.reporting.visualizer import Visualizer
from src.reporting.pdf_generator import PDFGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InsightEngine:
    """Main orchestrator for the automated insight engine"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.processor = DataProcessor()
        self.anomaly_detector = AnomalyDetector()
        self.ai_analyzer = AIAnalyzer()
        self.visualizer = Visualizer()
        self.pdf_generator = PDFGenerator()
        
    def process_file(self, file_path: Path):
        """Complete ETL pipeline for a single file"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 STARTING PIPELINE FOR: {file_path.name}")
        logger.info(f"{'='*60}\n")
        
        start_time = __import__('time').time()
        
        try:
            # 1. INGEST
            df = self.data_loader.load_csv(file_path)
            self.data_loader.validate_data(df)
            
            # 2. PROCESS
            df_clean = self.processor.prepare_for_ml(df)
            metrics = self.processor.calculate_metrics(df_clean)
            
            # 3. DETECT ANOMALIES
            anomalies = self.anomaly_detector.detect(df_clean)
            
            # 4. AI ANALYSIS
            insights = self.ai_analyzer.generate_insights(metrics, anomalies)
            
            # 5. VISUALIZE
            charts = self.visualizer.create_summary_charts(df_clean, metrics)
            
            # 6. GENERATE REPORT
            report_data = {
                "title": f"Analysis Report: {file_path.stem}",
                "metrics": metrics,
                "anomalies": anomalies,
                "insights": insights,
                "charts": charts
            }
            
            output_filename = f"report_{file_path.stem}_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = self.pdf_generator.generate(report_data, output_filename)
            
            elapsed = __import__('time').time() - start_time
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✅ PIPELINE COMPLETED IN {elapsed:.1f} SECONDS")
            logger.info(f"📄 Report saved: {pdf_path}")
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"\n❌ PIPELINE FAILED: {str(e)}\n")
            raise

def main():
    """Entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        🚀 AUTOMATED INSIGHT ENGINE - H-001 🚀            ║
    ║                                                           ║
    ║        Event-Driven Data Pipeline with AI Insights        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Validate configuration
    Config.validate()
    
    # Initialize engine
    engine = InsightEngine()
    
    # Start file watcher
    watcher = FileWatcher(
        watch_directory=Config.INPUT_DIR,
        callback=engine.process_file
    )
    
    watcher.start()

if __name__ == "__main__":
    main()

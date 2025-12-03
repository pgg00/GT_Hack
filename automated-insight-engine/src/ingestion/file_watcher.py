import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataFileHandler(FileSystemEventHandler):
    """Event handler for monitoring new data files"""
    
    def __init__(self, callback):
        self.callback = callback
        self.processed_files = set()
        
    def on_created(self, event):
        """Triggered when a new file is created"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Only process CSV files
        if file_path.suffix.lower() == '.csv' and file_path not in self.processed_files:
            logger.info(f"📥 New file detected: {file_path.name}")
            self.processed_files.add(file_path)
            
            # Wait briefly to ensure file is fully written
            time.sleep(1)
            
            # Trigger the processing callback
            try:
                self.callback(file_path)
            except Exception as e:
                logger.error(f"❌ Error processing {file_path.name}: {str(e)}")
                
class FileWatcher:
    """Monitors directory for new files and triggers processing"""
    
    def __init__(self, watch_directory, callback):
        self.watch_directory = Path(watch_directory)
        self.callback = callback
        self.observer = None
        
    def start(self):
        """Start monitoring the directory"""
        event_handler = DataFileHandler(self.callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_directory), recursive=False)
        self.observer.start()
        
        logger.info(f"👀 Watching directory: {self.watch_directory}")
        logger.info("🚀 Drop CSV files to start processing...")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("🛑 File watcher stopped")

import logging
from config.config import Config

def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=Config.LOG_LEVEL,
        filename=Config.LOG_FILE
    ) 
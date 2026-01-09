# utils/logger.py
import logging
from config.settings import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("LosieBot")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
# run.py - Use this instead of main.py for production
from main import *

if __name__ == "__main__":
    from utils.logger import logger
    logger.info("Losie Bot Production Mode Activated")
    main()
# main.py - Advanced Entry Point with Extra Features
import signal
import sys
import time
from datetime import datetime

from bot.instance import bot
from database.repository import init_db
from utils.logger import logger
from config.settings import BOT_NAME

# Global variables for uptime tracking
START_TIME = datetime.now()
BOT_USERNAME = None
BOT_ID = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    logger.info("Shutdown signal received. Stopping bot gracefully...")
    bot.stop_polling()
    uptime = datetime.now() - START_TIME
    logger.info(f"Bot stopped. Total uptime: {uptime}")
    sys.exit(0)

def get_bot_info():
    """Fetch bot username and ID once at startup"""
    global BOT_USERNAME, BOT_ID
    try:
        me = bot.get_me()
        BOT_USERNAME = me.username
        BOT_ID = me.id
        logger.info(f"Bot Info: @{BOT_USERNAME} (ID: {BOT_ID})")
    except Exception as e:
        logger.error(f"Failed to get bot info: {e}")
        BOT_USERNAME = "unknown"
        BOT_ID = "unknown"

def print_startup_banner():
    """Print a cool startup banner"""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     {BOT_NAME} BOT STARTED SUCCESSFULLY!     ║
║                                                          ║
║  Version     : 2.0 (Advanced Production Ready)          ║
║  Started at  : {START_TIME.strftime('%d %B %Y, %I:%M %p')}           ║
║  Bot         : @{BOT_USERNAME or 'Loading...'}                           ║
║  Status      : ONLINE & READY FOR ACTION 🔥              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """.strip()
    print(banner)
    logger.info("Startup banner displayed")

def run_bot():
    """Main bot running function with crash recovery"""
    global START_TIME
    attempt = 0
    max_retries = 5
    
    while attempt < max_retries:
        attempt += 1
        try:
            logger.info(f"Starting polling attempt {attempt}/{max_retries}...")
            bot.infinity_polling(
                none_stop=True,
                interval=1,
                timeout=20,
                long_polling_timeout=20
            )
        except KeyboardInterrupt:
            signal_handler(None, None)
        except Exception as e:
            logger.error(f"Bot crashed (attempt {attempt}): {str(e)}")
            if attempt < max_retries:
                wait = 10 * attempt
                logger.info(f"Restarting in {wait} seconds...")
                time.sleep(wait)
                START_TIME = datetime.now()  # Reset uptime on restart
            else:
                logger.critical("Max restart attempts reached. Exiting.")
                sys.exit(1)

if __name__ == "__main__":
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Initializing Losie Bot...")
    
    # Initialize database
    init_db()
    
    # Get bot info
    get_bot_info()
    
    # Print cool banner
    print_startup_banner()
    
    # Import handlers (to register them)
    try:
        import handlers.start_handler
        import handlers.message_handler
        import handlers.payment_handler
        import handlers.admin_handler
        logger.info("All handlers loaded successfully")
    except Exception as e:
        logger.critical(f"Failed to load handlers: {e}")
        sys.exit(1)
    
    # Start the bot with auto-restart
    run_bot()

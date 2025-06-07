# main.py
import sys
import logging
from app_controller import AppController

if __name__ == '__main__':
    # Configure basic logging for the main entry point
    # AppController might set up more sophisticated logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        controller = AppController()
        controller.run()
    except Exception as e:
        logging.critical(f"Application failed to start: {e}", exc_info=True)
        # Optionally, show a user-friendly error message dialog here
        sys.exit(1)

    sys.exit(0) # Assuming controller.run() will block until app exits

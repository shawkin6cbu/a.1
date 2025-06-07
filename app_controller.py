# app_controller.py

import logging
import sys # Required for QApplication and sys.exit
import yaml # For loading config.YAML
from PyQt6.QtWidgets import QApplication # Required for Qt App
from gui.main_window import ContractProcessorApp # Main application window
from gui.styles import modern_stylesheet # Application stylesheet

class AppController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("AppController initialized.")

        # Load configuration from config.YAML
        try:
            with open("config.YAML", 'r') as f:
                self.config = yaml.safe_load(f)
            if self.config is None: # Handle empty or invalid YAML
                self.config = {}
                self.logger.warning("config.YAML is empty or invalid. Using default empty config.")
            self.logger.info("Configuration loaded from config.YAML.")
        except FileNotFoundError:
            self.config = {} # Default empty config if file not found
            self.logger.error("config.YAML not found. Using default empty config.")
        except yaml.YAMLError as e:
            self.config = {} # Default empty config on parsing error
            self.logger.error(f"Error parsing config.YAML: {e}. Using default empty config.")

        # Initialize GUI components
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(modern_stylesheet)

        # Pass the loaded config to the main window
        self.main_window = ContractProcessorApp(config=self.config)
        # self.main_window.show() # Show will be called in run()

    def run(self):
        self.logger.info("Application starting...")
        self.main_window.show()
        # Start the main GUI event loop
        exit_code = self.app.exec()
        self.logger.info("Application finished.")
        sys.exit(exit_code)

if __name__ == '__main__':
    # This basicConfig is for when app_controller.py is run directly
    # In the main application flow, main.py's basicConfig will likely take precedence
    # or a more sophisticated logging setup will be used.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    controller = AppController()
    controller.run()

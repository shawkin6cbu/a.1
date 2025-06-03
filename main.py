import sys
import os # Though os might not be directly used here, it's good practice if create_standard_dirs were enabled
from PyQt6.QtWidgets import QApplication, QMessageBox # QMessageBox for optional directory creation
from gui.main_window import ContractProcessorApp
from gui.styles import modern_stylesheet
# from processing_logic import create_standard_dirs # If the optional directory creation is used

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # --- APPLY THE STYLESHEET TO THE ENTIRE APPLICATION ---
    app.setStyleSheet(modern_stylesheet)

    # --- Optional: Create standard directories (example call) ---
    # (You can keep or remove this block based on your preference for handling directory creation)
    # Ensure create_standard_dirs is defined or imported if you uncomment this.
    # root_dir_to_setup = r"C:\Users\shawk\Desktop\a.1" 
    # if not os.path.exists(os.path.join(root_dir_to_setup, "Logs")):
    #     # Assuming create_standard_dirs is available and imported
    #     reply = QMessageBox.question(None, 'Application Setup',
    #                                  f"Standard folders might be missing in:\n{root_dir_to_setup}\nCreate them?",
    #                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    #                                  QMessageBox.StandardButton.Yes)
    #     if reply == QMessageBox.StandardButton.Yes:
    #         # if create_standard_dirs(root_dir_to_setup): # Definition or import needed
    #         #     QMessageBox.information(None, "Setup Complete", f"Standard directories created/verified.")
    #         # else:
    #         #     QMessageBox.warning(None, "Setup Issue", f"Could not create all standard directories.")
    #         pass # Placeholder if create_standard_dirs is not yet implemented/imported

    main_window = ContractProcessorApp()
    main_window.show()
    sys.exit(app.exec())

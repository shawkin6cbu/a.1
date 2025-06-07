import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QComboBox, QGroupBox, QCheckBox, QLabel, QListWidget,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit,
    QStatusBar, QProgressBar, QFileDialog, QMessageBox, QSizePolicy,
    QSpacerItem, QCompleter, QInputDialog, QListView,
    QRadioButton # Make sure QRadioButton is imported if not already
)
from PyQt6.QtCore import Qt, pyqtSignal, QDir, QTimer, QDateTime, QAbstractItemModel
from PyQt6.QtGui import QAction, QPalette, QColor

# --- Import functions from processing_logic.py ---
from processing_logic import check_folder_exists
from processing_logic import get_initial_legacy_folder_name_and_data
from processing_logic import handle_legacy_contract_processing
from processing_logic import copy_pdf_to_folder
from processing_logic import get_all_legacy_contract_field_names

# --- Import custom GUI components ---
from gui.widgets import CustomComboBox, PDFListWidget # Ensure correct relative import
from gui.tabs.processing_tab import create_processing_tab
from gui.tabs.data_viewer_tab import create_data_viewer_tab


class ContractProcessorApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contract Processing Application")
        self.setGeometry(100, 100, 900, 700)

        # It's generally better to set the style once in main.py on the QApplication instance
        # QApplication.setStyle("Fusion") # If you want to force Fusion style

        self.init_ui() 
        self.log_message("Application initialized. Ready.")
        self.extracted_data_cache = None

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self._create_menu_bar()

        self.tab_widget = QTabWidget()

        # These will assign widgets like self.rb_refi, self.chk_seller to self
        self.processing_tab = create_processing_tab(self) 
        self.data_viewer_tab = create_data_viewer_tab(self)

        self.tab_widget.addTab(self.processing_tab, "Processing Controls")
        self.tab_widget.addTab(self.data_viewer_tab, "Extracted Data Viewer")

        main_layout.addWidget(self.tab_widget)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100)
        main_layout.addWidget(self.log_area)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar, 1)

        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

    def _update_output_directory_for_contract_type(self, contract_type_text):
        if contract_type_text == "Legacy":
            self.output_dir_edit.setText("C:/Closings/Legacy Seller")
        else:
            self.output_dir_edit.setText("C:/Closings")

    def _select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory",
            self.output_dir_edit.text() or QDir.homePath()
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)
            self.log_message(f"Output directory selected: {dir_path}")

    def _get_and_validate_processing_inputs(self):
        contract_type = self.contract_type_combo.currentText()
        generate_label = self.chk_generate_file_label.isChecked()
        generate_docs = self.chk_generate_setup_docs.isChecked()
        pdfs_list = [self.pdf_list_widget.item(i).text() for i in range(self.pdf_list_widget.count())]
        single_pdf_file = pdfs_list[0] if pdfs_list else None
        output_dir = self.output_dir_edit.text()
        is_buyer_checked = self.chk_buyer.isChecked()
        is_seller_checked = self.chk_seller.isChecked() # This will now reflect the Refi logic

        if not single_pdf_file:
            self.show_warning("No PDF file selected.")
            self.log_message("Processing attempted with no PDF.", "WARNING")
            return None, None, None, None, None, None, None
        if not output_dir:
            self.show_warning("Output directory not selected.")
            self.log_message("Processing attempted with no output directory.", "WARNING")
            return None, None, None, None, None, None, None
        if not contract_type:
            self.show_warning("No contract type selected.")
            self.log_message("Processing attempted with no contract type selected.", "WARNING")
            return None, None, None, None, None, None, None
        
        return contract_type, single_pdf_file, output_dir, generate_label, generate_docs, is_buyer_checked, is_seller_checked

    def _negotiate_legacy_folder_name(self, output_dir: str, proposed_folder_name: str, extracted_data: dict) -> str | None:
        target_path = os.path.join(output_dir, proposed_folder_name)
        final_folder_name = proposed_folder_name
        if check_folder_exists(target_path):
            overwrite_reply = QMessageBox.question(
                self, "Folder Exists",
                f"Folder '{proposed_folder_name}' already exists in '{output_dir}'.\nDo you want to overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
            )
            if overwrite_reply == QMessageBox.StandardButton.No:
                rename_reply = QMessageBox.question(
                    self, "Rename Folder",
                    "Do you want to rename the new folder? If no, processing for this item will be cancelled.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes
                )
                if rename_reply == QMessageBox.StandardButton.Yes:
                    new_name_candidate, ok = QInputDialog.getText(
                        self, "Rename Folder", "Enter new folder name:", text=proposed_folder_name
                    )
                    if ok and new_name_candidate and new_name_candidate.strip():
                        final_folder_name = new_name_candidate.strip()
                        self.log_message(f"Folder will be named: {final_folder_name}", "INFO")
                    else:
                        self.log_message(f"Folder renaming cancelled or invalid name for {proposed_folder_name}.", "INFO")
                        if extracted_data: self.update_extracted_data_viewer(extracted_data)
                        return None
                else:
                    self.log_message(f"Processing cancelled for {proposed_folder_name} due to existing folder and no rename.", "INFO")
                    if extracted_data: self.update_extracted_data_viewer(extracted_data)
                    return None
            else:
                self.log_message(f"Proceeding with overwriting folder: {proposed_folder_name}", "INFO")
        return final_folder_name

    def _handle_legacy_processing(self, single_pdf_file: str, output_dir: str, is_buyer_checked: bool, is_seller_checked: bool):
        self.log_message(f"Initiating Legacy processing for: {single_pdf_file}. Buyer: {is_buyer_checked}, Seller: {is_seller_checked}", "INFO")
        proposed_folder_name, extracted_data, error_message = get_initial_legacy_folder_name_and_data(single_pdf_file)
        self.extracted_data_cache = extracted_data
        if error_message or not proposed_folder_name:
            self.log_message(f"Failed to get proposed folder name or parse data: {error_message}", "ERROR")
            self.show_warning(f"Could not determine folder name or parse essential data: {error_message}")
            if extracted_data: self.update_extracted_data_viewer(extracted_data)
            return
        final_folder_name_for_processing = self._negotiate_legacy_folder_name(output_dir, proposed_folder_name, extracted_data)
        if not final_folder_name_for_processing:
            return
        self.log_message(f"Calling core processing for folder: {final_folder_name_for_processing}", "INFO")
        created_path, message = handle_legacy_contract_processing(
            [single_pdf_file], output_dir, final_folder_name_for_processing, extracted_data,
            is_buyer_checked, is_seller_checked
        )
        if created_path:
            self.log_message(f"SUCCESS (Legacy Folder Structure): {message}", "INFO")
            pdf_filename_to_copy = os.path.basename(single_pdf_file)
            copy_success, copy_message = copy_pdf_to_folder(single_pdf_file, created_path, pdf_filename_to_copy)
            if copy_success:
                self.log_message(copy_message, "INFO")
                QMessageBox.information(self, "Processing Complete",
                                        f"Legacy contract structure created/updated at:\n{created_path}\n"
                                        f"PDF '{pdf_filename_to_copy}' copied successfully.")
            else:
                self.log_message(copy_message, "ERROR")
                QMessageBox.warning(self, "Processing Warning",
                                    f"Legacy contract structure created/updated at:\n{created_path}\n"
                                    f"BUT, failed to copy PDF: {copy_message}")
        else:
            self.log_message(f"ERROR (Legacy Folder Structure): {message}", "ERROR")
            self.show_warning(f"Legacy processing failed: {message}")
        self.update_extracted_data_viewer(extracted_data)

    def _start_processing_placeholder(self):
        inputs = self._get_and_validate_processing_inputs()
        if inputs is None or not all(inputs) or any(val is None for val in inputs): # More robust check
            self.log_message("Validation failed or some inputs are None, aborting processing.", "WARNING")
            return
        contract_type, single_pdf_file, output_dir, generate_label, generate_docs, is_buyer_checked, is_seller_checked = inputs
        self.log_message(f"Starting processing...")
        self.log_message(f"  Contract Type: {contract_type}")
        self.log_message(f"  Generate Label: {generate_label}")
        self.log_message(f"  Generate Docs: {generate_docs}")
        self.log_message(f"  Is Buyer: {is_buyer_checked}")
        self.log_message(f"  Is Seller: {is_seller_checked}") # Will reflect disabled state if Refi
        self.log_message(f"  PDF: {single_pdf_file}")
        self.log_message(f"  Output Dir: {output_dir}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.status_label.setText(f"Processing {contract_type}...")
        if contract_type == "Legacy":
            self._handle_legacy_processing(single_pdf_file, output_dir, is_buyer_checked, is_seller_checked)
        else:
            self.log_message(f"Processing logic for '{contract_type}' is not yet implemented.", "WARNING")
            self.log_message(f"  (For non-Legacy: Buyer: {is_buyer_checked}, Seller: {is_seller_checked})", "DEBUG") 
            QMessageBox.information(self, "Processing", f"Placeholder processing for {contract_type} complete!")
            if hasattr(self, 'data_table'): self.data_table.setRowCount(0) # Check if data_table exists
            self.extracted_data_cache = None
        self.progress_bar.setValue(100)
        # QTimer.singleShot(500, lambda: self.progress_bar.setVisible(False)) # Optionally hide after a delay
        self.progress_bar.setVisible(False)
        self.status_label.setText("Processing finished.")

    def _save_table_data_to_pxt(self):
        if not hasattr(self, 'data_table') or self.data_table.rowCount() == 0:
            self.log_message("No data in table to save.", "WARNING")
            QMessageBox.information(self, "No Data", "There is no data in the table to save.")
            return
        table_data = {}
        for row in range(self.data_table.rowCount()):
            label_item = self.data_table.item(row, 0)
            value_item = self.data_table.item(row, 1)
            if label_item and value_item:
                table_data[label_item.text()] = value_item.text()
            elif label_item:
                table_data[label_item.text()] = ""
        if not table_data:
            self.log_message("No valid data extracted from table to save.", "WARNING")
            QMessageBox.warning(self, "No Data", "Could not extract valid data from the table.")
            return
        suggested_filename = "overlay.pxt"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save PXT File", os.path.join(QDir.homePath(), suggested_filename), # Use os.path.join
            "PXT files (*.pxt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    for key, value in table_data.items():
                        f.write(f"{key}: {value}\n")
                    f.write("---\n")
                    f.write("End of Extracted Data\n")
                self.log_message(f"Table data successfully saved to: {file_path}", "INFO")
                QMessageBox.information(self, "Save Successful", f"Data saved to:\n{file_path}")
            except Exception as e:
                self.log_message(f"Error saving data to PXT file '{file_path}': {e}", "ERROR")
                QMessageBox.warning(self, "Save Failed", f"Could not save data to file:\n{e}")
        else:
            self.log_message("Save operation cancelled by user.", "INFO")

    def update_extracted_data_viewer(self, data_dict_to_display):
        if not hasattr(self, 'data_table'):
            self.log_message("Data table UI element not found.", "ERROR")
            return
        data_to_use = data_dict_to_display if data_dict_to_display is not None else self.extracted_data_cache
        if not data_to_use:
            self.data_table.setRowCount(0)
            self.log_message("No data to display in viewer.", "INFO")
            return
        self.data_table.setRowCount(0) # Clear previous items
        self.data_table.setRowCount(len(data_to_use))
        row = 0
        for key, value in data_to_use.items():
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value) if value is not None else "")
            key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable) # Make key non-editable
            self.data_table.setItem(row, 0, key_item)
            self.data_table.setItem(row, 1, value_item)
            row += 1
        self.log_message(f"Displayed {len(data_to_use)} items in Extracted Data Viewer.", "INFO")
        if hasattr(self, 'data_viewer_tab'): # Check if tab exists
            self.tab_widget.setCurrentWidget(self.data_viewer_tab)

    def _show_about_dialog(self):
        QMessageBox.about(
            self, "About Contract Processing Application",
            "<b>Contract Processing Application Shell</b><br><br>"
            "Version 0.1 (GUI Shell)<br>"
            "Built with PyQt6.<br><br>"
            "This application is a front-end for processing contracts."
        )

    def _toggle_setup_docs_options(self, checked: bool):
        if hasattr(self, 'setup_docs_options_group'):
            self.setup_docs_options_group.setVisible(checked)
            self.log_message(f"Setup Docs Options visibility toggled to: {checked}", "DEBUG")
        else:
            self.log_message("setup_docs_options_group not found on main window.", "ERROR")

    # --- Radio Button and Checkbox Logic ---
    def _update_seller_checkbox_based_on_refi(self):
        """
        Updates the Seller checkbox state based on whether Refi is selected.
        If Refi is selected, Seller is unchecked and disabled.
        If Purchase is selected, Seller is enabled (its checked state is preserved).
        """
        if not hasattr(self, 'rb_refi') or not hasattr(self, 'chk_seller'):
            self.log_message("Cannot update seller checkbox: rb_refi or chk_seller missing.", "ERROR")
            return

        is_refi_selected = self.rb_refi.isChecked()

        if is_refi_selected:
            if self.chk_seller.isChecked(): # Only log if state changes
                self.log_message("Refi selected: Unchecking Seller.", "DEBUG")
            self.chk_seller.setChecked(False)
            if self.chk_seller.isEnabled(): # Only log if state changes
                self.log_message("Refi selected: Disabling Seller checkbox.", "DEBUG")
            self.chk_seller.setEnabled(False)
        else: # Purchase is selected
            if not self.chk_seller.isEnabled(): # Only log if state changes
                self.log_message("Purchase selected: Enabling Seller checkbox.", "DEBUG")
            self.chk_seller.setEnabled(True)
            # The user's previous selection for chk_seller (when Purchase was active) is maintained.

    # The following methods are now OBSOLETE if QButtonGroup is used correctly
    # for rb_purchase/rb_refi and rb_cd/rb_hud in create_processing_tab.
    # QButtonGroup handles mutual exclusivity automatically.
    # The only logic needed for Purchase/Refi is to update the chk_seller,
    # which is handled by connecting rb_refi.toggled to _update_seller_checkbox_based_on_refi.

    # def _handle_refi_selection(self): # OBSOLETE
    #     # ... (This logic is now in _update_seller_checkbox_based_on_refi) ...
    #     pass

    # def _handle_cd_hud_selection(self, toggled_button): # OBSOLETE
    #     # ... (Mutual exclusivity handled by QButtonGroup) ...
    #     pass

    # def _handle_purchase_refi_selection(self, toggled_button): # OBSOLETE
    #     # ... (Mutual exclusivity handled by QButtonGroup, chk_seller by _update_seller_checkbox_based_on_refi) ...
    #     pass

    def log_message(self, message, level="INFO"):
        if level == "DEBUG" and not os.getenv("APP_DEBUG_MODE", False): # Check if APP_DEBUG_MODE is True-like
            return
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        self.log_area.append(formatted_message)
        if level == "INFO":
            self.status_label.setText(message[:100]) # Truncate for status bar
        elif level in ("WARNING", "ERROR"):
             self.status_label.setText(f"{level}: {message[:100]}")

    def show_warning(self, message):
        QMessageBox.warning(self, "Warning", message)

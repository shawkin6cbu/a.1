from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt 
# Other imports like QFileDialog, QMessageBox etc. are handled by main_window_instance methods.

# --- Import functions from processing_logic.py ---
from processing_logic import get_all_legacy_contract_field_names # Added import


def create_data_viewer_tab(main_window_instance):
    data_viewer_tab = QWidget()
    layout = QVBoxLayout(data_viewer_tab)
    layout.setSpacing(10)

    main_window_instance.data_table = QTableWidget()
    main_window_instance.data_table.setColumnCount(2)
    main_window_instance.data_table.setHorizontalHeaderLabels(["Label", "Value"])
    main_window_instance.data_table.horizontalHeader().setStretchLastSection(True)
    main_window_instance.data_table.setAlternatingRowColors(True) # QSS can also control this via ::alternate
    
    # Get all possible field names from processing_logic
    all_field_names = get_all_legacy_contract_field_names()
    
    main_window_instance.data_table.setRowCount(len(all_field_names))
    
    for row, label_text in enumerate(all_field_names):
        label_item = QTableWidgetItem(label_text)
        label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable) # Make label not editable
        
        value_item = QTableWidgetItem("") # Empty value
        # Value items are editable by default, no need to change flags unless explicitly making them non-editable
        
        main_window_instance.data_table.setItem(row, 0, label_item)
        main_window_instance.data_table.setItem(row, 1, value_item)
        
    layout.addWidget(main_window_instance.data_table)

    buttons_layout = QHBoxLayout()
    buttons_layout.addStretch(1)

    main_window_instance.btn_save_changes = QPushButton("Save Changes")
    main_window_instance.btn_save_changes.setEnabled(True) # Enable the button
    main_window_instance.btn_save_changes.setToolTip("Save the current table data to a .pxt file.")
    main_window_instance.btn_save_changes.clicked.connect(main_window_instance._save_table_data_to_pxt) # Connect to new method
    # main_window_instance.btn_save_changes.setStyleSheet(...) # REMOVED

    buttons_layout.addWidget(main_window_instance.btn_save_changes)
    layout.addLayout(buttons_layout)
    
    return data_viewer_tab

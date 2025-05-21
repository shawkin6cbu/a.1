import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QTabWidget, QComboBox, QGroupBox, QCheckBox, QLabel, QListWidget,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QTextEdit,
    QStatusBar, QProgressBar, QFileDialog, QMessageBox, QSizePolicy,
    QSpacerItem, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QDir, QTimer, QDateTime, QAbstractItemModel
from PyQt6.QtGui import QAction, QPalette, QColor

# Optional: Set a modern style
try:
    from PyQt6.QtSvgWidgets import QSvgWidget
    from PyQt6.QtSvg import QSvgRenderer
except ImportError:
    QSvgWidget = None
    QSvgRenderer = None
    # print("PyQt6.QtSvg or PyQt6.QtSvgWidgets not found, some icons might not load if they were SVGs.")


# ==============================================================================
# SECTION 1: STYLESHEET DEFINITION
# ==============================================================================


modern_stylesheet = r"""
    /* Global settings for a more modern feel - adjust colors to your theme */
    QWidget {
        background-color: #202124; /* Main dark background - like Google's dark theme */
        color: #e8eaed;            /* Light text color */
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif; /* Modern font stack */
        font-size: 12pt;
    }

    /* --- QTabWidget and QTabBar Styling (Google AI Studio like) --- */
    QTabWidget::pane {
        border: none; 
        background-color: #202124; 
    }
    QTabBar {
        border-bottom: 1px solid #3c4043; 
        background-color: #202124; 
    }
    QTabBar::tab {
        background-color: transparent; 
        color: #bdc1c6;               
        padding: 10px 18px;          
        margin-right: 1px;           
        border: none;                
        min-width: 100px;            
    }
    QTabBar::tab:selected {
        color: #8ab4f8;               
        border-bottom: 2px solid #8ab4f8; 
        background-color: transparent;    
    }
    QTabBar::tab:!selected:hover {
        color: #e8eaed;               
        background-color: #2d2e31;    
    }
    QTabBar::tab:selected:hover {}

    /* --- Rounded and Softer Controls --- */
    QPushButton {
        background-color: #3c4043; 
        color: #e8eaed;
        border: 1px solid #5f6368;
        padding: 8px 16px;
        border-radius: 18px;       
        min-height: 20px;          
    }
    QPushButton:hover {
        background-color: #4a4d50;
        border-color: #70757a;
    }
    QPushButton:pressed {
        background-color: #565a5d;
    }
    QPushButton:disabled {
        background-color: #2a2b2d;
        color: #5f6368;
        border-color: #3c4043;
    }
      QPushButton#startProcessingButton {
        background-color: #8ab4f8; /* Your theme's primary accent blue */
        color: #202124;              /* Dark text for contrast on this lighter blue, 
                                        or use white if you prefer and it's readable.
                                        Your QComboBox selected item uses #202124 text on this blue. */
        font-weight: bold;
        border: none;              /* Keep it borderless for a modern flat look */
        padding: 10px 20px;
        border-radius: 18px;       /* Keep your existing rounding */
    }
    QPushButton#startProcessingButton:hover {
        background-color: #7da0e1;
    }
    QPushButton#startProcessingButton:pressed {
        background-color: #6f8ccf;                             
    }

    QLineEdit, QComboBox {
        background-color: #2d2e31;
        border: 1px solid #5f6368;
        padding: 6px 10px;
        border-radius: 4px; 
        color: #e8eaed;
    }
    QLineEdit:focus, QComboBox:focus {
        border-color: #8ab4f8; 
    }
    QComboBox::drop-down {
        border: none;
        background-color: transparent;
        width: 20px;
        padding-right: 5px; 
    }
    QComboBox::down-arrow {
        image: url(dropdown.png); 
        width: 12px;              
        height: 12px;            
    }

    /* --- QComboBox Dropdown List Styling --- */
    QComboBox QAbstractItemView { 
        background-color: #2d2e31;    
        border: 1px solid #5f6368;    
        color: #e8eaed;               
        padding: 4px;                 
        outline: 0px;                 
        border-radius: 4px;           
    }

    QComboBox QAbstractItemView::item {
        padding: 5px 8px;             
        background-color: transparent;
        
        /* Using a transparent border by default to reserve space */
        border: 1px solid transparent; 
        /* border-radius: 3px; */ /* Temporarily commented for simpler debugging */
        
        color: #e8eaed;               
        min-height: 20px;             
        outline: none; /* Ensure no native outline interferes */
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #8ab4f8;;  /* This part seems to work (background changes) */
        
        /* --- DEBUGGING BORDER --- */
        /* Try a very obvious border to see if *any* border change is applied */
        border: 3px solid red !important; 
        /* If red border appears, the issue is with the blue color's visibility or subtle conflict. */
        /* If red border does NOT appear, the issue is more fundamental with applying border to item:hover. */
        
        /* Original intended style (once red border test is done): */
        /* border: 1px solid #8ab4f8; */
        /* border-radius: 3px; */ /* Restore if previously commented out */
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #8ab4f8;      
        color: #202124;                   
        border: 1px solid #8ab4f8; 
        /* border-radius: 3px; */ /* Restore if base item has it */
    }
    /* --- End QComboBox Dropdown List Styling --- */

    QGroupBox {
        background-color: #2d2e31; 
        border: 1px solid #3c4043;
        border-radius: 8px;
        margin-top: 10px; 
        padding: 10px;
        padding-top: 20px; 
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px; 
        margin-left: 10px; 
        color: #e8eaed;
        font-weight: bold;
        background-color: #2d2e31; 
    }

    QCheckBox {
        spacing: 8px; 
        color: #e8eaed;
        padding: 4px 0;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 1px solid #5f6368;
        border-radius: 3px;
        background-color: #3c4043;
    }
    QCheckBox::indicator:hover {
        border-color: #70757a;
    }
    QCheckBox::indicator:checked {
        background-color: #8ab4f8; 
        border-color: #8ab4f8;
        /* image: url(:/icons/checkmark_white.svg); */
    }
    QCheckBox::indicator:disabled {
        border-color: #3c4043;
        background-color: #2a2b2d;
    }

    QListWidget {
        background-color: #2d2e31;
        border: 1px solid #5f6368;
        border-radius: 4px;
        color: #e8eaed;
        padding: 4px; 
    }
    QListWidget::item {
        padding: 5px; 
        border-radius: 3px; 
        border: 1px solid transparent; 
    }
    QListWidget::item:selected {
        background-color: #8ab4f8; 
        color: #202124;      
        border: 1px solid #8ab4f8;
    }
    QListWidget::item:hover:!selected {
        background-color: #3c4043;
        border: 1px solid #3c4043; 
    }
    PDFListWidget#functionalPdfDropArea { /* Target PDFListWidget by class and object name */
    background-color: #2a2b2d;
    border: 2px dashed #5f6368;
    border-radius: 6px;
    /* Padding here will affect the content area *inside* the border.
       The placeholder text drawn in paintEvent will be centered within this padded area.
       Adjust padding as needed for item display and placeholder text appearance. */
    padding: 5px; /* Example padding, adjust as you see fit */
    }

    /* Optional: Style for items within this specific list widget if needed */
    PDFListWidget#functionalPdfDropArea::item {
        color: #e8eaed; /* Your default text color for items */
        padding: 3px; /* Padding for individual items */
    }

    PDFListWidget#functionalPdfDropArea::item:selected {
        background-color: #8ab4f8; /* Your selection color */
        color: #202124;      
    }
     QPushButton#selectOutputDirectoryButton {
        background-color: #8ab4f8; /* accent blue */
        color: #202124;              /*  text */
       
        font-weight: bold;       
        border: none;            
        padding: 8px 16px;         
        border-radius: 18px;       
        min-height: 20px;          
    }
    QPushButton#selectOutputDirectoryButton:hover {
        background-color: #7da0e1; /* Slightly darker blue for hover */
    }
    QPushButton#selectOutputDirectoryButton:pressed {
        background-color: #6f8ccf; /* Even darker blue for pressed */
    }

    QScrollBar:vertical {
        border: none; background: #2d2e31; width: 10px; margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #5f6368; min-height: 20px; border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover { background: #70757a; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px; background: transparent;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: transparent;
    }
    QScrollBar:horizontal {
        border: none; background: #2d2e31; height: 10px; margin: 0px;
    }
    QScrollBar::handle:horizontal {
        background: #5f6368; min-width: 20px; border-radius: 5px;
    }
    QScrollBar::handle:horizontal:hover { background: #70757a; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px; background: transparent;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: transparent;
    }

    QTextEdit { 
        background-color: #2d2e31;
        border: 1px solid #5f6368;
        border-radius: 4px;
        color: #dadce0; 
        font-family: "Consolas", "Menlo", "Courier New", monospace;
        padding: 5px;
    }
    QStatusBar {
        background-color: #202124; 
        color: #bdc1c6;
        border-top: 1px solid #3c4043; 
    }
    QProgressBar {
        border: 1px solid #5f6368; border-radius: 4px; text-align: center;
        background-color: #3c4043; color: #e8eaed; padding: 1px; 
    }
    QProgressBar::chunk {
        background-color: #8ab4f8; border-radius: 3px; margin: 1px; 
    }
    QMenuBar {
        background-color: #2d2e31; color: #e8eaed; border-bottom: 1px solid #3c4043;
    }
    QMenuBar::item { background-color: transparent; padding: 6px 12px; }
    QMenuBar::item:selected { background-color: #3c4043; }
    QMenu {
        background-color: #2d2e31; color: #e8eaed; border: 1px solid #5f6368;
        padding: 5px; border-radius: 4px; 
    }
    QMenu::item { padding: 8px 24px 8px 12px; background-color: transparent; border-radius: 3px; }
    QMenu::item:selected { background-color: #8ab4f8; color: #202124; }
    QMenu::separator { height: 1px; background-color: #3c4043; margin: 5px 0px; }

    QTableWidget {
        background-color: #2d2e31; border: 1px solid #3c4043; gridline-color: #3c4043; 
        color: #e8eaed; border-radius: 4px;
    }
    QHeaderView::section { 
        background-color: #3c4043; color: #e8eaed; padding: 6px;
        border: 1px solid #2d2e31; font-weight: bold;
    }
    QTableWidget::item {
        padding: 5px; border-bottom: 1px solid #3c4043; border-right: 1px solid #3c4043;  
    }
    QTableWidget::item:selected { background-color: #8ab4f8; color: #202124; }
"""


# ==============================================================================
# SECTION 2: CLASS DEFINITIONS (e.g., PDFListWidget, ContractProcessorApp)
# ==============================================================================


class PDFListWidget(QListWidget):
    files_added = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        # REMOVED inline stylesheet - let global QSS handle it
        # self.setStyleSheet("""...""")

    # Ensure this method is correctly indented as part of the class
    def _replace_current_pdf(self, new_file_path):
        """Helper to clear and add the new PDF."""
        self.clear()
        self.addItem(new_file_path)
        self.files_added.emit([new_file_path])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # Check if any of the URLs are PDF files
            # We only need to know if *at least one* is a PDF to accept the enter
            is_pdf_present = any(url.toLocalFile().lower().endswith('.pdf')
                                 for url in event.mimeData().urls())
            if is_pdf_present:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # If dragEnterEvent accepted, dragMove can usually just accept too.
        # More specific checks can be done if needed (e.g., based on mouse position over sub-elements)
        if event.mimeData().hasUrls(): # Basic check is good
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction) # Set the action
            event.acceptProposedAction() # Explicitly accept

            new_pdf_path = None
            # Find the first valid PDF path from the dropped URLs
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.pdf'):
                    new_pdf_path = file_path
                    break # We only care about the first PDF for swapping

            if new_pdf_path:
                self._replace_current_pdf(new_pdf_path) # Use the helper
            # If no valid PDF was dropped, we do nothing, the event was accepted but no action taken on list
        # If mimeData doesn't have URLs, the event is implicitly ignored by not being handled.

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def add_pdfs_dialog(self):
        # No need to ask for confirmation here if the behavior is always to replace
        # The user is explicitly choosing a new file.

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF File",
            QDir.homePath(),
            "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path: # If a file was selected
            self._replace_current_pdf(file_path) # Use the helper
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF File",
            QDir.homePath(),
            "PDF Files (*.pdf);;All Files (*)"
        )

        if file_path: # If a file was selected
            self._replace_current_pdf(file_path)




class ContractProcessorApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Contract Processing Application")
        self.setGeometry(100, 100, 900, 700)

        QApplication.setStyle("Fusion") # Keep Fusion as a base

        # self.setup_modern_palette() # REMOVED - QSS handles this now

        self.init_ui() # This will now create widgets that get styled by the global QSS
        self.log_message("Application initialized. Ready.")

    # def setup_modern_palette(self): # ENTIRE METHOD REMOVED
    #     pass

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        # Margins and spacing can also be controlled by QSS on QWidget or specific layouts if desired
        # For now, keeping these explicit calls is fine.
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self._create_menu_bar()

        self.tab_widget = QTabWidget()
        # self.tab_widget.setStyleSheet("QTabBar::tab { min-width: 150px; padding: 8px; }") # REMOVED - Handled by global QSS

        self.processing_tab = QWidget()
        self.data_viewer_tab = QWidget()

        self.tab_widget.addTab(self.processing_tab, "Processing Controls")
        self.tab_widget.addTab(self.data_viewer_tab, "Extracted Data Viewer")

        self._create_processing_controls_tab()
        self._create_data_viewer_tab()

        main_layout.addWidget(self.tab_widget)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(100) # Fixed height for the log area
        # self.log_area.setStyleSheet(...) # REMOVED - Handled by global QSS
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
        menu_bar = self.menuBar() # QMainWindow has menuBar() method

        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close) # QMainWindow has close()
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about_dialog) # Assuming _show_about_dialog exists
        help_menu.addAction(about_action)

    def _create_processing_controls_tab(self):
        layout = QVBoxLayout(self.processing_tab)
        layout.setSpacing(15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.contract_type_combo = QComboBox()
        self.contract_type_combo.setPlaceholderText("Select or type contract type...")
        self.contract_type_combo.setEditable(False)
        self.contract_type_combo.addItems(["Legacy", "MS Assoc. of Realtors", "Other"])
        self.contract_type_combo.setToolTip("Select the type of contract being processed.")
        form_layout.addRow(QLabel("Contract Type:"), self.contract_type_combo)
        layout.addLayout(form_layout)

        self.output_options_group = QGroupBox("Desired Outputs")
        output_options_layout = QVBoxLayout()

        self.chk_generate_file_label = QCheckBox("Generate File Label")
        self.chk_generate_setup_docs = QCheckBox("Generate Setup Documents")
        self.chk_generate_file_label.setChecked(True)
        self.chk_generate_setup_docs.setChecked(True)

        output_options_layout.addWidget(self.chk_generate_file_label)
        output_options_layout.addWidget(self.chk_generate_setup_docs)
        self.output_options_group.setLayout(output_options_layout)
        layout.addWidget(self.output_options_group)

        # === MODIFIED PDF Input Section ===
        pdf_input_group = QGroupBox("PDF Input")
        pdf_input_layout = QVBoxLayout()

        # REMOVE the old QLabel for "Drop .pdf here"
        # self.pdf_drop_label = QLabel("Drop .pdf here")
        # self.pdf_drop_label.setObjectName("pdfDropLabel")
        # self.pdf_drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.pdf_drop_label.setToolTip("Click the list area to open file dialog or drag PDF files onto the list.")

        self.pdf_list_widget = PDFListWidget()
        self.pdf_list_widget.setObjectName("functionalPdfDropArea") # *** SET OBJECT NAME HERE ***
        self.pdf_list_widget.setMinimumHeight(100) # Adjust as needed
        # The tooltip is now more relevant on the list widget itself
        self.pdf_list_widget.setToolTip("Drag and drop a PDF file here, or click the empty area to select a file.")
        self.pdf_list_widget.files_added.connect(lambda files: self.log_message(f"Added PDFs: {', '.join(files)}"))

        # pdf_input_layout.addWidget(self.pdf_drop_label) # REMOVE THIS LINE
        pdf_input_layout.addWidget(self.pdf_list_widget) # Add only the functional list widget
        pdf_input_group.setLayout(pdf_input_layout)
        layout.addWidget(pdf_input_group)
        # === End MODIFIED PDF Input Section ===

        output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel("Output Directory:")
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Select directory...")
        self.output_dir_edit.setReadOnly(False)
        
        self.btn_select_output_dir = QPushButton("Select Output Directory")
        self.btn_select_output_dir.setObjectName("selectOutputDirectoryButton")
        self.btn_select_output_dir.clicked.connect(self._select_output_directory)

        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.output_dir_edit, 1)
        output_dir_layout.addWidget(self.btn_select_output_dir)
        layout.addLayout(output_dir_layout)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.btn_start_processing = QPushButton("Start Processing")
        self.btn_start_processing.setObjectName("startProcessingButton")
        self.btn_start_processing.clicked.connect(self._start_processing_placeholder)
        layout.addWidget(self.btn_start_processing, 0, Qt.AlignmentFlag.AlignCenter)

    def _create_data_viewer_tab(self):
        layout = QVBoxLayout(self.data_viewer_tab)
        layout.setSpacing(10)

        self.data_table = QTableWidget()
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["Label", "Value"])
        self.data_table.horizontalHeader().setStretchLastSection(True)
        self.data_table.setAlternatingRowColors(True) # QSS can also control this via ::alternate
        # self.data_table.setStyleSheet(...) # REMOVED - Handled by global QSS
        layout.addWidget(self.data_table)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)

        self.btn_save_changes = QPushButton("Save Changes")
        self.btn_save_changes.setEnabled(False)
        self.btn_save_changes.setToolTip("Save any edited values in the table (Not Implemented).")
        # self.btn_save_changes.setStyleSheet(...) # REMOVED

        self.btn_export_data = QPushButton("Export Data")
        self.btn_export_data.setEnabled(False)
        self.btn_export_data.setToolTip("Export the displayed data to a file (Not Implemented).")
        # self.btn_export_data.setStyleSheet(...) # REMOVED

        buttons_layout.addWidget(self.btn_save_changes)
        buttons_layout.addWidget(self.btn_export_data)
        layout.addLayout(buttons_layout)

    def _select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_dir_edit.text() or QDir.homePath()
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)
            self.log_message(f"Output directory selected: {dir_path}")

    def _start_processing_placeholder(self):
        contract_type = self.contract_type_combo.currentText()
        generate_label = self.chk_generate_file_label.isChecked()
        generate_docs = self.chk_generate_setup_docs.isChecked()
        pdfs = [self.pdf_list_widget.item(i).text() for i in range(self.pdf_list_widget.count())]
        output_dir = self.output_dir_edit.text()
        single_pdf_file = None
        if self.pdf_list_widget.count() > 0:
            single_pdf_file = self.pdf_list_widget.item(0).text()

        if not single_pdf_file:
            self.show_warning("No PDF file selected.")
            self.log_message("Processing attempted with no PDF.", "WARNING")
            return
        if not pdfs:
            self.show_warning("No PDF files selected.")
            self.log_message("Processing attempted with no PDFs.", "WARNING")
            return
        if not output_dir:
            self.show_warning("Output directory not selected.")
            self.log_message("Processing attempted with no output directory.", "WARNING")
            return
        if not contract_type:
            self.show_warning("No contract type selected.")
            self.log_message("Processing attempted with no contract type selected.", "WARNING")
            return

        self.log_message(f"Starting processing (placeholder)...")
        self.log_message(f"  Contract Type: {contract_type}")
        self.log_message(f"  Generate Label: {generate_label}")
        self.log_message(f"  Generate Docs: {generate_docs}")
        self.log_message(f"  PDFs: {len(pdfs)} file(s)")
        self.log_message(f"  Output Dir: {output_dir}")
        self.log_message(f"Starting processing for contract type: {contract_type}...")
        self.log_message(f"  PDF: {single_pdf_file}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0,100)
        self.status_label.setText(f"Processing {contract_type}...")

        if contract_type == "Legacy":
            from processing_logic import handle_legacy_contract_processing # Ensure this import is correct

            # IMPORTANT: For real application, run this in a QThread
            # For now, direct call:
            created_path, message, extracted_data_dict = handle_legacy_contract_processing([single_pdf_file], output_dir)

            if created_path and extracted_data_dict:
                self.log_message(f"SUCCESS (Legacy): {message}", "INFO")
                QMessageBox.information(self, "Processing Complete", f"Legacy contract structure created at:\n{created_path}")
                self.update_extracted_data_viewer(extracted_data_dict) # <--- NEW CALL
            else:
                self.log_message(f"ERROR (Legacy): {message}", "ERROR")
                self.show_warning(f"Legacy processing failed: {message}")
                if extracted_data_dict: # Show partial data if any was extracted before failure
                    self.update_extracted_data_viewer(extracted_data_dict)

        else:
            self.log_message(f"Processing logic for '{contract_type}' is not yet implemented.", "WARNING")
            QMessageBox.information(self, "Processing", f"Placeholder processing for {contract_type} complete!")
            self.data_table.setRowCount(0) # Clear table for non-legacy types for now

        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Processing finished.")

    def update_extracted_data_viewer(self, data_dict):
        """
        Populates the QTableWidget in the 'Extracted Data Viewer' tab.
        """
        if not data_dict:
            self.data_table.setRowCount(0) # Clear table if no data
            self.log_message("No data to display in viewer.", "INFO")
            return

        self.data_table.setRowCount(0) # Clear previous data
        self.data_table.setRowCount(len(data_dict))

        row = 0
        for key, value in data_dict.items():
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value) if value is not None else "") # Handle None values

            # Make items non-editable for now, but selectable
            key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable) # For future editing, change this

            self.data_table.setItem(row, 0, key_item)
            self.data_table.setItem(row, 1, value_item)
            row += 1
        
        self.log_message(f"Displayed {len(data_dict)} items in Extracted Data Viewer.", "INFO")
        self.tab_widget.setCurrentWidget(self.data_viewer_tab) # Switch to the data viewer tab

    def _update_progress_simulation(self):
        self.current_progress += 10
        self.progress_bar.setValue(self.current_progress)
        if self.current_progress >= 100:
            self.timer.stop()
            self.log_message("Processing finished (placeholder).")
            self.progress_bar.setVisible(False)
            QMessageBox.information(self, "Processing", "Placeholder processing complete!")


    def _show_about_dialog(self): # Make sure this exists if called by the menu
        QMessageBox.about(
            self,
            "About Contract Processing Application",
            "<b>Contract Processing Application Shell</b><br><br>"
            "Version 0.1 (GUI Shell)<br>"
            "Built with PyQt6.<br><br>"
            "This application is a front-end for processing contracts. "
        )

    def log_message(self, message, level="INFO"):
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        self.log_area.append(formatted_message)
        if level == "INFO":
            self.status_label.setText(message[:100])
        elif level in ("WARNING", "ERROR"):
             self.status_label.setText(f"{level}: {message[:100]}")

    def show_warning(self, message):
        QMessageBox.warning(self, "Warning", message)

    


# ==============================================================================
# SECTION 3: MAIN EXECUTION BLOCK
# ==============================================================================


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # --- APPLY THE STYLESHEET TO THE ENTIRE APPLICATION ---
    # This should be done AFTER creating QApplication and BEFORE creating your main window
    app.setStyleSheet(modern_stylesheet) # <------------------- HERE

    # --- Optional: Create standard directories (example call) ---
    # (You can keep or remove this block based on your preference for handling directory creation)
    #root_dir_to_setup = r"C:\Users\shawk\Desktop\a.1"
    #if not os.path.exists(os.path.join(root_dir_to_setup, "Logs")):
    #    reply = QMessageBox.question(None, 'Application Setup',
    #                                 f"Standard folders might be missing in:\n{root_dir_to_setup}\nCreate them?",
    #                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    #                                 QMessageBox.StandardButton.Yes)
    #    if reply == QMessageBox.StandardButton.Yes:
    #        if create_standard_dirs(root_dir_to_setup):
    #            QMessageBox.information(None, "Setup Complete", f"Standard directories created/verified.")
    #        else:
    #            QMessageBox.warning(None, "Setup Issue", f"Could not create all standard directories.")
    # --- End of optional directory creation ---

    main_window = ContractProcessorApp()
    main_window.show()
    sys.exit(app.exec())
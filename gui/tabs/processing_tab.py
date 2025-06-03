from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QCheckBox, QLabel, QPushButton, QLineEdit,
    QRadioButton,  # Added QRadioButton
    QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
# Note: QComboBox is not directly used here, CustomComboBox is.
# QListWidget is not directly used, PDFListWidget is.
# Other imports like QFileDialog, QMessageBox etc. are handled by main_window_instance methods.

# --- Import custom widgets ---
from gui.widgets import CustomComboBox, PDFListWidget


def create_processing_tab(main_window_instance):
    processing_tab = QWidget()
    layout = QVBoxLayout(processing_tab)
    layout.setSpacing(15)

    form_layout = QFormLayout()
    form_layout.setSpacing(10)
    form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

    # *** CHANGED: Use CustomComboBox instead of QComboBox ***
    main_window_instance.contract_type_combo = CustomComboBox()
    main_window_instance.contract_type_combo.setPlaceholderText("Select or type contract type...")
    main_window_instance.contract_type_combo.setEditable(False)
    main_window_instance.contract_type_combo.addItems(["Legacy", "MS Assoc. of Realtors", "Other"])
    main_window_instance.contract_type_combo.setCurrentText("Legacy")
    main_window_instance.contract_type_combo.setToolTip("Select the type of contract being processed.")
    form_layout.addRow(QLabel("Contract Type:"), main_window_instance.contract_type_combo)
    layout.addLayout(form_layout)

    # Output directory line edit (created before connecting the signal)
    main_window_instance.output_dir_edit = QLineEdit() # Ensure output_dir_edit is created
    main_window_instance.output_dir_edit.setPlaceholderText("Select directory...")
    main_window_instance.output_dir_edit.setReadOnly(False)
    main_window_instance.output_dir_edit.setText("C:/Closings/Legacy Seller") # Set default output dir

    # Connect signal for contract type change
    main_window_instance.contract_type_combo.currentTextChanged.connect(main_window_instance._update_output_directory_for_contract_type)

    main_window_instance.output_options_group = QGroupBox("Desired Outputs")
    output_options_layout = QVBoxLayout()

    main_window_instance.chk_generate_file_label = QCheckBox("Generate File Label")
    main_window_instance.chk_generate_setup_docs = QCheckBox("Generate Setup Documents")
    main_window_instance.chk_generate_file_label.setChecked(True)
    main_window_instance.chk_generate_setup_docs.setChecked(True)

    # Connect signal for chk_generate_setup_docs
    main_window_instance.chk_generate_setup_docs.toggled.connect(main_window_instance._toggle_setup_docs_options)

    output_options_layout.addWidget(main_window_instance.chk_generate_file_label)
    output_options_layout.addWidget(main_window_instance.chk_generate_setup_docs)
    main_window_instance.output_options_group.setLayout(output_options_layout)
    layout.addWidget(main_window_instance.output_options_group)

    # --- Setup Docs Options Group ---
    main_window_instance.setup_docs_options_group = QGroupBox("Setup Docs Options")
    setup_docs_options_layout = QVBoxLayout()

    # Purchase/Refi Radio Buttons
    main_window_instance.rb_purchase = QRadioButton("Purchase")
    main_window_instance.rb_purchase.setChecked(True)
    main_window_instance.rb_refi = QRadioButton("Refi")

    # Connect signal for rb_refi
    main_window_instance.rb_refi.toggled.connect(main_window_instance._handle_refi_selection)

    purchase_refi_layout = QHBoxLayout()
    purchase_refi_layout.addWidget(main_window_instance.rb_purchase)
    purchase_refi_layout.addWidget(main_window_instance.rb_refi)
    setup_docs_options_layout.addLayout(purchase_refi_layout)

    # Buyer/Seller Checkboxes
    main_window_instance.chk_buyer = QCheckBox("Buyer")
    main_window_instance.chk_buyer.setChecked(True)
    main_window_instance.chk_seller = QCheckBox("Seller")
    main_window_instance.chk_seller.setChecked(True)

    buyer_seller_layout = QHBoxLayout()
    buyer_seller_layout.addWidget(main_window_instance.chk_buyer)
    buyer_seller_layout.addWidget(main_window_instance.chk_seller)
    setup_docs_options_layout.addLayout(buyer_seller_layout)

    # CD/HUD Radio Buttons
    main_window_instance.rb_cd = QRadioButton("CD")
    main_window_instance.rb_cd.setChecked(True)
    main_window_instance.rb_hud = QRadioButton("HUD")

    cd_hud_layout = QHBoxLayout()
    cd_hud_layout.addWidget(main_window_instance.rb_cd)
    cd_hud_layout.addWidget(main_window_instance.rb_hud)
    setup_docs_options_layout.addLayout(cd_hud_layout)

    main_window_instance.setup_docs_options_group.setLayout(setup_docs_options_layout)
    main_window_instance.setup_docs_options_group.setVisible(False) # Initially hidden
    layout.addWidget(main_window_instance.setup_docs_options_group)
    # --- End Setup Docs Options Group ---

    # === MODIFIED PDF Input Section ===
    pdf_input_group = QGroupBox("PDF Input")
    pdf_input_layout = QVBoxLayout()

    main_window_instance.pdf_list_widget = PDFListWidget()
    main_window_instance.pdf_list_widget.setObjectName("functionalPdfDropArea") # *** SET OBJECT NAME HERE ***
    main_window_instance.pdf_list_widget.setMinimumHeight(100) # Adjust as needed
    # The tooltip is now more relevant on the list widget itself
    main_window_instance.pdf_list_widget.setToolTip("Drag and drop a PDF file here, or click the empty area to select a file.")
    main_window_instance.pdf_list_widget.files_added.connect(lambda files: main_window_instance.log_message(f"Added PDFs: {', '.join(files)}"))

    pdf_input_layout.addWidget(main_window_instance.pdf_list_widget) # Add only the functional list widget
    pdf_input_group.setLayout(pdf_input_layout)
    layout.addWidget(pdf_input_group)
    # === End MODIFIED PDF Input Section ===

    output_dir_layout = QHBoxLayout()
    main_window_instance.output_dir_label = QLabel("Output Directory:")
    # main_window_instance.output_dir_edit is already created and default set above
    
    main_window_instance.btn_select_output_dir = QPushButton("Select Output Directory")
    main_window_instance.btn_select_output_dir.setObjectName("selectOutputDirectoryButton")
    main_window_instance.btn_select_output_dir.clicked.connect(main_window_instance._select_output_directory)

    output_dir_layout.addWidget(main_window_instance.output_dir_label)
    output_dir_layout.addWidget(main_window_instance.output_dir_edit, 1)
    output_dir_layout.addWidget(main_window_instance.btn_select_output_dir)
    layout.addLayout(output_dir_layout)

    layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    main_window_instance.btn_start_processing = QPushButton("Start Processing")
    main_window_instance.btn_start_processing.setObjectName("startProcessingButton")
    main_window_instance.btn_start_processing.clicked.connect(main_window_instance._start_processing_placeholder)
    layout.addWidget(main_window_instance.btn_start_processing, 0, Qt.AlignmentFlag.AlignCenter)
    
    return processing_tab

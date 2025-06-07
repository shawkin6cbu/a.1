from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QCheckBox, QLabel, QPushButton, QLineEdit,
    QRadioButton, QButtonGroup,
    QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt

from ..widgets import CustomComboBox, PDFListWidget


def create_processing_tab(main_window_instance):
    processing_tab = QWidget()
    layout = QVBoxLayout(processing_tab)
    layout.setSpacing(15)

    form_layout = QFormLayout()
    form_layout.setSpacing(10)
    form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

    main_window_instance.contract_type_combo = CustomComboBox()
    main_window_instance.contract_type_combo.setPlaceholderText("Select or type contract type...")
    main_window_instance.contract_type_combo.setEditable(False)
    main_window_instance.contract_type_combo.addItems(["Legacy", "MS Assoc. of Realtors", "Other"])
    main_window_instance.contract_type_combo.setCurrentText("Legacy")
    main_window_instance.contract_type_combo.setToolTip("Select the type of contract being processed.")
    form_layout.addRow(QLabel("Contract Type:"), main_window_instance.contract_type_combo)
    layout.addLayout(form_layout)

    main_window_instance.output_dir_edit = QLineEdit()
    main_window_instance.output_dir_edit.setPlaceholderText("Select directory...")
    main_window_instance.output_dir_edit.setReadOnly(False)
    main_window_instance.output_dir_edit.setText("C:/Closings/Legacy Seller")

    main_window_instance.contract_type_combo.currentTextChanged.connect(main_window_instance._update_output_directory_for_contract_type)

    main_window_instance.output_options_group = QGroupBox("Desired Outputs")
    output_options_layout = QVBoxLayout() # This will contain the checkboxes and the expanding options container

    main_window_instance.chk_generate_file_label = QCheckBox("Generate File Label")
    main_window_instance.chk_generate_setup_docs = QCheckBox("Generate Setup Documents")
    main_window_instance.chk_generate_file_label.setChecked(True)
    main_window_instance.chk_generate_setup_docs.setChecked(True) # Default to checked

    # Add the primary checkboxes to the layout first
    output_options_layout.addWidget(main_window_instance.chk_generate_file_label)
    output_options_layout.addWidget(main_window_instance.chk_generate_setup_docs)
    
    # --- Accordion Container for Setup Docs Options ---
    # This QWidget will hold all the options that expand/collapse
    main_window_instance.setup_docs_options_container = QWidget()
    # Use a QVBoxLayout for the container itself
    accordion_layout = QVBoxLayout(main_window_instance.setup_docs_options_container)
    # Set left margin for indentation, and remove others for tight fit
    accordion_layout.setContentsMargins(20, 5, 0, 5) # Indent from the left

    # --- Create the options and add them to the accordion_layout ---
    
    # Purchase/Refi Radio Buttons
    purchase_refi_group_layout = QHBoxLayout()
    main_window_instance.rb_purchase = QRadioButton("Purchase")
    main_window_instance.rb_refi = QRadioButton("Refi")
    # Group them for mutual exclusivity. The parent can be the container.
    main_window_instance.purchase_refi_button_group = QButtonGroup(main_window_instance.setup_docs_options_container)
    main_window_instance.purchase_refi_button_group.addButton(main_window_instance.rb_purchase)
    main_window_instance.purchase_refi_button_group.addButton(main_window_instance.rb_refi)
    main_window_instance.rb_purchase.setChecked(True)
    purchase_refi_group_layout.addWidget(main_window_instance.rb_purchase)
    purchase_refi_group_layout.addWidget(main_window_instance.rb_refi)
    accordion_layout.addLayout(purchase_refi_group_layout)

    # Buyer/Seller Checkboxes
    buyer_seller_layout = QHBoxLayout()
    main_window_instance.chk_buyer = QCheckBox("Buyer")
    main_window_instance.chk_buyer.setChecked(True)
    main_window_instance.chk_seller = QCheckBox("Seller")
    main_window_instance.chk_seller.setChecked(True)
    buyer_seller_layout.addWidget(main_window_instance.chk_buyer)
    buyer_seller_layout.addWidget(main_window_instance.chk_seller)
    accordion_layout.addLayout(buyer_seller_layout)

    # CD/HUD Radio Buttons
    cd_hud_layout = QHBoxLayout()
    main_window_instance.rb_cd = QRadioButton("CD")
    main_window_instance.rb_hud = QRadioButton("HUD")
    # Group them for mutual exclusivity
    main_window_instance.cd_hud_button_group = QButtonGroup(main_window_instance.setup_docs_options_container)
    main_window_instance.cd_hud_button_group.addButton(main_window_instance.rb_cd)
    main_window_instance.cd_hud_button_group.addButton(main_window_instance.rb_hud)
    main_window_instance.rb_cd.setChecked(True)
    cd_hud_layout.addWidget(main_window_instance.rb_cd)
    cd_hud_layout.addWidget(main_window_instance.rb_hud)
    accordion_layout.addLayout(cd_hud_layout)

    # Add the accordion container itself to the layout, right after the checkbox that controls it
    output_options_layout.addWidget(main_window_instance.setup_docs_options_container)
    
    main_window_instance.output_options_group.setLayout(output_options_layout)
    layout.addWidget(main_window_instance.output_options_group)

    # --- Connect signals and set initial states ---
    main_window_instance.chk_generate_setup_docs.toggled.connect(main_window_instance._toggle_setup_docs_options)
    main_window_instance.rb_refi.toggled.connect(main_window_instance._update_seller_checkbox_based_on_refi)
    
    # Set initial states after everything is created
    if hasattr(main_window_instance, 'rb_refi') and hasattr(main_window_instance, 'chk_seller'):
        main_window_instance._update_seller_checkbox_based_on_refi()
    if hasattr(main_window_instance, 'chk_generate_setup_docs') and hasattr(main_window_instance, '_toggle_setup_docs_options'):
        main_window_instance._toggle_setup_docs_options(main_window_instance.chk_generate_setup_docs.isChecked())
    
    # === PDF Input Section ===
    pdf_input_group = QGroupBox("PDF Input")
    pdf_input_layout = QVBoxLayout()
    main_window_instance.pdf_list_widget = PDFListWidget()
    main_window_instance.pdf_list_widget.setObjectName("functionalPdfDropArea")
    main_window_instance.pdf_list_widget.setMinimumHeight(100)
    main_window_instance.pdf_list_widget.setToolTip("Drag and drop a PDF file here, or click the empty area to select a file.")
    main_window_instance.pdf_list_widget.files_added.connect(lambda files: main_window_instance.log_message(f"Added PDFs: {', '.join(files)}"))
    pdf_input_layout.addWidget(main_window_instance.pdf_list_widget)
    pdf_input_group.setLayout(pdf_input_layout)
    layout.addWidget(pdf_input_group)

    # === Output Directory Section ===
    output_dir_outer_layout = QHBoxLayout()
    main_window_instance.output_dir_label = QLabel("Output Directory:")
    main_window_instance.btn_select_output_dir = QPushButton("Select Output Directory")
    main_window_instance.btn_select_output_dir.setObjectName("selectOutputDirectoryButton")
    main_window_instance.btn_select_output_dir.clicked.connect(main_window_instance._select_output_directory)
    output_dir_outer_layout.addWidget(main_window_instance.output_dir_label)
    output_dir_outer_layout.addWidget(main_window_instance.output_dir_edit, 1)
    output_dir_outer_layout.addWidget(main_window_instance.btn_select_output_dir)
    layout.addLayout(output_dir_outer_layout)

    layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    main_window_instance.btn_start_processing = QPushButton("Start Processing")
    main_window_instance.btn_start_processing.setObjectName("startProcessingButton")
    main_window_instance.btn_start_processing.clicked.connect(main_window_instance._start_processing_placeholder)
    layout.addWidget(main_window_instance.btn_start_processing, 0, Qt.AlignmentFlag.AlignCenter)
    
    return processing_tab
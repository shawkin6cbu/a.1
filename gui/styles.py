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
        background-color: transparent; /* Keep this transparent */
        border: 1px solid transparent; /* Border that will be 'overwritten' by hover's border */
        color: #e8eaed;
        min-height: 20px;
        outline: none;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #8ab4f8 !important;
        color: #202124 !important;
        border: 1px solid #8ab4f8 !important; /* Match background to make border seamless */
        outline: none !important;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #8ab4f8;
        color: #202124;
        border: 1px solid #8ab4f8; /* Border for selected item */
        /* border-radius: 3px; */
    }

    /* Custom QComboBox QListView styling for our CustomComboBox */
    QComboBox QListView {
        background-color: #2d2e31;
        border: 1px solid #5f6368;
        color: #e8eaed;
        outline: none;
        border-radius: 4px;
        padding: 0px;
        margin: 0px;
    }
    QComboBox QListView::item {
        padding: 6px 10px;
        border: none;
        color: #e8eaed;
        margin: 0px;
    }
    QComboBox QListView::item:hover {
        background-color: #4a4d50;
        color: #ffffff;
    }
    QComboBox QListView::item:selected {
        background-color: #8ab4f8;
        color: #202124;
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
        border-bottom: 1px solid #3c4043; border-right: 1px solid #3c4043;
        padding: 1px;
    }
    QTableWidget::item:selected, QTableWidget::item:focus {
        background-color: #8ab4f8;
        color: #202124;
    }
    /* Make the editor widget fill the cell properly */
    QTableWidget QLineEdit {
        background-color: #2d2e31;
        color: #e8eaed;
        border: none;
        margin: 0px;
        padding: 1px;
        font-size: 12pt;
    }
"""

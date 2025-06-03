from PyQt6.QtWidgets import QComboBox, QListWidget, QFileDialog, QListView
from PyQt6.QtCore import Qt, pyqtSignal, QDir

class CustomComboBox(QComboBox):
    """Custom QComboBox with working hover effects while preserving dropdown arrow"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_custom_styling()
    
    def setup_custom_styling(self):
        # Create a clean QListView for the dropdown
        list_view = QListView()
        list_view.setSpacing(0)  # Remove spacing between items
        list_view.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.setView(list_view)
        # Note: The dropdown arrow styling is preserved from the global CSS

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
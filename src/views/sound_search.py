"""
Search and filter functionality for sounds
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class SoundSearchBar(QWidget):
    """Widget for searching and filtering sounds"""
    
    # Signals
    search_changed = pyqtSignal(str, list)  # Search text, list of tags to filter by
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.active_tags = []
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search sounds...")
        self.search_input.textChanged.connect(self.on_search_changed)
        main_layout.addWidget(self.search_input)
        
        # Tag filter button
        self.tag_filter_button = QPushButton("Tags")
        self.tag_filter_button.setCheckable(True)
        self.tag_filter_button.clicked.connect(self.on_tag_filter_clicked)
        main_layout.addWidget(self.tag_filter_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_search)
        main_layout.addWidget(self.clear_button)
        
        # Tag filter panel (hidden by default)
        self.tag_filter_panel = QWidget(self)
        self.tag_filter_panel.setVisible(False)
        panel_layout = QVBoxLayout(self.tag_filter_panel)
        
        # Tag list
        self.tag_list_layout = QVBoxLayout()
        panel_layout.addLayout(self.tag_list_layout)
        
        # Apply button
        self.apply_button = QPushButton("Apply Filters")
        self.apply_button.clicked.connect(self.apply_tag_filters)
        panel_layout.addWidget(self.apply_button)
    
    def on_search_changed(self, text):
        """Handle search text change"""
        self.search_changed.emit(text, self.active_tags)
    
    def on_tag_filter_clicked(self, checked):
        """Handle tag filter button click"""
        self.tag_filter_panel.setVisible(checked)
        
        # Position the panel below the search bar
        if checked:
            self.tag_filter_panel.move(0, self.height())
            self.tag_filter_panel.resize(self.width(), 200)
    
    def clear_search(self):
        """Clear the search input and tag filters"""
        self.search_input.clear()
        self.active_tags = []
        
        # Update checkboxes
        for i in range(self.tag_list_layout.count()):
            widget = self.tag_list_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)
        
        self.search_changed.emit("", [])
    
    def update_available_tags(self, tags):
        """Update the list of available tags"""
        # Clear existing tags
        while self.tag_list_layout.count():
            item = self.tag_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add new tags
        for tag in sorted(tags):
            checkbox = QCheckBox(tag)
            checkbox.setChecked(tag in self.active_tags)
            self.tag_list_layout.addWidget(checkbox)
    
    def apply_tag_filters(self):
        """Apply the selected tag filters"""
        self.active_tags = []
        
        # Get selected tags
        for i in range(self.tag_list_layout.count()):
            widget = self.tag_list_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox) and widget.isChecked():
                self.active_tags.append(widget.text())
        
        # Hide the panel
        self.tag_filter_button.setChecked(False)
        self.tag_filter_panel.setVisible(False)
        
        # Emit signal
        self.search_changed.emit(self.search_input.text(), self.active_tags)

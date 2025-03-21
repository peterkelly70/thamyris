"""
Profile dialog - Dialog for profile management
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QListWidget, QPushButton, QMessageBox,
    QFileDialog, QListWidgetItem, QInputDialog
)
from PyQt6.QtCore import Qt, pyqtSignal

import os


class ProfileDialog(QDialog):
    """Dialog for profile management"""
    
    # Signals
    load_profile_signal = pyqtSignal(str)  # Profile path
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile_manager = parent.profile_manager if hasattr(parent, 'profile_manager') else None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Thamyris Profile Manager")
        self.setMinimumSize(500, 400)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("<h2>Profile Manager</h2>")
        main_layout.addWidget(title_label)
        
        # Profile list
        main_layout.addWidget(QLabel("Available Profiles:"))
        
        self.profile_list = QListWidget()
        self.profile_list.itemDoubleClicked.connect(self.on_profile_double_clicked)
        self.profile_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.profile_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.on_new)
        button_layout.addWidget(self.new_button)
        
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.on_load)
        button_layout.addWidget(self.load_button)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)
        button_layout.addWidget(self.save_button)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_button)
        
        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(self.on_import)
        button_layout.addWidget(self.import_button)
        
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.on_export)
        button_layout.addWidget(self.export_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)
        
        # Load profiles
        self.load_profiles()
    
    def load_profiles(self):
        """Load profiles from the profiles directory"""
        self.profile_list.clear()
        
        if not self.profile_manager:
            self.profile_list.addItem("No profile manager available")
            return
        
        profiles = self.profile_manager.get_available_profiles()
        
        if not profiles:
            self.profile_list.addItem("No profiles available")
            return
        
        for profile in profiles:
            item = QListWidgetItem(profile['name'])
            item.setData(Qt.ItemDataRole.UserRole, profile['path'])
            self.profile_list.addItem(item)
    
    def on_profile_double_clicked(self, item):
        """Handle profile double click"""
        self.load_selected_profile()
    
    def on_new(self):
        """Handle new button click"""
        name, ok = QInputDialog.getText(self, "New Profile", "Enter profile name:")
        
        if ok and name:
            # Create a new profile
            if self.profile_manager:
                # Create a safe filename
                safe_name = self.profile_manager._sanitize_filename(name)
                profile_path = os.path.join(self.profile_manager.profiles_directory, f"{safe_name}.profile")
                
                # Check if profile already exists
                if os.path.exists(profile_path):
                    reply = QMessageBox.question(
                        self, "Profile Exists",
                        f"Profile '{name}' already exists. Overwrite?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    
                    if reply != QMessageBox.StandardButton.Yes:
                        return
                
                # Signal to create a new profile
                self.load_profile_signal.emit(profile_path)
                self.accept()
    
    def on_load(self):
        """Handle load button click"""
        self.load_selected_profile()
    
    def on_save(self):
        """Handle save button click"""
        current_item = self.profile_list.currentItem()
        if not current_item:
            # No profile selected, prompt for a new name
            self.on_new()
            return
        
        profile_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Signal to save the current profile
        self.load_profile_signal.emit(profile_path)
        self.accept()
    
    def on_delete(self):
        """Handle delete button click"""
        current_item = self.profile_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a profile to delete.")
            return
        
        profile_name = current_item.text()
        profile_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the profile '{profile_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.profile_manager and self.profile_manager.delete_profile(profile_path):
                # Reload profiles
                self.load_profiles()
                QMessageBox.information(
                    self, "Delete Successful",
                    f"Profile '{profile_name}' deleted successfully.",
                    QMessageBox.StandardButton.Ok
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    f"Failed to delete profile '{profile_name}'.",
                    QMessageBox.StandardButton.Ok
                )
    
    def on_import(self):
        """Handle import button click"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Profile", "", "Profile Files (*.profile);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # Get the profile name from the file name
            profile_name = os.path.splitext(os.path.basename(file_path))[0]
            
            if not self.profile_manager:
                QMessageBox.critical(
                    self, "Error",
                    "No profile manager available.",
                    QMessageBox.StandardButton.Ok
                )
                return
            
            # Copy the file to the profiles directory
            import shutil
            dest_path = os.path.join(self.profile_manager.profiles_directory, f"{profile_name}.profile")
            
            # Check if profile already exists
            if os.path.exists(dest_path):
                reply = QMessageBox.question(
                    self, "Profile Exists",
                    f"Profile '{profile_name}' already exists. Overwrite?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply != QMessageBox.StandardButton.Yes:
                    return
            
            # Copy the file
            shutil.copy2(file_path, dest_path)
            
            # Reload profiles
            self.load_profiles()
            
            QMessageBox.information(
                self, "Import Successful",
                f"Profile '{profile_name}' imported successfully.",
                QMessageBox.StandardButton.Ok
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to import profile: {e}",
                QMessageBox.StandardButton.Ok
            )
    
    def on_export(self):
        """Handle export button click"""
        current_item = self.profile_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a profile to export.")
            return
        
        profile_name = current_item.text()
        profile_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Get export location
        export_path, _ = QFileDialog.getSaveFileName(
            self, "Export Profile", f"{profile_name}.profile", "Profile Files (*.profile);;All Files (*)"
        )
        
        if not export_path:
            return
        
        try:
            # Copy the file
            import shutil
            shutil.copy2(profile_path, export_path)
            
            QMessageBox.information(
                self, "Export Successful",
                f"Profile '{profile_name}' exported successfully.",
                QMessageBox.StandardButton.Ok
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to export profile: {e}",
                QMessageBox.StandardButton.Ok
            )
    
    def load_selected_profile(self):
        """Load the selected profile"""
        current_item = self.profile_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a profile to load.")
            return
        
        profile_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        self.load_profile_signal.emit(profile_path)
        self.accept()

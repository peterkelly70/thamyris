"""
Hotkey editor dialog - Dialog for editing hotkeys
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QMessageBox,
    QListWidgetItem, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

import keyboard


class HotkeyRecordButton(QPushButton):
    """Button for recording hotkeys"""
    
    # Signals
    hotkey_recorded = pyqtSignal(str)  # Hotkey combination
    
    def __init__(self, parent=None):
        super().__init__("Click to Record Hotkey", parent)
        self.setCheckable(True)
        self.clicked.connect(self.on_clicked)
        self.recording = False
        self.keys_pressed = set()
        self.current_hotkey = ""
    
    def on_clicked(self, checked):
        """Handle button click"""
        if checked:
            # Start recording
            self.start_recording()
        else:
            # Stop recording
            self.stop_recording()
    
    def start_recording(self):
        """Start recording hotkeys"""
        self.recording = True
        self.keys_pressed.clear()
        self.setText("Press keys... (ESC to cancel)")
        self.setStyleSheet("background-color: #ffcccc;")
        
        # Hook keyboard events
        keyboard.hook(self.on_key_event)
    
    def stop_recording(self):
        """Stop recording hotkeys"""
        self.recording = False
        self.setText("Click to Record Hotkey")
        self.setStyleSheet("")
        self.setChecked(False)
        
        # Unhook keyboard events
        keyboard.unhook(self.on_key_event)
        
        # Emit the hotkey if valid
        if self.current_hotkey and self.current_hotkey != "escape":
            self.hotkey_recorded.emit(self.current_hotkey)
    
    def on_key_event(self, event):
        """Handle keyboard event"""
        if not self.recording:
            return
        
        # Check if key is pressed
        if event.event_type == keyboard.KEY_DOWN:
            # Add key to pressed keys
            self.keys_pressed.add(event.name)
            
            # Check for escape key to cancel
            if "escape" in self.keys_pressed:
                self.keys_pressed.clear()
                self.current_hotkey = ""
                self.stop_recording()
                return
            
            # Update current hotkey
            self.current_hotkey = "+".join(sorted(self.keys_pressed))
            self.setText(f"Keys: {self.current_hotkey}")
        
        # Check if key is released
        elif event.event_type == keyboard.KEY_UP:
            # Remove key from pressed keys
            if event.name in self.keys_pressed:
                self.keys_pressed.remove(event.name)
            
            # If all keys are released, stop recording
            if not self.keys_pressed:
                self.stop_recording()


class HotkeyEditorDialog(QDialog):
    """Dialog for editing hotkeys"""
    
    def __init__(self, hotkey_manager, parent=None):
        super().__init__(parent)
        self.hotkey_manager = hotkey_manager
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Hotkey Editor")
        self.setMinimumSize(500, 400)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("<h2>Hotkey Editor</h2>")
        main_layout.addWidget(title_label)
        
        # Instructions
        instructions = QLabel(
            "Assign hotkeys to sounds and macros. "
            "Hotkeys will work even when the application is not in focus."
        )
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Hotkey list
        main_layout.addWidget(QLabel("Current Hotkeys:"))
        
        self.hotkey_list = QListWidget()
        self.hotkey_list.setAlternatingRowColors(True)
        main_layout.addWidget(self.hotkey_list)
        
        # Add hotkey section
        add_layout = QHBoxLayout()
        
        add_layout.addWidget(QLabel("Action Name:"))
        self.action_name_edit = QLineEdit()
        add_layout.addWidget(self.action_name_edit)
        
        self.record_button = HotkeyRecordButton()
        self.record_button.hotkey_recorded.connect(self.on_hotkey_recorded)
        add_layout.addWidget(self.record_button)
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.on_add)
        add_layout.addWidget(self.add_button)
        
        main_layout.addLayout(add_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        main_layout.addLayout(button_layout)
        
        # Load hotkeys
        self.load_hotkeys()
    
    def load_hotkeys(self):
        """Load registered hotkeys"""
        self.hotkey_list.clear()
        
        hotkeys = self.hotkey_manager.get_registered_hotkeys()
        
        for hotkey in hotkeys:
            item = QListWidgetItem(f"{hotkey['name']} ({hotkey['key_combination']})")
            item.setData(Qt.ItemDataRole.UserRole, hotkey['key_combination'])
            self.hotkey_list.addItem(item)
    
    def on_hotkey_recorded(self, hotkey):
        """Handle recorded hotkey"""
        # Store the recorded hotkey
        self.recorded_hotkey = hotkey
    
    def on_add(self):
        """Handle add button click"""
        action_name = self.action_name_edit.text().strip()
        
        if not action_name:
            QMessageBox.warning(self, "Missing Name", "Please enter an action name.")
            return
        
        if not hasattr(self, 'recorded_hotkey') or not self.recorded_hotkey:
            QMessageBox.warning(self, "No Hotkey", "Please record a hotkey combination.")
            return
        
        # Register the hotkey
        success = self.hotkey_manager.register_hotkey(
            self.recorded_hotkey, action_name
        )
        
        if success:
            # Clear inputs
            self.action_name_edit.clear()
            delattr(self, 'recorded_hotkey')
            
            # Reload hotkeys
            self.load_hotkeys()
        else:
            QMessageBox.warning(
                self, "Registration Failed", 
                f"Failed to register hotkey '{self.recorded_hotkey}'. It may already be in use."
            )
    
    def on_delete(self):
        """Handle delete button click"""
        current_item = self.hotkey_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a hotkey to delete.")
            return
        
        key_combination = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Unregister the hotkey
        success = self.hotkey_manager.unregister_hotkey(key_combination)
        
        if success:
            # Reload hotkeys
            self.load_hotkeys()
        else:
            QMessageBox.warning(
                self, "Unregistration Failed", 
                f"Failed to unregister hotkey '{key_combination}'."
            )

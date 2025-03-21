"""
Macro editor dialog - Dialog for creating and editing macros
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QMessageBox,
    QListWidgetItem, QLineEdit, QSpinBox,
    QDoubleSpinBox, QComboBox, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal

from models.macro_manager import Macro, MacroStep


class MacroEditorDialog(QDialog):
    """Dialog for creating and editing macros"""
    
    def __init__(self, macro_manager, sound_manager, parent=None, macro=None):
        super().__init__(parent)
        self.macro_manager = macro_manager
        self.sound_manager = sound_manager
        self.macro = macro or Macro("New Macro")
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Macro Editor")
        self.setMinimumSize(600, 500)
        
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("<h2>Macro Editor</h2>")
        main_layout.addWidget(title_label)
        
        # Macro name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Macro Name:"))
        self.name_edit = QLineEdit(self.macro.name)
        name_layout.addWidget(self.name_edit)
        main_layout.addLayout(name_layout)
        
        # Steps table
        main_layout.addWidget(QLabel("Macro Steps:"))
        
        self.steps_table = QTableWidget(0, 3)
        self.steps_table.setHorizontalHeaderLabels(["Sound", "Delay (sec)", "Actions"])
        self.steps_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.steps_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.steps_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        main_layout.addWidget(self.steps_table)
        
        # Add step section
        add_group = QGroupBox("Add Step")
        add_layout = QVBoxLayout(add_group)
        
        sound_layout = QHBoxLayout()
        sound_layout.addWidget(QLabel("Sound:"))
        self.sound_combo = QComboBox()
        self.populate_sound_combo()
        sound_layout.addWidget(self.sound_combo)
        add_layout.addLayout(sound_layout)
        
        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay before playing (seconds):"))
        self.delay_spin = QDoubleSpinBox()
        self.delay_spin.setRange(0, 60)
        self.delay_spin.setDecimals(1)
        self.delay_spin.setSingleStep(0.1)
        delay_layout.addWidget(self.delay_spin)
        add_layout.addLayout(delay_layout)
        
        self.add_step_button = QPushButton("Add Step")
        self.add_step_button.clicked.connect(self.on_add_step)
        add_layout.addWidget(self.add_step_button)
        
        main_layout.addWidget(add_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.test_button = QPushButton("Test Macro")
        self.test_button.clicked.connect(self.on_test)
        button_layout.addWidget(self.test_button)
        
        button_layout.addStretch()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.on_save)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        # Load macro steps
        self.load_steps()
    
    def populate_sound_combo(self):
        """Populate the sound combo box"""
        self.sound_combo.clear()
        
        # Add all available sounds
        sounds = self.sound_manager.get_all_sounds() if hasattr(self.sound_manager, 'get_all_sounds') else []
        
        for sound in sounds:
            self.sound_combo.addItem(sound.name, sound.id)
    
    def load_steps(self):
        """Load macro steps into the table"""
        self.steps_table.setRowCount(0)
        
        for i, step in enumerate(self.macro.steps):
            self.steps_table.insertRow(i)
            
            # Sound name
            sound_name = "Unknown Sound"
            if hasattr(self.sound_manager, 'get_sound'):
                sound = self.sound_manager.get_sound(step.sound_id)
                if sound:
                    sound_name = sound.name
            
            sound_item = QTableWidgetItem(sound_name)
            sound_item.setData(Qt.ItemDataRole.UserRole, step.sound_id)
            self.steps_table.setItem(i, 0, sound_item)
            
            # Delay
            delay_item = QTableWidgetItem(f"{step.delay:.1f}")
            self.steps_table.setItem(i, 1, delay_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            
            up_button = QPushButton("↑")
            up_button.setFixedWidth(30)
            up_button.clicked.connect(lambda _, s=step.id: self.on_move_step_up(s))
            actions_layout.addWidget(up_button)
            
            down_button = QPushButton("↓")
            down_button.setFixedWidth(30)
            down_button.clicked.connect(lambda _, s=step.id: self.on_move_step_down(s))
            actions_layout.addWidget(down_button)
            
            delete_button = QPushButton("×")
            delete_button.setFixedWidth(30)
            delete_button.clicked.connect(lambda _, s=step.id: self.on_delete_step(s))
            actions_layout.addWidget(delete_button)
            
            self.steps_table.setCellWidget(i, 2, actions_widget)
    
    def on_add_step(self):
        """Handle add step button click"""
        sound_id = self.sound_combo.currentData()
        delay = self.delay_spin.value()
        
        if not sound_id:
            QMessageBox.warning(self, "No Sound", "Please select a sound to add.")
            return
        
        # Add step to macro
        self.macro.add_step(sound_id, delay)
        
        # Reload steps
        self.load_steps()
    
    def on_move_step_up(self, step_id):
        """Handle move step up button click"""
        self.macro.move_step_up(step_id)
        self.load_steps()
    
    def on_move_step_down(self, step_id):
        """Handle move step down button click"""
        self.macro.move_step_down(step_id)
        self.load_steps()
    
    def on_delete_step(self, step_id):
        """Handle delete step button click"""
        self.macro.remove_step(step_id)
        self.load_steps()
    
    def on_test(self):
        """Handle test macro button click"""
        if not self.macro.steps:
            QMessageBox.warning(self, "Empty Macro", "This macro has no steps to play.")
            return
        
        # Update macro from UI
        self.update_macro_from_ui()
        
        # Play the macro
        if hasattr(self.macro_manager, 'play_macro'):
            self.macro_manager.play_macro(self.macro.id, self.play_sound_callback)
    
    def play_sound_callback(self, sound_id):
        """Callback for playing sounds during macro test"""
        if hasattr(self.sound_manager, 'play_sound'):
            sound = self.sound_manager.get_sound(sound_id)
            if sound:
                self.sound_manager.play_sound(sound)
    
    def on_save(self):
        """Handle save button click"""
        # Update macro from UI
        self.update_macro_from_ui()
        
        # Save the macro
        if self.macro.id not in self.macro_manager.macros:
            self.macro_manager.macros[self.macro.id] = self.macro
        
        self.macro_manager.save_macros()
        
        self.accept()
    
    def update_macro_from_ui(self):
        """Update macro from UI state"""
        # Update name
        self.macro.name = self.name_edit.text().strip()
        if not self.macro.name:
            self.macro.name = "Unnamed Macro"
    
    def get_macro(self):
        """Get the edited macro"""
        return self.macro

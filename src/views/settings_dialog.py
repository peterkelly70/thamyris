"""
Settings dialog - Dialog for application settings
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QSpinBox, QFontComboBox, QPushButton,
    QGroupBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from models.settings import Settings, Theme


class SettingsDialog(QDialog):
    """Dialog for application settings"""
    
    # Signals
    settings_changed = pyqtSignal(object)  # Settings object
    
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or Settings()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Thamyris Settings")
        self.setMinimumWidth(400)
        
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Appearance tab
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout(appearance_tab)
        
        # Theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", Theme.LIGHT.value)
        self.theme_combo.addItem("Dark", Theme.DARK.value)
        self.theme_combo.addItem("Custom", Theme.CUSTOM.value)
        
        # Set current theme
        index = self.theme_combo.findData(self.settings.theme.value)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        
        theme_layout.addWidget(self.theme_combo)
        appearance_layout.addLayout(theme_layout)
        
        # Font
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font:"))
        
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.settings.font_family))
        font_layout.addWidget(self.font_combo)
        
        font_layout.addWidget(QLabel("Size:"))
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(self.settings.font_size)
        font_layout.addWidget(self.font_size_spin)
        
        appearance_layout.addLayout(font_layout)
        
        # Add appearance tab
        tab_widget.addTab(appearance_tab, "Appearance")
        
        # Audio tab
        audio_tab = QWidget()
        audio_layout = QVBoxLayout(audio_tab)
        
        # Default volumes
        volumes_group = QGroupBox("Default Volumes")
        volumes_layout = QVBoxLayout(volumes_group)
        
        # Master volume
        master_layout = QHBoxLayout()
        master_layout.addWidget(QLabel("Master:"))
        
        self.master_volume_spin = QSpinBox()
        self.master_volume_spin.setRange(0, 100)
        self.master_volume_spin.setSuffix("%")
        self.master_volume_spin.setValue(int(self.settings.master_volume * 100))
        master_layout.addWidget(self.master_volume_spin)
        
        volumes_layout.addLayout(master_layout)
        
        # Ambient volume
        ambient_layout = QHBoxLayout()
        ambient_layout.addWidget(QLabel("Ambient:"))
        
        self.ambient_volume_spin = QSpinBox()
        self.ambient_volume_spin.setRange(0, 100)
        self.ambient_volume_spin.setSuffix("%")
        self.ambient_volume_spin.setValue(int(self.settings.ambient_volume * 100))
        ambient_layout.addWidget(self.ambient_volume_spin)
        
        volumes_layout.addLayout(ambient_layout)
        
        # Effects volume
        effects_layout = QHBoxLayout()
        effects_layout.addWidget(QLabel("Effects:"))
        
        self.effects_volume_spin = QSpinBox()
        self.effects_volume_spin.setRange(0, 100)
        self.effects_volume_spin.setSuffix("%")
        self.effects_volume_spin.setValue(int(self.settings.effects_volume * 100))
        effects_layout.addWidget(self.effects_volume_spin)
        
        volumes_layout.addLayout(effects_layout)
        
        audio_layout.addWidget(volumes_group)
        
        # Fade settings
        fade_group = QGroupBox("Fade Settings")
        fade_layout = QVBoxLayout(fade_group)
        
        # Fade in
        fade_in_layout = QHBoxLayout()
        fade_in_layout.addWidget(QLabel("Default Fade In:"))
        
        self.fade_in_spin = QSpinBox()
        self.fade_in_spin.setRange(0, 10000)
        self.fade_in_spin.setSuffix(" ms")
        self.fade_in_spin.setSingleStep(100)
        self.fade_in_spin.setValue(self.settings.fade_in_duration)
        fade_in_layout.addWidget(self.fade_in_spin)
        
        fade_layout.addLayout(fade_in_layout)
        
        # Fade out
        fade_out_layout = QHBoxLayout()
        fade_out_layout.addWidget(QLabel("Default Fade Out:"))
        
        self.fade_out_spin = QSpinBox()
        self.fade_out_spin.setRange(0, 10000)
        self.fade_out_spin.setSuffix(" ms")
        self.fade_out_spin.setSingleStep(100)
        self.fade_out_spin.setValue(self.settings.fade_out_duration)
        fade_out_layout.addWidget(self.fade_out_spin)
        
        fade_layout.addLayout(fade_out_layout)
        
        audio_layout.addWidget(fade_group)
        
        # Add audio tab
        tab_widget.addTab(audio_tab, "Audio")
        
        # Button box
        button_box = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_box.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_box.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_box)
    
    def accept(self):
        """Handle OK button click"""
        # Update settings
        self.settings.theme = Theme(self.theme_combo.currentData())
        self.settings.font_family = self.font_combo.currentFont().family()
        self.settings.font_size = self.font_size_spin.value()
        self.settings.master_volume = self.master_volume_spin.value() / 100.0
        self.settings.ambient_volume = self.ambient_volume_spin.value() / 100.0
        self.settings.effects_volume = self.effects_volume_spin.value() / 100.0
        self.settings.fade_in_duration = self.fade_in_spin.value()
        self.settings.fade_out_duration = self.fade_out_spin.value()
        
        # Emit signal
        self.settings_changed.emit(self.settings)
        
        # Close dialog
        super().accept()
    
    def get_settings(self):
        """Get the current settings"""
        return self.settings

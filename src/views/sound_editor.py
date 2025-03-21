"""
Sound editor dialog - Dialog for editing sound properties
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QComboBox, QSpinBox, QPushButton,
    QGroupBox, QFileDialog, QDoubleSpinBox, QColorDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from models.sound import Sound, PlaybackMode, ChannelType


class SoundEditorDialog(QDialog):
    """Dialog for editing sound properties"""
    
    def __init__(self, sound, parent=None):
        super().__init__(parent)
        self.sound = sound
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Edit Sound")
        self.setMinimumWidth(400)
        
        main_layout = QVBoxLayout(self)
        
        # Basic properties
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QVBoxLayout(basic_group)
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        
        self.name_edit = QLineEdit(self.sound.name)
        name_layout.addWidget(self.name_edit)
        
        basic_layout.addLayout(name_layout)
        
        # File path
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("File:"))
        
        self.file_edit = QLineEdit(self.sound.file_path)
        self.file_edit.setReadOnly(True)
        file_layout.addWidget(self.file_edit)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.on_browse)
        file_layout.addWidget(self.browse_button)
        
        basic_layout.addLayout(file_layout)
        
        # Channel
        channel_layout = QHBoxLayout()
        channel_layout.addWidget(QLabel("Channel:"))
        
        self.channel_combo = QComboBox()
        self.channel_combo.addItem("Ambient", ChannelType.AMBIENT)
        self.channel_combo.addItem("Effects 1", ChannelType.EFFECTS_1)
        self.channel_combo.addItem("Effects 2", ChannelType.EFFECTS_2)
        self.channel_combo.addItem("Effects 3", ChannelType.EFFECTS_3)
        
        # Set current channel
        index = self.channel_combo.findData(self.sound.channel)
        if index >= 0:
            self.channel_combo.setCurrentIndex(index)
        
        channel_layout.addWidget(self.channel_combo)
        
        basic_layout.addLayout(channel_layout)
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        
        self.volume_spin = QDoubleSpinBox()
        self.volume_spin.setRange(0.0, 1.0)
        self.volume_spin.setSingleStep(0.1)
        self.volume_spin.setValue(self.sound.volume)
        volume_layout.addWidget(self.volume_spin)
        
        basic_layout.addLayout(volume_layout)
        
        main_layout.addWidget(basic_group)
        
        # Playback properties
        playback_group = QGroupBox("Playback Properties")
        playback_layout = QVBoxLayout(playback_group)
        
        # Playback mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Playback Mode:"))
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Play Once", PlaybackMode.PLAY_ONCE)
        self.mode_combo.addItem("Play N Times", PlaybackMode.PLAY_N_TIMES)
        self.mode_combo.addItem("Loop", PlaybackMode.LOOP)
        
        # Set current mode
        index = self.mode_combo.findData(self.sound.playback_mode)
        if index >= 0:
            self.mode_combo.setCurrentIndex(index)
        
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        
        playback_layout.addLayout(mode_layout)
        
        # Repeat count
        repeat_layout = QHBoxLayout()
        repeat_layout.addWidget(QLabel("Repeat Count:"))
        
        self.repeat_spin = QSpinBox()
        self.repeat_spin.setRange(1, 100)
        self.repeat_spin.setValue(self.sound.repeat_count)
        repeat_layout.addWidget(self.repeat_spin)
        
        playback_layout.addLayout(repeat_layout)
        
        # Fade in/out
        fade_layout = QHBoxLayout()
        fade_layout.addWidget(QLabel("Fade In:"))
        
        self.fade_in_spin = QSpinBox()
        self.fade_in_spin.setRange(0, 10000)
        self.fade_in_spin.setSuffix(" ms")
        self.fade_in_spin.setSingleStep(100)
        self.fade_in_spin.setValue(self.sound.fade_in)
        fade_layout.addWidget(self.fade_in_spin)
        
        fade_layout.addWidget(QLabel("Fade Out:"))
        
        self.fade_out_spin = QSpinBox()
        self.fade_out_spin.setRange(0, 10000)
        self.fade_out_spin.setSuffix(" ms")
        self.fade_out_spin.setSingleStep(100)
        self.fade_out_spin.setValue(self.sound.fade_out)
        fade_layout.addWidget(self.fade_out_spin)
        
        playback_layout.addLayout(fade_layout)
        
        main_layout.addWidget(playback_group)
        
        # Tags
        tags_group = QGroupBox("Tags")
        tags_layout = QVBoxLayout(tags_group)
        
        tags_layout.addWidget(QLabel("Tags (comma-separated):"))
        
        self.tags_edit = QLineEdit(self.sound.get_tags_as_string())
        tags_layout.addWidget(self.tags_edit)
        
        tags_help = QLabel("Example: monster,roar,loud")
        tags_help.setStyleSheet("color: gray; font-style: italic;")
        tags_layout.addWidget(tags_help)
        
        main_layout.addWidget(tags_group)
        
        # Appearance
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QHBoxLayout(appearance_group)
        
        appearance_layout.addWidget(QLabel("Button Color:"))
        
        self.color_button = QPushButton()
        self.color_button.setStyleSheet(f"background-color: {self.sound.color};")
        self.color_button.setFixedSize(30, 30)
        self.color_button.clicked.connect(self.on_color_select)
        appearance_layout.addWidget(self.color_button)
        
        main_layout.addWidget(appearance_group)
        
        # Button box
        button_box = QHBoxLayout()
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        button_box.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_box.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_box)
        
        # Update UI based on current mode
        self.on_mode_changed(self.mode_combo.currentIndex())
    
    def on_browse(self):
        """Handle browse button click"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Sound File", "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac);;All Files (*)"
        )
        
        if file_path:
            self.file_edit.setText(file_path)
    
    def on_mode_changed(self, index):
        """Handle playback mode change"""
        mode = self.mode_combo.itemData(index)
        
        # Enable/disable repeat count based on mode
        self.repeat_spin.setEnabled(mode == PlaybackMode.PLAY_N_TIMES)
    
    def on_color_select(self):
        """Handle color button click"""
        color = QColorDialog.getColor(QColor(self.sound.color), self)
        
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
    
    def get_sound(self):
        """Get the edited sound"""
        # Create a new Sound object with the edited properties
        sound = Sound(
            name=self.name_edit.text(),
            file_path=self.file_edit.text(),
            channel=self.channel_combo.currentData(),
            volume=self.volume_spin.value(),
            playback_mode=self.mode_combo.currentData(),
            repeat_count=self.repeat_spin.value(),
            fade_in=self.fade_in_spin.value(),
            fade_out=self.fade_out_spin.value(),
            color=self.color_button.styleSheet().split("background-color: ")[1].split(";")[0]
        )
        
        # Add tags from the tags edit field
        sound.add_tags_from_string(self.tags_edit.text())
        
        return sound

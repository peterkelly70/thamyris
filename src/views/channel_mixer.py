"""
Channel mixer view - Controls for audio channels
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSlider, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from models.sound import ChannelType


class ChannelMixerView(QGroupBox):
    """Widget for controlling audio channel volumes"""
    
    # Signals
    channel_volume_changed = pyqtSignal(object, float)  # Channel type, volume
    voice_ducking_toggled = pyqtSignal(bool)  # Enabled
    voice_ducking_amount_changed = pyqtSignal(float)  # Amount
    
    def __init__(self, parent=None):
        super().__init__("Channel Mixer", parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        
        # Create sliders for each channel
        self.channel_sliders = {}
        self.channel_labels = {}
        
        # Ambient channel
        ambient_layout = QHBoxLayout()
        ambient_layout.addWidget(QLabel("Ambient:"))
        
        self.channel_sliders[ChannelType.AMBIENT] = QSlider(Qt.Orientation.Horizontal)
        self.channel_sliders[ChannelType.AMBIENT].setRange(0, 100)
        self.channel_sliders[ChannelType.AMBIENT].setValue(50)
        self.channel_sliders[ChannelType.AMBIENT].setTickPosition(QSlider.TickPosition.TicksBelow)
        self.channel_sliders[ChannelType.AMBIENT].setTickInterval(10)
        ambient_layout.addWidget(self.channel_sliders[ChannelType.AMBIENT])
        
        self.channel_labels[ChannelType.AMBIENT] = QLabel("50%")
        ambient_layout.addWidget(self.channel_labels[ChannelType.AMBIENT])
        
        main_layout.addLayout(ambient_layout)
        
        # Effects channels
        for i, channel_type in enumerate([ChannelType.EFFECTS_1, ChannelType.EFFECTS_2, ChannelType.EFFECTS_3]):
            layout = QHBoxLayout()
            layout.addWidget(QLabel(f"Effects {i+1}:"))
            
            self.channel_sliders[channel_type] = QSlider(Qt.Orientation.Horizontal)
            self.channel_sliders[channel_type].setRange(0, 100)
            self.channel_sliders[channel_type].setValue(70)
            self.channel_sliders[channel_type].setTickPosition(QSlider.TickPosition.TicksBelow)
            self.channel_sliders[channel_type].setTickInterval(10)
            layout.addWidget(self.channel_sliders[channel_type])
            
            self.channel_labels[channel_type] = QLabel("70%")
            layout.addWidget(self.channel_labels[channel_type])
            
            main_layout.addLayout(layout)
        
        # Voice ducking controls
        ducking_group = QWidget()
        ducking_layout = QVBoxLayout(ducking_group)
        
        ducking_header = QHBoxLayout()
        self.ducking_checkbox = QCheckBox("Voice Ducking")
        self.ducking_checkbox.setChecked(True)
        ducking_header.addWidget(self.ducking_checkbox)
        ducking_layout.addLayout(ducking_header)
        
        ducking_slider_layout = QHBoxLayout()
        ducking_slider_layout.addWidget(QLabel("Amount:"))
        
        self.ducking_slider = QSlider(Qt.Orientation.Horizontal)
        self.ducking_slider.setRange(0, 100)
        self.ducking_slider.setValue(50)
        self.ducking_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ducking_slider.setTickInterval(10)
        ducking_slider_layout.addWidget(self.ducking_slider)
        
        self.ducking_label = QLabel("50%")
        ducking_slider_layout.addWidget(self.ducking_label)
        
        ducking_layout.addLayout(ducking_slider_layout)
        main_layout.addWidget(ducking_group)
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals and slots"""
        # Channel volume sliders
        for channel_type, slider in self.channel_sliders.items():
            slider.valueChanged.connect(
                lambda value, ct=channel_type: self.on_channel_volume_changed(ct, value)
            )
        
        # Voice ducking controls
        self.ducking_checkbox.toggled.connect(self.on_ducking_toggled)
        self.ducking_slider.valueChanged.connect(self.on_ducking_amount_changed)
    
    def on_channel_volume_changed(self, channel_type, value):
        """Handle channel volume slider change"""
        self.channel_labels[channel_type].setText(f"{value}%")
        self.channel_volume_changed.emit(channel_type, value / 100.0)
    
    def on_ducking_toggled(self, enabled):
        """Handle voice ducking checkbox toggle"""
        self.ducking_slider.setEnabled(enabled)
        self.voice_ducking_toggled.emit(enabled)
    
    def on_ducking_amount_changed(self, value):
        """Handle voice ducking amount slider change"""
        self.ducking_label.setText(f"{value}%")
        self.voice_ducking_amount_changed.emit(value / 100.0)
    
    def set_channel_volume(self, channel_type, volume):
        """Set the volume for a channel"""
        value = int(volume * 100)
        self.channel_sliders[channel_type].setValue(value)
        self.channel_labels[channel_type].setText(f"{value}%")
    
    def set_voice_ducking(self, enabled, amount):
        """Set voice ducking settings"""
        self.ducking_checkbox.setChecked(enabled)
        value = int(amount * 100)
        self.ducking_slider.setValue(value)
        self.ducking_label.setText(f"{value}%")

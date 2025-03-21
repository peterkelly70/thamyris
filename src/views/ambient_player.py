"""
Ambient player view - Controls for ambient background tracks
"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QSlider, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal


class AmbientPlayerView(QGroupBox):
    """Widget for controlling ambient background tracks"""
    
    # Signals
    play_ambient_signal = pyqtSignal(int)  # Index in the ambient list
    stop_ambient_signal = pyqtSignal()
    add_ambient_signal = pyqtSignal(str)  # File path
    
    def __init__(self, parent=None):
        super().__init__("Ambient Background", parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        
        # Track selection
        track_layout = QHBoxLayout()
        track_layout.addWidget(QLabel("Track:"))
        
        self.track_combo = QComboBox()
        self.track_combo.setMinimumWidth(200)
        track_layout.addWidget(self.track_combo)
        
        self.add_track_button = QPushButton("+")
        self.add_track_button.setMaximumWidth(30)
        self.add_track_button.clicked.connect(self.on_add_track)
        track_layout.addWidget(self.add_track_button)
        
        main_layout.addLayout(track_layout)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play)
        controls_layout.addWidget(self.play_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop)
        controls_layout.addWidget(self.stop_button)
        
        main_layout.addLayout(controls_layout)
    
    def on_play(self):
        """Handle play button click"""
        index = self.track_combo.currentIndex()
        if index >= 0:
            self.play_ambient_signal.emit(index)
    
    def on_stop(self):
        """Handle stop button click"""
        self.stop_ambient_signal.emit()
    
    def on_add_track(self):
        """Handle add track button click"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Ambient Track", "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac);;All Files (*)"
        )
        
        if file_path:
            self.add_ambient_signal.emit(file_path)
    
    def update_track_list(self, tracks):
        """Update the ambient track list"""
        self.track_combo.clear()
        
        for track in tracks:
            self.track_combo.addItem(track.name)
    
    def set_active_track(self, index):
        """Set the active track"""
        if index >= 0 and index < self.track_combo.count():
            self.track_combo.setCurrentIndex(index)

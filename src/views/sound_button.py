"""
Sound button view - A button for playing sounds
"""
from PyQt6.QtWidgets import QPushButton, QMenu, QAction, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont

from models.sound import Sound, PlaybackMode


class SoundButton(QPushButton):
    """Button for playing sounds with context menu for editing"""
    
    # Signals
    play_clicked = pyqtSignal(object)  # Emits the Sound object
    edit_clicked = pyqtSignal(object, object)  # Emits the Sound object and button reference
    delete_clicked = pyqtSignal(object, object)  # Emits the Sound object and button reference
    
    def __init__(self, sound: Sound, parent=None):
        super().__init__(parent)
        self.sound = sound
        self.init_ui()
    
    def init_ui(self):
        """Initialize the button UI"""
        # Set button style
        self.setStyleSheet(f"background-color: {self.sound.color}; color: white;")
        
        # Set button size
        self.setMinimumSize(QSize(120, 80))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        # Set font
        font = QFont()
        font.setBold(True)
        self.setFont(font)
        
        # Create button text with name, playback mode, and tags
        button_text = self.sound.name
        
        # Add playback mode indicator
        if self.sound.playback_mode == PlaybackMode.LOOP:
            button_text += "\n[Loop]"
        elif self.sound.playback_mode == PlaybackMode.PLAY_N_TIMES:
            button_text += f"\n[x{self.sound.repeat_count}]"
        
        # Add tags if present
        if self.sound.tags:
            tags_text = ", ".join(self.sound.tags)
            button_text += f"\n[{tags_text}]"
        
        self.setText(button_text)
        
        # Connect click event
        self.clicked.connect(self.on_clicked)
        
        # Set up context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def set_sound(self, sound: Sound):
        """Update the button with a new sound"""
        self.sound = sound
        self.init_ui()
    
    def on_clicked(self):
        """Handle button click"""
        self.play_clicked.emit(self.sound)
    
    def show_context_menu(self, pos):
        """Show context menu for the button"""
        menu = QMenu(self)
        
        # Add actions
        play_action = QAction("Play", self)
        play_action.triggered.connect(self.on_clicked)
        menu.addAction(play_action)
        
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(lambda: self.edit_clicked.emit(self.sound, self))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_clicked.emit(self.sound, self))
        menu.addAction(delete_action)
        
        # Show the menu
        menu.exec(self.mapToGlobal(pos))

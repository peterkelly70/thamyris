"""
Main window view - The main application window
"""
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QComboBox, QSlider, QGroupBox, 
    QScrollArea, QGridLayout, QFileDialog, QMessageBox,
    QDialog, QLineEdit, QColorDialog, QSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QAction

from views.sound_button import SoundButton
from views.channel_mixer import ChannelMixerView
from views.ambient_player import AmbientPlayerView
from views.settings_dialog import SettingsDialog
from views.sound_editor import SoundEditorDialog
from views.profile_dialog import ProfileDialog
from views.sound_search import SoundSearchBar


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    connect_discord_signal = pyqtSignal(str)
    disconnect_discord_signal = pyqtSignal()
    play_sound_signal = pyqtSignal(object)
    stop_sound_signal = pyqtSignal(str)
    stop_all_sounds_signal = pyqtSignal()
    load_profile_signal = pyqtSignal(str)
    save_profile_signal = pyqtSignal(str)
    master_volume_changed_signal = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        
        # Window properties
        self.setWindowTitle("Thamyris - Soundboard for Roleplaying")
        self.setMinimumSize(800, 600)
        
        # Initialize UI components
        self.init_ui()
        
        # Connect signals and slots
        self.connect_signals()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create top panel
        self.create_top_panel()
        
        # Create tab widget
        self.create_tab_widget()
        
        # Create bottom panel
        self.create_bottom_panel()
    
    def create_menu_bar(self):
        """Create the menu bar"""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        # New profile action
        new_profile_action = QAction("&New Profile", self)
        new_profile_action.setShortcut("Ctrl+N")
        new_profile_action.triggered.connect(self.on_new_profile)
        file_menu.addAction(new_profile_action)
        
        # Open profile action
        open_profile_action = QAction("&Open Profile", self)
        open_profile_action.setShortcut("Ctrl+O")
        open_profile_action.triggered.connect(self.on_open_profile)
        file_menu.addAction(open_profile_action)
        
        # Save profile action
        save_profile_action = QAction("&Save Profile", self)
        save_profile_action.setShortcut("Ctrl+S")
        save_profile_action.triggered.connect(self.on_save_profile)
        file_menu.addAction(save_profile_action)
        
        # Save profile as action
        save_profile_as_action = QAction("Save Profile &As...", self)
        save_profile_as_action.setShortcut("Ctrl+Shift+S")
        save_profile_as_action.triggered.connect(self.on_save_profile_as)
        file_menu.addAction(save_profile_as_action)
        
        file_menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Se&ttings", self)
        settings_action.triggered.connect(self.on_settings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = self.menuBar().addMenu("&Edit")
        
        # Add tab action
        add_tab_action = QAction("Add &Tab", self)
        add_tab_action.triggered.connect(self.on_add_tab)
        edit_menu.addAction(add_tab_action)
        
        # Add sound action
        add_sound_action = QAction("Add &Sound", self)
        add_sound_action.triggered.connect(self.on_add_sound)
        edit_menu.addAction(add_sound_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        # About action
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def create_top_panel(self):
        """Create the top panel with Discord connection and master volume"""
        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)
        
        # Discord connection
        discord_group = QGroupBox("Discord Connection")
        discord_layout = QHBoxLayout(discord_group)
        
        self.channel_combo = QComboBox()
        self.channel_combo.setMinimumWidth(200)
        discord_layout.addWidget(self.channel_combo)
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_discord)
        discord_layout.addWidget(self.connect_button)
        
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.on_disconnect_discord)
        self.disconnect_button.setEnabled(False)
        discord_layout.addWidget(self.disconnect_button)
        
        top_layout.addWidget(discord_group)
        
        # Master volume
        volume_group = QGroupBox("Master Volume")
        volume_layout = QHBoxLayout(volume_group)
        
        self.master_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.master_volume_slider.setRange(0, 100)
        self.master_volume_slider.setValue(80)
        volume_layout.addWidget(self.master_volume_slider)
        
        self.master_volume_label = QLabel("80%")
        volume_layout.addWidget(self.master_volume_label)
        
        top_layout.addWidget(volume_group)
        
        # Stop all button
        self.stop_all_button = QPushButton("Stop All Sounds")
        self.stop_all_button.clicked.connect(self.on_stop_all_sounds)
        top_layout.addWidget(self.stop_all_button)
        
        self.main_layout.addWidget(top_panel)
    
    def create_tab_widget(self):
        """Create the tab widget for sound buttons"""
        # Create search bar
        self.search_bar = SoundSearchBar()
        self.search_bar.search_changed.connect(self.on_search_changed)
        self.main_layout.addWidget(self.search_bar)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.on_tab_close_requested)
        
        # Add a default tab
        self.add_tab("General")
        
        self.main_layout.addWidget(self.tab_widget, 1)  # Give it a stretch factor of 1
    
    def create_bottom_panel(self):
        """Create the bottom panel with channel mixer and ambient player"""
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)
        
        # Channel mixer
        self.channel_mixer = ChannelMixerView()
        bottom_layout.addWidget(self.channel_mixer)
        
        # Ambient player
        self.ambient_player = AmbientPlayerView()
        bottom_layout.addWidget(self.ambient_player)
        
        self.main_layout.addWidget(bottom_panel)
    
    def connect_signals(self):
        """Connect signals and slots"""
        # Master volume slider
        self.master_volume_slider.valueChanged.connect(self.on_master_volume_changed)
        
    def on_search_changed(self, search_text, tag_filters):
        """Handle search text or tag filters change"""
        # Get the current tab
        current_index = self.tab_widget.currentIndex()
        if current_index < 0:
            return
            
        # Get the tab's scroll area
        scroll = self.tab_widget.widget(current_index)
        
        # Get the tab content widget
        tab_content = scroll.widget()
        
        # Get all sound buttons in the tab
        for i in range(tab_content.layout().count()):
            item = tab_content.layout().itemAt(i)
            if item and item.widget():
                button = item.widget()
                if isinstance(button, SoundButton):
                    # Check if the button matches the search criteria
                    sound = button.sound
                    name_match = not search_text or search_text.lower() in sound.name.lower()
                    
                    # Check tag filters
                    tag_match = True
                    if tag_filters:
                        tag_match = any(sound.has_tag(tag) for tag in tag_filters)
                    
                    # Show or hide the button based on the search
                    button.setVisible(name_match and tag_match)
    
    def add_tab(self, name):
        """Add a new tab with the given name"""
        # Create a scroll area for the tab content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create a widget for the tab content
        tab_content = QWidget()
        
        # Create a grid layout for the sound buttons
        grid_layout = QGridLayout(tab_content)
        grid_layout.setSpacing(10)
        
        # Set the tab content as the scroll area's widget
        scroll.setWidget(tab_content)
        
        # Add the scroll area to the tab widget
        self.tab_widget.addTab(scroll, name)
        
        # Set the new tab as the current tab
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
    
    def add_sound_button(self, tab_index, sound):
        """Add a sound button to the specified tab"""
        # Get the tab's scroll area
        scroll = self.tab_widget.widget(tab_index)
        
        # Get the tab content widget
        tab_content = scroll.widget()
        
        # Get the grid layout
        grid_layout = tab_content.layout()
        
        # Calculate the row and column for the new button
        count = grid_layout.count()
        cols = max(1, tab_content.width() // 150)  # Approximate button width + spacing
        row = count // cols
        col = count % cols
        
        # Create a sound button
        button = SoundButton(sound)
        button.play_signal.connect(self.on_play_sound)
        button.stop_signal.connect(self.on_stop_sound)
        button.edit_signal.connect(self.on_edit_sound)
        
        # Add the button to the grid layout
        grid_layout.addWidget(button, row, col)
    
    def on_master_volume_changed(self, value):
        """Handle master volume slider change"""
        self.master_volume_label.setText(f"{value}%")
        # Emit signal to update audio player master volume
        self.master_volume_changed_signal.emit(value / 100.0)
    
    def on_connect_discord(self):
        """Handle connect to Discord button click"""
        # Get the selected channel ID
        if self.channel_combo.count() == 0:
            QMessageBox.warning(self, "No Channels", "No voice channels available.")
            return
        
        channel_id = self.channel_combo.currentData()
        if not channel_id:
            return
        
        # Emit signal to connect to Discord
        self.connect_discord_signal.emit(channel_id)
    
    def on_disconnect_discord(self):
        """Handle disconnect from Discord button click"""
        # Emit signal to disconnect from Discord
        self.disconnect_discord_signal.emit()
    
    def set_discord_connected(self, connected):
        """Set the Discord connection state"""
        self.connect_button.setEnabled(not connected)
        self.disconnect_button.setEnabled(connected)
    
    def on_play_sound(self, sound):
        """Handle play sound button click"""
        # Emit signal to play sound
        self.play_sound_signal.emit(sound)
    
    def on_stop_sound(self, sound_path):
        """Handle stop sound button click"""
        # Emit signal to stop sound
        self.stop_sound_signal.emit(sound_path)
    
    def on_stop_all_sounds(self):
        """Handle stop all sounds button click"""
        # Emit signal to stop all sounds
        self.stop_all_sounds_signal.emit()
    
    def on_edit_sound(self, sound, button):
        """Handle edit sound button click"""
        # Create a sound editor dialog
        dialog = SoundEditorDialog(sound, self)
        
        # Show the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the edited sound
            edited_sound = dialog.get_sound()
            
            # Update the button
            button.set_sound(edited_sound)
    
    def on_add_tab(self):
        """Handle add tab action"""
        # Create a dialog to get the tab name
        name, ok = QInputDialog.getText(self, "Add Tab", "Tab name:")
        
        if ok and name:
            # Add the tab
            self.add_tab(name)
    
    def on_tab_close_requested(self, index):
        """Handle tab close request"""
        # Don't allow closing the last tab
        if self.tab_widget.count() <= 1:
            QMessageBox.warning(self, "Cannot Close Tab", "Cannot close the last tab.")
            return
        
        # Ask for confirmation
        reply = QMessageBox.question(
            self, "Close Tab", 
            f"Are you sure you want to close the tab '{self.tab_widget.tabText(index)}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Close the tab
            self.tab_widget.removeTab(index)
    
    def on_add_sound(self):
        """Handle add sound action"""
        # Get the current tab index
        current_index = self.tab_widget.currentIndex()
        if current_index < 0:
            QMessageBox.warning(self, "No Tab", "No tab selected.")
            return
        
        # Open a file dialog to select a sound file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Sound File", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)"
        )
        
        if not file_path:
            return
        
        # Create a new sound
        sound = Sound(
            name=os.path.basename(file_path),
            file_path=file_path
        )
        
        # Create a sound editor dialog
        dialog = SoundEditorDialog(sound, self)
        
        # Show the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the edited sound
            edited_sound = dialog.get_sound()
            
            # Add a button for the sound
            self.add_sound_button(current_index, edited_sound)
    
    def on_new_profile(self):
        """Handle new profile action"""
        # Ask for confirmation if there are unsaved changes
        reply = QMessageBox.question(
            self, "New Profile", 
            "Are you sure you want to create a new profile? Any unsaved changes will be lost.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Clear all tabs
            while self.tab_widget.count() > 0:
                self.tab_widget.removeTab(0)
            
            # Add a default tab
            self.add_tab("General")
            
            # Clear ambient tracks
            self.ambient_player.clear_tracks()
    
    def on_open_profile(self):
        """Handle open profile action"""
        # Create a profile dialog
        dialog = ProfileDialog(self, mode=ProfileDialog.Mode.OPEN)
        
        # Show the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the selected profile path
            profile_path = dialog.get_selected_profile_path()
            
            # Emit signal to load profile
            self.load_profile_signal.emit(profile_path)
    
    def on_save_profile(self):
        """Handle save profile action"""
        # Check if there's a current profile
        if not hasattr(self, 'current_profile_path') or not self.current_profile_path:
            # No current profile, use save as
            self.on_save_profile_as()
            return
        
        # Emit signal to save profile
        self.save_profile_signal.emit(self.current_profile_path)
    
    def on_save_profile_as(self):
        """Handle save profile as action"""
        # Create a profile dialog
        dialog = ProfileDialog(self, mode=ProfileDialog.Mode.SAVE)
        
        # Show the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the selected profile path
            profile_path = dialog.get_selected_profile_path()
            
            # Save the current profile path
            self.current_profile_path = profile_path
            
            # Emit signal to save profile
            self.save_profile_signal.emit(profile_path)
    
    def on_settings(self):
        """Handle settings action"""
        # Create a settings dialog
        dialog = SettingsDialog(self)
        
        # Show the dialog
        dialog.exec()
    
    def on_about(self):
        """Handle about action"""
        QMessageBox.about(
            self, "About Thamyris",
            "Thamyris - Soundboard for Roleplaying\n\n"
            "A feature-rich, customizable soundboard application designed for online roleplaying groups.\n"
            "Named after the Greek bard who challenged the Muses.\n\n"
            "Version 1.0.0"
        )
    
    def update_channel_list(self, channels):
        """Update the voice channel dropdown list"""
        self.channel_combo.clear()
        
        for channel in channels:
            self.channel_combo.addItem(f"{channel['server']} - {channel['name']}", channel['id'])

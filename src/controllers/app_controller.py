"""
App controller - Main application controller
"""
import os
import threading
import asyncio
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from models.settings import Settings, Theme
from models.profile import Profile, Tab
from models.sound import Sound, ChannelType, PlaybackMode
from models.audio_player import AudioPlayer
from models.sound_file_manager import SoundFileManager
from models.profile_manager import ProfileManager
from models.theme_file_manager import ThemeFileManager
from controllers.discord_integration import DiscordIntegration
from views.main_window import MainWindow
from views.theme_manager import ThemeManager


class AppController(QObject):
    """Main application controller"""
    
    # Signals
    channels_updated = pyqtSignal(list)  # List of available voice channels
    
    def __init__(self):
        super().__init__()
        
        # Get base directory
        self.base_directory = os.getcwd()
        
        # Initialize file managers
        self.sound_file_manager = SoundFileManager(self.base_directory)
        self.profile_manager = ProfileManager(self.base_directory)
        self.theme_file_manager = ThemeFileManager(self.base_directory)
        
        # Initialize models
        self.settings = self.load_settings()
        self.profile = self.load_last_profile() or Profile.create_empty()
        self.discord_integration = DiscordIntegration()
        self.audio_player = AudioPlayer(self.settings.master_volume)
        
        # Initialize views
        self.main_window = MainWindow()
        
        # Connect signals and slots
        self.connect_signals()
    
    def connect_signals(self):
        """Connect signals and slots"""
        # Main window signals
        self.main_window.connect_discord_signal.connect(self.connect_discord)
        self.main_window.disconnect_discord_signal.connect(self.disconnect_discord)
        self.main_window.play_sound_signal.connect(self.play_sound)
        self.main_window.stop_sound_signal.connect(self.stop_sound)
        self.main_window.stop_all_sounds_signal.connect(self.stop_all_sounds)
        self.main_window.load_profile_signal.connect(self.load_profile)
        self.main_window.save_profile_signal.connect(self.save_profile)
        self.main_window.master_volume_changed_signal.connect(self.set_master_volume)
        
        # Channel mixer signals
        self.main_window.channel_mixer.channel_volume_changed.connect(self.set_channel_volume)
        self.main_window.channel_mixer.voice_ducking_toggled.connect(self.set_voice_ducking_enabled)
        self.main_window.channel_mixer.voice_ducking_amount_changed.connect(self.set_voice_ducking_amount)
        
        # Ambient player signals
        self.main_window.ambient_player.play_ambient_signal.connect(self.play_ambient)
        self.main_window.ambient_player.stop_ambient_signal.connect(self.stop_ambient)
        self.main_window.ambient_player.add_ambient_signal.connect(self.add_ambient)
        
        # Controller signals
        self.channels_updated.connect(self.main_window.update_channel_list)
    
    def start(self):
        """Start the application"""
        # Start the audio player
        self.audio_player.start()
        
        # Start the Discord integration
        self.discord_integration.start_bot()
        
        # Apply settings
        self.apply_settings()
        
        # Load the profile
        self.apply_profile()
        
        # Show the main window
        self.main_window.show()
        
        # Schedule a task to update the channel list
        threading.Timer(2.0, self.update_channel_list).start()
    
    def load_settings(self):
        """Load application settings"""
        settings_dir = os.path.join(os.getcwd(), 'resources', 'settings')
        os.makedirs(settings_dir, exist_ok=True)
        
        settings_path = os.path.join(settings_dir, 'settings.json')
        return Settings.load_from_file(settings_path)
    
    def save_settings(self):
        """Save application settings"""
        settings_dir = os.path.join(os.getcwd(), 'resources', 'settings')
        os.makedirs(settings_dir, exist_ok=True)
        
        settings_path = os.path.join(settings_dir, 'settings.json')
        self.settings.save_to_file(settings_path)
    
    def apply_settings(self):
        """Apply settings to the application"""
        # Apply theme
        ThemeManager.apply_theme(self.settings.theme)
        
        # Set audio player settings
        self.audio_player.set_master_volume(self.settings.master_volume)
        self.audio_player.set_channel_volume(ChannelType.AMBIENT, self.settings.ambient_volume)
        self.audio_player.set_channel_volume(ChannelType.EFFECTS_1, self.settings.effects_volume)
        self.audio_player.set_channel_volume(ChannelType.EFFECTS_2, self.settings.effects_volume)
        self.audio_player.set_channel_volume(ChannelType.EFFECTS_3, self.settings.effects_volume)
        self.audio_player.set_voice_ducking(True, self.settings.voice_ducking_amount)
        
        # Update UI
        self.main_window.master_volume_slider.setValue(int(self.settings.master_volume * 100))
        self.main_window.channel_mixer.set_channel_volume(ChannelType.AMBIENT, self.settings.ambient_volume)
        self.main_window.channel_mixer.set_channel_volume(ChannelType.EFFECTS_1, self.settings.effects_volume)
        self.main_window.channel_mixer.set_channel_volume(ChannelType.EFFECTS_2, self.settings.effects_volume)
        self.main_window.channel_mixer.set_channel_volume(ChannelType.EFFECTS_3, self.settings.effects_volume)
        self.main_window.channel_mixer.set_voice_ducking(True, self.settings.voice_ducking_amount)
        
        # Apply font settings
        from PyQt6.QtGui import QFont
        font = QFont(self.settings.font_family, self.settings.font_size)
        self.main_window.setFont(font)
    
    def load_last_profile(self):
        """Load the last used profile"""
        if not self.settings.last_profile:
            return None
        
        return Profile.load_from_file(self.settings.last_profile)
    
    def load_profile(self, file_path):
        """Load a profile from a file"""
        profile = self.profile_manager.load_profile(file_path)
        if profile:
            self.profile = profile
            self.settings.last_profile = file_path
            self.save_settings()
            self.apply_profile()
            
            # Update main window title
            profile_name = os.path.basename(file_path).split('.')[0]
            self.main_window.setWindowTitle(f"Thamyris - {profile_name}")
            
            # Show confirmation message
            self.main_window.statusBar().showMessage(f"Profile loaded: {profile_name}", 3000)
    
    def save_profile(self, file_path):
        """Save the current profile to a file"""
        # Update profile from UI
        self.update_profile_from_ui()
        
        # Save the profile
        self.profile_manager.save_profile(self.profile, os.path.basename(file_path).split('.')[0])
        
        # Update settings
        self.settings.last_profile = file_path
        self.save_settings()
        
        # Update main window title
        self.main_window.setWindowTitle(f"Thamyris - {os.path.basename(file_path).split('.')[0]}")
        
        # Show confirmation message
        self.main_window.statusBar().showMessage(f"Profile saved: {os.path.basename(file_path)}", 3000)
    
    def update_profile_from_ui(self):
        """Update the profile from the UI state"""
        # Get the active tab index
        self.profile.active_tab_index = self.main_window.tab_widget.currentIndex()
        
        # Clear existing tabs in the profile
        self.profile.tabs.clear()
        
        # Iterate through all tabs in the UI
        for tab_index in range(self.main_window.tab_widget.count()):
            tab_name = self.main_window.tab_widget.tabText(tab_index)
            tab = Tab(name=tab_name)
            
            # Get the tab's scroll area
            scroll = self.main_window.tab_widget.widget(tab_index)
            
            # Get the tab content widget
            tab_content = scroll.widget()
            
            # Get all sound buttons in the tab
            for i in range(tab_content.layout().count()):
                item = tab_content.layout().itemAt(i)
                if item and item.widget():
                    button = item.widget()
                    if isinstance(button, SoundButton):
                        # Add the sound to the tab
                        tab.sounds.append(button.sound)
            
            # Add the tab to the profile
            self.profile.tabs.append(tab)
    
    def apply_profile(self):
        """Apply the profile to the UI"""
        # Clear existing tabs
        while self.main_window.tab_widget.count() > 0:
            self.main_window.tab_widget.removeTab(0)
        
        # Add tabs from profile
        for tab in self.profile.tabs:
            self.main_window.add_tab(tab.name)
            
            # Add sounds to the tab
            for sound in tab.sounds:
                self.main_window.add_sound_button(
                    self.main_window.tab_widget.count() - 1, sound
                )
        
        # Set active tab
        if self.profile.active_tab_index < self.main_window.tab_widget.count():
            self.main_window.tab_widget.setCurrentIndex(self.profile.active_tab_index)
        
        # Update ambient tracks
        self.main_window.ambient_player.update_track_list(self.profile.ambient_tracks)
        
        # Set active ambient track
        if self.profile.active_ambient_index >= 0:
            self.main_window.ambient_player.set_active_track(self.profile.active_ambient_index)
            
            # Play the active ambient track
            if self.profile.active_ambient_index < len(self.profile.ambient_tracks):
                self.play_ambient(self.profile.active_ambient_index)
    
    def update_channel_list(self):
        """Update the list of available voice channels"""
        channels = self.discord_integration.get_available_channels()
        self.channels_updated.emit(channels)
    
    def connect_discord(self, channel_id):
        """Connect to a Discord voice channel"""
        result = self.discord_integration.connect_to_channel(channel_id)
        self.main_window.set_discord_connected(result)
    
    def disconnect_discord(self):
        """Disconnect from Discord voice channel"""
        self.discord_integration.disconnect()
        self.main_window.set_discord_connected(False)
    
    def play_sound(self, sound):
        """Play a sound"""
        # Play locally
        self.audio_player.play_sound(sound)
        
        # Play on Discord if connected
        if self.discord_integration.is_connected:
            self.discord_integration.play_sound(sound)
    
    def stop_sound(self, sound_path):
        """Stop a specific sound"""
        # Stop locally
        self.audio_player.stop_sound(sound_path)
        
        # Stop on Discord
        if self.discord_integration.is_connected:
            self.discord_integration.stop_sound(sound_path)
    
    def stop_all_sounds(self):
        """Stop all sounds"""
        # Stop locally
        self.audio_player.stop_all_sounds()
        
        # Stop on Discord
        if self.discord_integration.is_connected:
            self.discord_integration.stop_all_sounds()
    
    def set_channel_volume(self, channel_type, volume):
        """Set the volume for a channel"""
        # Update audio player
        self.audio_player.set_channel_volume(channel_type, volume)
        
        # Update settings based on channel type
        if channel_type == ChannelType.AMBIENT:
            self.settings.ambient_volume = volume
        else:
            self.settings.effects_volume = volume
        
        # Save settings
        self.save_settings()
    
    def set_voice_ducking_enabled(self, enabled):
        """Enable or disable voice ducking"""
        # Update audio player
        self.audio_player.set_voice_ducking(enabled, self.settings.voice_ducking_amount)
        
        # Update settings
        self.settings.voice_ducking_enabled = enabled
        self.save_settings()
    
    def set_voice_ducking_amount(self, amount):
        """Set the voice ducking amount"""
        # Update audio player
        self.audio_player.set_voice_ducking(True, amount)
        
        # Update settings
        self.settings.voice_ducking_amount = amount
        self.save_settings()
    
    def set_master_volume(self, volume):
        """Set the master volume"""
        # Update audio player
        self.audio_player.set_master_volume(volume)
        
        # Update settings
        self.settings.master_volume = volume
        self.save_settings()
    
    def play_ambient(self, index):
        """Play an ambient track"""
        if index < 0 or index >= len(self.profile.ambient_tracks):
            return
        
        # Stop any current ambient
        self.stop_ambient()
        
        # Play the new ambient
        sound = self.profile.ambient_tracks[index]
        sound.playback_mode = PlaybackMode.LOOP
        self.play_sound(sound)
        
        # Update profile
        self.profile.active_ambient_index = index
    
    def stop_ambient(self):
        """Stop the ambient track"""
        if self.profile.active_ambient_index >= 0 and self.profile.active_ambient_index < len(self.profile.ambient_tracks):
            sound = self.profile.ambient_tracks[self.profile.active_ambient_index]
            self.stop_sound(sound.file_path)
        
        # Update profile
        self.profile.active_ambient_index = -1
    
    def add_ambient(self, file_path):
        """Add an ambient track"""
        # Import the sound file to the application's directory
        success, new_path = self.sound_file_manager.import_sound_file(file_path, is_ambient=True)
        if not success:
            return
            
        # Create a new sound
        sound = Sound(
            name=os.path.basename(new_path),
            file_path=new_path,
            channel=ChannelType.AMBIENT,
            playback_mode=PlaybackMode.LOOP
        )
        
        # Add to profile
        self.profile.ambient_tracks.append(sound)
        
        # Update UI
        self.main_window.ambient_player.update_track_list(self.profile.ambient_tracks)

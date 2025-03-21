"""
Discord bot integration module - Connects the Discord bot with the application
"""
import os
import asyncio
import threading
from typing import Optional, List, Dict, Any, Callable

from models.sound import Sound
from discord_bot import SoundboardBot

class DiscordIntegration:
    """Class for integrating the Discord bot with the application"""
    
    def __init__(self):
        """Initialize the Discord integration"""
        self.bot: Optional[SoundboardBot] = None
        self.bot_thread: Optional[threading.Thread] = None
        self.is_connected = False
        self.current_channel_id = None
        self.loop = asyncio.new_event_loop()
    
    def start_bot(self):
        """Start the Discord bot in a separate thread"""
        if self.bot_thread and self.bot_thread.is_alive():
            return
        
        def run_bot_thread():
            asyncio.set_event_loop(self.loop)
            self.bot = self.loop.run_until_complete(self._create_and_start_bot())
        
        self.bot_thread = threading.Thread(target=run_bot_thread, daemon=True)
        self.bot_thread.start()
    
    async def _create_and_start_bot(self):
        """Create and start the Discord bot"""
        from discord_bot import run_bot
        return await run_bot()
    
    def connect_to_channel(self, channel_id: str) -> bool:
        """Connect to a voice channel"""
        if not self.bot:
            return False
        
        self.current_channel_id = channel_id
        
        # Get the channel
        channel = None
        for guild in self.bot.guilds:
            for voice_channel in guild.voice_channels:
                if str(voice_channel.id) == channel_id:
                    channel = voice_channel
                    break
            if channel:
                break
        
        if not channel:
            return False
        
        # Connect to the channel
        future = asyncio.run_coroutine_threadsafe(
            self.bot.join_voice_channel(channel),
            self.loop
        )
        
        try:
            future.result(timeout=10)
            self.is_connected = True
            return True
        except Exception as e:
            print(f"Error connecting to voice channel: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the voice channel"""
        if not self.bot:
            return
        
        future = asyncio.run_coroutine_threadsafe(
            self.bot.leave_voice_channel(),
            self.loop
        )
        
        try:
            future.result(timeout=5)
            self.is_connected = False
            self.current_channel_id = None
        except Exception as e:
            print(f"Error disconnecting from voice channel: {e}")
    
    def play_sound(self, sound: Sound) -> bool:
        """Play a sound in the voice channel"""
        if not self.bot or not self.is_connected:
            return False
        
        # Check if the bot is connected to a voice channel
        if not self.bot.voice_client or not self.bot.voice_client.is_connected():
            return False
        
        # Play the sound
        return self.bot.play_sound(
            sound.file_path,
            volume=sound.volume,
            loop=sound.playback_mode.value == 2  # PlaybackMode.LOOP
        )
    
    def stop_sound(self, sound_path: str):
        """Stop a specific sound"""
        if not self.bot or not self.is_connected:
            return
        
        self.bot.stop_sound(os.path.basename(sound_path))
    
    def stop_all_sounds(self):
        """Stop all sounds"""
        if not self.bot or not self.is_connected:
            return
        
        self.bot.stop_all_sounds()
    
    def get_available_channels(self) -> List[Dict[str, Any]]:
        """Get a list of available voice channels"""
        if not self.bot:
            return []
        
        future = asyncio.run_coroutine_threadsafe(
            asyncio.to_thread(self.bot.get_available_channels),
            self.loop
        )
        
        try:
            return future.result(timeout=5)
        except Exception as e:
            print(f"Error getting available channels: {e}")
            return []

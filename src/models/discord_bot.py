"""
Discord bot model - Handles Discord integration and audio playback
"""
import asyncio
import os
from typing import Optional, Dict, List, Callable, Any
import discord
from discord.ext import commands

class DiscordBot:
    """Class for handling Discord integration and audio playback"""
    def __init__(self):
        """Initialize the Discord bot"""
        self.token = os.getenv('DISCORD_BOT_TOKEN', '')
        self.guild_id = os.getenv('DISCORD_GUILD_ID', '')
        self.bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        self.voice_client: Optional[discord.VoiceClient] = None
        self.audio_players: Dict[str, discord.AudioSource] = {}
        self.is_connected = False
        self.channel_id = None
        self.setup_events()
    
    def setup_events(self):
        """Set up Discord bot event handlers"""
        @self.bot.event
        async def on_ready():
            print(f'Bot logged in as {self.bot.user}')
            self.is_connected = True
        
        @self.bot.event
        async def on_voice_state_update(member, before, after):
            # Handle voice state updates if needed
            pass
    
    async def connect(self, channel_id: str) -> bool:
        """Connect to a voice channel"""
        try:
            if self.voice_client and self.voice_client.is_connected():
                await self.voice_client.disconnect()
            
            self.channel_id = channel_id
            channel = self.bot.get_channel(int(channel_id))
            if not channel:
                print(f"Channel {channel_id} not found")
                return False
            
            self.voice_client = await channel.connect()
            return True
        except Exception as e:
            print(f"Error connecting to voice channel: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from voice channel"""
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            self.voice_client = None
            self.channel_id = None
    
    async def play_sound(self, file_path: str, channel_id: str = None, 
                         volume: float = 1.0, loop: bool = False, 
                         after: Callable = None) -> bool:
        """Play a sound in the voice channel"""
        try:
            if channel_id and channel_id != self.channel_id:
                await self.connect(channel_id)
            
            if not self.voice_client or not self.voice_client.is_connected():
                print("Not connected to a voice channel")
                return False
            
            # Stop any existing audio on this source if needed
            source_id = os.path.basename(file_path)
            if source_id in self.audio_players:
                self.stop_sound(source_id)
            
            # Create audio source
            audio_source = discord.FFmpegPCMAudio(file_path)
            audio_source = discord.PCMVolumeTransformer(audio_source, volume=volume)
            
            # Store the audio source
            self.audio_players[source_id] = audio_source
            
            # Play the audio
            self.voice_client.play(audio_source, after=after)
            return True
        except Exception as e:
            print(f"Error playing sound: {e}")
            return False
    
    def stop_sound(self, source_id: str):
        """Stop a specific sound"""
        if source_id in self.audio_players:
            if self.voice_client and self.voice_client.is_playing():
                self.voice_client.stop()
            del self.audio_players[source_id]
    
    def stop_all_sounds(self):
        """Stop all sounds"""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
        self.audio_players.clear()
    
    async def start_bot(self):
        """Start the Discord bot"""
        if not self.token:
            print("Discord bot token not found in environment variables")
            return False
        
        try:
            await self.bot.start(self.token)
            return True
        except Exception as e:
            print(f"Error starting Discord bot: {e}")
            return False
    
    def run_async(self, coro):
        """Run a coroutine in the bot's event loop"""
        return asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
    
    def get_available_channels(self) -> List[Dict[str, Any]]:
        """Get a list of available voice channels"""
        channels = []
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                channels.append({
                    'id': str(channel.id),
                    'name': channel.name,
                    'guild': guild.name
                })
        return channels

"""
Discord bot implementation - Handles Discord API integration
"""
import os
import asyncio
import logging
from typing import Optional, Dict, List, Callable, Any

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord_bot')

class SoundboardBot(commands.Bot):
    """Discord bot for soundboard functionality"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix='!', intents=intents)
        
        # Add commands
        self.add_command(commands.Command(self.cmd_join, name='join', help='Join a voice channel'))
        self.add_command(commands.Command(self.cmd_leave, name='leave', help='Leave the voice channel'))
        self.add_command(commands.Command(self.cmd_stop, name='stop', help='Stop all playing sounds'))
        
        # Voice client
        self.voice_client: Optional[discord.VoiceClient] = None
        self.audio_players: Dict[str, discord.AudioSource] = {}
    
    async def cmd_join(self, ctx):
        """Join command handler"""
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel.")
            return
        
        channel = ctx.author.voice.channel
        await self.join_voice_channel(channel)
        await ctx.send(f"Joined {channel.name}")
    
    async def cmd_leave(self, ctx):
        """Leave command handler"""
        if self.voice_client is None:
            await ctx.send("I am not connected to a voice channel.")
            return
        
        await self.leave_voice_channel()
        await ctx.send("Left voice channel")
    
    async def cmd_stop(self, ctx):
        """Stop command handler"""
        if self.voice_client is None:
            await ctx.send("I am not connected to a voice channel.")
            return
        
        self.stop_all_sounds()
        await ctx.send("Stopped all sounds")
    
    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')
    
    async def join_voice_channel(self, channel):
        """Join a voice channel"""
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
        
        self.voice_client = await channel.connect()
        logger.info(f'Connected to voice channel: {channel.name}')
    
    async def leave_voice_channel(self):
        """Leave the voice channel"""
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
            self.audio_players.clear()
            logger.info('Disconnected from voice channel')
    
    def play_sound(self, file_path: str, volume: float = 1.0, loop: bool = False):
        """Play a sound in the voice channel"""
        if self.voice_client is None or not self.voice_client.is_connected():
            logger.warning('Not connected to a voice channel')
            return False
        
        try:
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
            self.voice_client.play(
                audio_source, 
                after=lambda e: logger.error(f'Player error: {e}') if e else None
            )
            
            logger.info(f'Playing sound: {file_path}')
            return True
        except Exception as e:
            logger.error(f'Error playing sound: {e}')
            return False
    
    def stop_sound(self, source_id: str):
        """Stop a specific sound"""
        if source_id in self.audio_players:
            if self.voice_client and self.voice_client.is_playing():
                self.voice_client.stop()
            del self.audio_players[source_id]
            logger.info(f'Stopped sound: {source_id}')
    
    def stop_all_sounds(self):
        """Stop all sounds"""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
        self.audio_players.clear()
        logger.info('Stopped all sounds')
    
    def get_available_channels(self) -> List[Dict[str, Any]]:
        """Get a list of available voice channels"""
        channels = []
        for guild in self.guilds:
            for channel in guild.voice_channels:
                channels.append({
                    'id': str(channel.id),
                    'name': channel.name,
                    'guild': guild.name
                })
        return channels


async def run_bot():
    """Run the Discord bot"""
    # Load environment variables
    load_dotenv()
    
    # Get token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error('DISCORD_BOT_TOKEN not found in environment variables')
        return None
    
    # Create and start the bot
    bot = SoundboardBot()
    try:
        await bot.start(token)
    except Exception as e:
        logger.error(f'Error starting bot: {e}')
        return None
    
    return bot


if __name__ == '__main__':
    # Run the bot directly for testing
    asyncio.run(run_bot())

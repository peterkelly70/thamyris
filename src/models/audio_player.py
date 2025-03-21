"""
Audio player model - Handles audio playback and mixing
"""
import os
import threading
import time
from typing import Dict, List, Optional, Callable
import sounddevice as sd
import soundfile as sf
import numpy as np

from models.sound import Sound, PlaybackMode, ChannelType
from models.audio_fade_controller import AudioFadeController, FadeType


class AudioChannel:
    """Class representing an audio channel for mixing"""
    def __init__(self, channel_type: ChannelType, volume: float = 1.0):
        self.channel_type = channel_type
        self.volume = volume
        self.active_sounds: Dict[str, Dict] = {}  # sound_id -> sound info
    
    def add_sound(self, sound_id: str, sound: Sound, buffer: np.ndarray, 
                  sample_rate: int, callback: Optional[Callable] = None):
        """Add a sound to the channel"""
        self.active_sounds[sound_id] = {
            'sound': sound,
            'buffer': buffer,
            'sample_rate': sample_rate,
            'position': 0,
            'callback': callback
        }
    
    def remove_sound(self, sound_id: str):
        """Remove a sound from the channel"""
        if sound_id in self.active_sounds:
            del self.active_sounds[sound_id]
    
    def get_mixed_audio(self, frames: int, sample_rate: int) -> np.ndarray:
        """Get mixed audio for this channel"""
        if not self.active_sounds:
            return np.zeros((frames, 2))
        
        # Mix all active sounds
        mixed = np.zeros((frames, 2))
        sounds_to_remove = []
        
        for sound_id, sound_info in self.active_sounds.items():
            buffer = sound_info['buffer']
            position = sound_info['position']
            sound = sound_info['sound']
            
            # Calculate how many frames to read
            frames_left = len(buffer) - position
            frames_to_read = min(frames, frames_left)
            
            if frames_to_read > 0:
                # Add the audio to the mix
                chunk = buffer[position:position+frames_to_read]
                if len(chunk.shape) == 1:  # Mono
                    chunk = np.column_stack((chunk, chunk))
                elif chunk.shape[1] == 1:  # Mono as (n, 1)
                    chunk = np.column_stack((chunk[:, 0], chunk[:, 0]))
                
                # Apply volume
                chunk = chunk * sound.volume * self.volume
                
                # Add to mix (only the frames we have)
                mixed[:frames_to_read] += chunk
                
                # Update position
                sound_info['position'] = position + frames_to_read
            
            # Check if we've reached the end
            if sound_info['position'] >= len(buffer):
                # Handle looping
                if sound.playback_mode == PlaybackMode.LOOP:
                    sound_info['position'] = 0
                else:
                    sounds_to_remove.append(sound_id)
                    if sound_info['callback']:
                        sound_info['callback'](sound_id)
        
        # Remove finished sounds
        for sound_id in sounds_to_remove:
            self.remove_sound(sound_id)
        
        return mixed


class AudioPlayer:
    """Class for handling audio playback and mixing"""
    def __init__(self, master_volume: float = 0.8):
        self.master_volume = master_volume
        self.channels: Dict[ChannelType, AudioChannel] = {
            ChannelType.AMBIENT: AudioChannel(ChannelType.AMBIENT, 0.5),
            ChannelType.EFFECTS_1: AudioChannel(ChannelType.EFFECTS_1, 0.7),
            ChannelType.EFFECTS_2: AudioChannel(ChannelType.EFFECTS_2, 0.7),
            ChannelType.EFFECTS_3: AudioChannel(ChannelType.EFFECTS_3, 0.7)
        }
        self.sample_rate = 44100
        self.stream = None
        self.is_playing = False
        self.sound_buffers: Dict[str, np.ndarray] = {}
        self.sound_sample_rates: Dict[str, int] = {}
        self.lock = threading.Lock()
        self.voice_ducking_enabled = True
        self.voice_ducking_amount = 0.5
        self.fade_controller = AudioFadeController()
    
    def start(self):
        """Start the audio playback"""
        if self.stream is not None:
            return
        
        def callback(outdata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            
            with self.lock:
                # Get audio from each channel
                ambient = self.channels[ChannelType.AMBIENT].get_mixed_audio(frames, self.sample_rate)
                effects1 = self.channels[ChannelType.EFFECTS_1].get_mixed_audio(frames, self.sample_rate)
                effects2 = self.channels[ChannelType.EFFECTS_2].get_mixed_audio(frames, self.sample_rate)
                effects3 = self.channels[ChannelType.EFFECTS_3].get_mixed_audio(frames, self.sample_rate)
                
                # Apply voice ducking if enabled
                if self.voice_ducking_enabled and (
                    np.any(effects1) or np.any(effects2) or np.any(effects3)
                ):
                    ducking_factor = 1.0 - self.voice_ducking_amount
                    ambient = ambient * ducking_factor
                
                # Mix all channels
                mixed = ambient + effects1 + effects2 + effects3
                
                # Apply master volume
                mixed = mixed * self.master_volume
                
                # Clip to prevent distortion
                mixed = np.clip(mixed, -1.0, 1.0)
                
                # Output the audio
                outdata[:] = mixed
        
        self.stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=2,
            callback=callback
        )
        self.stream.start()
        self.is_playing = True
    
    def stop(self):
        """Stop the audio playback"""
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            self.is_playing = False
    
    def load_sound(self, sound: Sound) -> bool:
        """Load a sound file into memory"""
        try:
            if not os.path.exists(sound.file_path):
                print(f"Sound file not found: {sound.file_path}")
                return False
            
            data, sample_rate = sf.read(sound.file_path)
            
            # Apply fade in/out if enabled
            if sound.fade_in_enabled and sound.fade_in_duration > 0:
                self.fade_controller.set_fade_in_duration(sound.fade_in_duration)
                self.fade_controller.set_fade_type(FadeType.LINEAR)
                data = self.fade_controller.apply_fade_in(data, sample_rate)
            
            if sound.fade_out_enabled and sound.fade_out_duration > 0:
                self.fade_controller.set_fade_out_duration(sound.fade_out_duration)
                self.fade_controller.set_fade_type(FadeType.LINEAR)
                data = self.fade_controller.apply_fade_out(data, sample_rate)
            
            # Store the buffer and sample rate
            self.sound_buffers[sound.file_path] = data
            self.sound_sample_rates[sound.file_path] = sample_rate
            
            return True
        except Exception as e:
            print(f"Error loading sound: {e}")
            return False
    
    def play_sound(self, sound: Sound, callback: Optional[Callable] = None) -> bool:
        """Play a sound"""
        try:
            # Make sure the audio engine is running
            if not self.is_playing:
                self.start()
            
            # Load the sound if not already loaded
            if sound.file_path not in self.sound_buffers:
                if not self.load_sound(sound):
                    return False
            
            # Get the buffer and sample rate
            buffer = self.sound_buffers[sound.file_path]
            sample_rate = self.sound_sample_rates[sound.file_path]
            
            # Add the sound to the appropriate channel
            with self.lock:
                self.channels[sound.channel].add_sound(
                    sound.file_path, sound, buffer, sample_rate, callback
                )
            
            return True
        except Exception as e:
            print(f"Error playing sound: {e}")
            return False
    
    def stop_sound(self, sound_path: str):
        """Stop a specific sound"""
        with self.lock:
            for channel in self.channels.values():
                channel.remove_sound(sound_path)
    
    def stop_all_sounds(self):
        """Stop all sounds"""
        with self.lock:
            for channel in self.channels.values():
                channel.active_sounds.clear()
    
    def set_channel_volume(self, channel_type: ChannelType, volume: float):
        """Set the volume for a channel"""
        with self.lock:
            self.channels[channel_type].volume = max(0.0, min(1.0, volume))
    
    def set_master_volume(self, volume: float):
        """Set the master volume"""
        with self.lock:
            self.master_volume = max(0.0, min(1.0, volume))
    
    def set_voice_ducking(self, enabled: bool, amount: float = 0.5):
        """Set voice ducking settings"""
        with self.lock:
            self.voice_ducking_enabled = enabled
            self.voice_ducking_amount = max(0.0, min(1.0, amount))
    
    def set_fade_in_duration(self, duration: float):
        """Set the default fade in duration"""
        self.fade_controller.set_fade_in_duration(duration)
    
    def set_fade_out_duration(self, duration: float):
        """Set the default fade out duration"""
        self.fade_controller.set_fade_out_duration(duration)
    
    def set_fade_type(self, fade_type: FadeType):
        """Set the fade type"""
        self.fade_controller.set_fade_type(fade_type)

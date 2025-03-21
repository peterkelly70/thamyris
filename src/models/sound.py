"""
Sound model - Represents a sound effect or ambient track
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Set
import os
from pathlib import Path


class PlaybackMode(Enum):
    """Enum for different playback modes"""
    PLAY_ONCE = 0
    PLAY_N_TIMES = 1
    LOOP = 2


class ChannelType(Enum):
    """Enum for different channel types"""
    AMBIENT = 0
    EFFECTS_1 = 1
    EFFECTS_2 = 2
    EFFECTS_3 = 3


@dataclass
class Sound:
    """Class representing a sound effect or ambient track"""
    name: str
    file_path: str
    channel: ChannelType = ChannelType.EFFECTS_1
    volume: float = 1.0
    playback_mode: PlaybackMode = PlaybackMode.PLAY_ONCE
    repeat_count: int = 1
    fade_in: int = 0  # milliseconds
    fade_out: int = 0  # milliseconds
    fade_in_enabled: bool = False
    fade_out_enabled: bool = False
    color: str = "#3498db"  # Default button color
    tags: List[str] = field(default_factory=list)  # List of tags for the sound
    hotkey: Optional[str] = None  # Hotkey for triggering this sound
    
    @property
    def file_exists(self) -> bool:
        """Check if the sound file exists"""
        return os.path.isfile(self.file_path)
    
    @property
    def file_extension(self) -> str:
        """Get the file extension"""
        return Path(self.file_path).suffix.lower()
    
    @property
    def is_valid_audio_file(self) -> bool:
        """Check if the file is a valid audio file"""
        valid_extensions = ['.mp3', '.wav', '.ogg', '.flac']
        return self.file_exists and self.file_extension in valid_extensions
    
    def add_tag(self, tag: str):
        """Add a tag to the sound"""
        # Convert to lowercase and strip whitespace
        tag = tag.lower().strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the sound"""
        tag = tag.lower().strip()
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if the sound has a specific tag"""
        return tag.lower().strip() in self.tags
    
    def add_tags_from_string(self, tags_string: str):
        """Add multiple tags from a comma-separated string"""
        if not tags_string:
            return
            
        # Split by comma and process each tag
        for tag in tags_string.split(','):
            self.add_tag(tag)
    
    def get_tags_as_string(self) -> str:
        """Get tags as a comma-separated string"""
        return ','.join(self.tags)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the sound to a dictionary for serialization"""
        return {
            'name': self.name,
            'file_path': self.file_path,
            'channel': self.channel.value,
            'volume': self.volume,
            'playback_mode': self.playback_mode.value,
            'repeat_count': self.repeat_count,
            'fade_in': self.fade_in,
            'fade_out': self.fade_out,
            'fade_in_enabled': self.fade_in_enabled,
            'fade_out_enabled': self.fade_out_enabled,
            'color': self.color,
            'tags': self.tags,
            'hotkey': self.hotkey
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sound':
        """Create a Sound object from a dictionary"""
        sound = cls(
            name=data['name'],
            file_path=data['file_path'],
            channel=ChannelType(data['channel']),
            volume=data['volume'],
            playback_mode=PlaybackMode(data['playback_mode']),
            repeat_count=data['repeat_count'],
            fade_in=data['fade_in'],
            fade_out=data['fade_out'],
            color=data['color']
        )
        
        # Add optional properties if present
        if 'fade_in_enabled' in data:
            sound.fade_in_enabled = data['fade_in_enabled']
        if 'fade_out_enabled' in data:
            sound.fade_out_enabled = data['fade_out_enabled']
        if 'hotkey' in data:
            sound.hotkey = data['hotkey']
        
        # Add tags if present
        if 'tags' in data:
            sound.tags = data['tags']
            
        return sound

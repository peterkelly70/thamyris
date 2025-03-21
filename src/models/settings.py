"""
Settings model - Represents application settings and preferences
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
import os
from enum import Enum


class Theme(Enum):
    """Enum for different UI themes"""
    LIGHT = "light"
    DARK = "dark"
    CUSTOM = "custom"


@dataclass
class Settings:
    """Class representing application settings and preferences"""
    theme: Theme = Theme.DARK
    font_size: int = 10
    font_family: str = "Arial"
    master_volume: float = 0.8
    ambient_volume: float = 0.5
    effects_volume: float = 0.7
    voice_ducking_amount: float = 0.5
    fade_in_duration: int = 1000  # milliseconds
    fade_out_duration: int = 1000  # milliseconds
    last_profile: str = ""
    hotkeys: Dict[str, str] = None
    
    def __post_init__(self):
        """Initialize default values for mutable fields"""
        if self.hotkeys is None:
            self.hotkeys = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the settings to a dictionary for serialization"""
        return {
            'theme': self.theme.value,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'master_volume': self.master_volume,
            'ambient_volume': self.ambient_volume,
            'effects_volume': self.effects_volume,
            'voice_ducking_amount': self.voice_ducking_amount,
            'fade_in_duration': self.fade_in_duration,
            'fade_out_duration': self.fade_out_duration,
            'last_profile': self.last_profile,
            'hotkeys': self.hotkeys
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Settings':
        """Create a Settings object from a dictionary"""
        return cls(
            theme=Theme(data.get('theme', Theme.DARK.value)),
            font_size=data.get('font_size', 10),
            font_family=data.get('font_family', 'Arial'),
            master_volume=data.get('master_volume', 0.8),
            ambient_volume=data.get('ambient_volume', 0.5),
            effects_volume=data.get('effects_volume', 0.7),
            voice_ducking_amount=data.get('voice_ducking_amount', 0.5),
            fade_in_duration=data.get('fade_in_duration', 1000),
            fade_out_duration=data.get('fade_out_duration', 1000),
            last_profile=data.get('last_profile', ''),
            hotkeys=data.get('hotkeys', {})
        )
    
    def save_to_file(self, file_path: str) -> bool:
        """Save the settings to a file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'Settings':
        """Load settings from a file, or create default settings if file doesn't exist"""
        try:
            if not os.path.exists(file_path):
                return cls()
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return cls()

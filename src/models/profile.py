"""
Profile model - Represents a saved soundboard configuration
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
import os
from pathlib import Path

from models.sound import Sound


@dataclass
class Tab:
    """Class representing a tab in the soundboard"""
    name: str
    sounds: List[Sound]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the tab to a dictionary for serialization"""
        return {
            'name': self.name,
            'sounds': [sound.to_dict() for sound in self.sounds]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tab':
        """Create a Tab object from a dictionary"""
        return cls(
            name=data['name'],
            sounds=[Sound.from_dict(sound_data) for sound_data in data['sounds']]
        )


@dataclass
class Profile:
    """Class representing a saved soundboard configuration"""
    name: str
    tabs: List[Tab]
    ambient_tracks: List[Sound]
    active_tab_index: int = 0
    active_ambient_index: int = -1  # -1 means no ambient track is active
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the profile to a dictionary for serialization"""
        return {
            'name': self.name,
            'tabs': [tab.to_dict() for tab in self.tabs],
            'ambient_tracks': [track.to_dict() for track in self.ambient_tracks],
            'active_tab_index': self.active_tab_index,
            'active_ambient_index': self.active_ambient_index
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        """Create a Profile object from a dictionary"""
        return cls(
            name=data['name'],
            tabs=[Tab.from_dict(tab_data) for tab_data in data['tabs']],
            ambient_tracks=[Sound.from_dict(track_data) for track_data in data['ambient_tracks']],
            active_tab_index=data.get('active_tab_index', 0),
            active_ambient_index=data.get('active_ambient_index', -1)
        )
    
    def save_to_file(self, file_path: str) -> bool:
        """Save the profile to a file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, file_path: str) -> Optional['Profile']:
        """Load a profile from a file"""
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    @classmethod
    def create_empty(cls, name: str = "New Profile") -> 'Profile':
        """Create an empty profile"""
        return cls(
            name=name,
            tabs=[Tab(name="General", sounds=[])],
            ambient_tracks=[]
        )

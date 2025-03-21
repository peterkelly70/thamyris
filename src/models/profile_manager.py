"""
Profile manager - Handles profile file operations
"""
import os
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from models.profile import Profile

class ProfileManager:
    """Class for managing profile files"""
    
    def __init__(self, base_directory: str):
        """Initialize the profile manager"""
        self.base_directory = base_directory
        self.profiles_directory = os.path.join(base_directory, 'resources', 'profiles')
        
        # Create directory if it doesn't exist
        os.makedirs(self.profiles_directory, exist_ok=True)
    
    def save_profile(self, profile: Profile, name: Optional[str] = None) -> str:
        """
        Save a profile to a file
        
        Args:
            profile: The profile to save
            name: Optional name to save as (defaults to profile.name)
            
        Returns:
            Path to the saved profile file
        """
        # Use provided name or profile name
        profile_name = name or profile.name
        
        # Sanitize filename
        safe_name = self._sanitize_filename(profile_name)
        
        # Create the file path
        file_path = os.path.join(self.profiles_directory, f"{safe_name}.profile")
        
        # Convert profile to JSON
        profile_data = profile.to_dict()
        
        # Save to file with pretty formatting for human readability
        with open(file_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        
        return file_path
    
    def load_profile(self, file_path: str) -> Optional[Profile]:
        """
        Load a profile from a file
        
        Args:
            file_path: Path to the profile file
            
        Returns:
            Loaded profile or None if loading failed
        """
        try:
            # Check if the file exists
            if not os.path.isfile(file_path):
                return None
            
            # Load JSON data
            with open(file_path, 'r') as f:
                profile_data = json.load(f)
            
            # Create profile from data
            return Profile.from_dict(profile_data)
        
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def get_available_profiles(self) -> List[Dict[str, str]]:
        """
        Get a list of available profiles
        
        Returns:
            List of dictionaries with 'name' and 'path' keys
        """
        profiles = []
        
        # Check if directory exists
        if not os.path.isdir(self.profiles_directory):
            return profiles
        
        # List all .profile files
        for file_name in os.listdir(self.profiles_directory):
            if file_name.endswith('.profile'):
                file_path = os.path.join(self.profiles_directory, file_name)
                profile_name = Path(file_name).stem
                
                profiles.append({
                    'name': profile_name,
                    'path': file_path
                })
        
        return profiles
    
    def delete_profile(self, file_path: str) -> bool:
        """
        Delete a profile file
        
        Args:
            file_path: Path to the profile file
            
        Returns:
            Success status
        """
        try:
            # Check if the file is within our profiles directory
            if not file_path.startswith(self.profiles_directory):
                return False
            
            # Check if the file exists
            if not os.path.isfile(file_path):
                return False
            
            # Delete the file
            os.remove(file_path)
            return True
        
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename to be safe for the filesystem
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        return filename

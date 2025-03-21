"""
Sound file manager - Handles sound file operations
"""
import os
import shutil
from pathlib import Path
import uuid
from typing import Optional, Tuple

class SoundFileManager:
    """Class for managing sound files"""
    
    def __init__(self, base_directory: str):
        """Initialize the sound file manager"""
        self.base_directory = base_directory
        self.sounds_directory = os.path.join(base_directory, 'resources', 'sounds')
        self.ambient_directory = os.path.join(base_directory, 'resources', 'ambient')
        
        # Create directories if they don't exist
        os.makedirs(self.sounds_directory, exist_ok=True)
        os.makedirs(self.ambient_directory, exist_ok=True)
    
    def import_sound_file(self, source_path: str, is_ambient: bool = False) -> Tuple[bool, str]:
        """
        Import a sound file into the application's directory structure
        
        Args:
            source_path: Path to the source sound file
            is_ambient: Whether the sound is an ambient track
            
        Returns:
            Tuple of (success, new_path)
        """
        try:
            # Check if the source file exists
            if not os.path.isfile(source_path):
                return False, f"File not found: {source_path}"
            
            # Determine the target directory
            target_dir = self.ambient_directory if is_ambient else self.sounds_directory
            
            # Generate a unique filename to avoid conflicts
            file_extension = Path(source_path).suffix
            original_filename = Path(source_path).stem
            unique_filename = f"{original_filename}_{uuid.uuid4().hex[:8]}{file_extension}"
            
            # Create the target path
            target_path = os.path.join(target_dir, unique_filename)
            
            # Copy the file
            shutil.copy2(source_path, target_path)
            
            return True, target_path
        
        except Exception as e:
            return False, f"Error importing sound file: {e}"
    
    def delete_sound_file(self, file_path: str) -> bool:
        """
        Delete a sound file from the application's directory structure
        
        Args:
            file_path: Path to the sound file to delete
            
        Returns:
            Success status
        """
        try:
            # Check if the file is within our managed directories
            if not (file_path.startswith(self.sounds_directory) or 
                    file_path.startswith(self.ambient_directory)):
                return False
            
            # Check if the file exists
            if not os.path.isfile(file_path):
                return False
            
            # Delete the file
            os.remove(file_path)
            return True
        
        except Exception as e:
            print(f"Error deleting sound file: {e}")
            return False
    
    def get_relative_path(self, file_path: str) -> str:
        """
        Get the path relative to the base directory
        
        Args:
            file_path: Absolute path to the file
            
        Returns:
            Relative path
        """
        try:
            return os.path.relpath(file_path, self.base_directory)
        except:
            return file_path
    
    def get_absolute_path(self, relative_path: str) -> str:
        """
        Get the absolute path from a relative path
        
        Args:
            relative_path: Path relative to the base directory
            
        Returns:
            Absolute path
        """
        # If it's already an absolute path, return it
        if os.path.isabs(relative_path):
            return relative_path
        
        return os.path.join(self.base_directory, relative_path)

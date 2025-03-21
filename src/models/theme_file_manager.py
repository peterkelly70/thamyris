"""
Theme manager model - Handles theme file operations
"""
import os
import json
from typing import Optional, List, Dict, Any
from pathlib import Path
from enum import Enum

from models.settings import Theme

class ThemeFile:
    """Class representing a theme file"""
    
    def __init__(self, name: str, colors: Dict[str, str]):
        """Initialize the theme file"""
        self.name = name
        self.colors = colors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the theme to a dictionary for serialization"""
        return {
            'name': self.name,
            'colors': self.colors
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThemeFile':
        """Create a ThemeFile object from a dictionary"""
        return cls(
            name=data.get('name', 'Custom Theme'),
            colors=data.get('colors', {})
        )


class ThemeFileManager:
    """Class for managing theme files"""
    
    def __init__(self, base_directory: str):
        """Initialize the theme manager"""
        self.base_directory = base_directory
        self.themes_directory = os.path.join(base_directory, 'resources', 'themes')
        
        # Create directory if it doesn't exist
        os.makedirs(self.themes_directory, exist_ok=True)
        
        # Create default themes if they don't exist
        self._create_default_themes()
    
    def _create_default_themes(self):
        """Create default themes if they don't exist"""
        # Light theme
        light_theme = ThemeFile(
            name="Light",
            colors={
                'window': '#f0f0f0',
                'windowText': '#000000',
                'base': '#ffffff',
                'alternateBase': '#f5f5f5',
                'toolTipBase': '#ffffdc',
                'toolTipText': '#000000',
                'text': '#000000',
                'button': '#f0f0f0',
                'buttonText': '#000000',
                'brightText': '#ff0000',
                'link': '#0000ff',
                'highlight': '#2a82da',
                'highlightedText': '#ffffff'
            }
        )
        
        # Dark theme
        dark_theme = ThemeFile(
            name="Dark",
            colors={
                'window': '#353535',
                'windowText': '#ffffff',
                'base': '#191919',
                'alternateBase': '#353535',
                'toolTipBase': '#353535',
                'toolTipText': '#ffffff',
                'text': '#ffffff',
                'button': '#353535',
                'buttonText': '#ffffff',
                'brightText': '#ff0000',
                'link': '#2a82da',
                'highlight': '#2a82da',
                'highlightedText': '#ffffff'
            }
        )
        
        # Save default themes if they don't exist
        light_path = os.path.join(self.themes_directory, "Light.theme")
        if not os.path.exists(light_path):
            self.save_theme(light_theme)
        
        dark_path = os.path.join(self.themes_directory, "Dark.theme")
        if not os.path.exists(dark_path):
            self.save_theme(dark_theme)
    
    def save_theme(self, theme: ThemeFile) -> str:
        """
        Save a theme to a file
        
        Args:
            theme: The theme to save
            
        Returns:
            Path to the saved theme file
        """
        # Sanitize filename
        safe_name = self._sanitize_filename(theme.name)
        
        # Create the file path
        file_path = os.path.join(self.themes_directory, f"{safe_name}.theme")
        
        # Convert theme to JSON
        theme_data = theme.to_dict()
        
        # Save to file with pretty formatting for human readability
        with open(file_path, 'w') as f:
            json.dump(theme_data, f, indent=2)
        
        return file_path
    
    def load_theme(self, file_path: str) -> Optional[ThemeFile]:
        """
        Load a theme from a file
        
        Args:
            file_path: Path to the theme file
            
        Returns:
            Loaded theme or None if loading failed
        """
        try:
            # Check if the file exists
            if not os.path.isfile(file_path):
                return None
            
            # Load JSON data
            with open(file_path, 'r') as f:
                theme_data = json.load(f)
            
            # Create theme from data
            return ThemeFile.from_dict(theme_data)
        
        except Exception as e:
            print(f"Error loading theme: {e}")
            return None
    
    def get_available_themes(self) -> List[Dict[str, str]]:
        """
        Get a list of available themes
        
        Returns:
            List of dictionaries with 'name' and 'path' keys
        """
        themes = []
        
        # Check if directory exists
        if not os.path.isdir(self.themes_directory):
            return themes
        
        # List all .theme files
        for file_name in os.listdir(self.themes_directory):
            if file_name.endswith('.theme'):
                file_path = os.path.join(self.themes_directory, file_name)
                theme_name = Path(file_name).stem
                
                themes.append({
                    'name': theme_name,
                    'path': file_path
                })
        
        return themes
    
    def delete_theme(self, file_path: str) -> bool:
        """
        Delete a theme file
        
        Args:
            file_path: Path to the theme file
            
        Returns:
            Success status
        """
        try:
            # Check if the file is within our themes directory
            if not file_path.startswith(self.themes_directory):
                return False
            
            # Check if the file exists
            if not os.path.isfile(file_path):
                return False
            
            # Delete the file
            os.remove(file_path)
            return True
        
        except Exception as e:
            print(f"Error deleting theme: {e}")
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

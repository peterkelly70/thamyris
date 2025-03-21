"""
Hotkey manager - Manages global hotkeys for the application
"""
import keyboard
import threading
from PyQt6.QtCore import QObject, pyqtSignal
from typing import Dict, Callable, Any


class HotkeyManager(QObject):
    """Class for managing global hotkeys"""
    
    # Signals
    hotkey_triggered = pyqtSignal(str)  # Hotkey name
    
    def __init__(self):
        super().__init__()
        self.hotkeys: Dict[str, Dict[str, Any]] = {}
        self.is_running = False
        self.lock = threading.Lock()
    
    def start(self):
        """Start the hotkey manager"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start a thread to handle hotkeys
        self.thread = threading.Thread(target=self._hotkey_thread, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the hotkey manager"""
        self.is_running = False
        
        # Unregister all hotkeys
        with self.lock:
            for hotkey in self.hotkeys:
                try:
                    keyboard.unhook_key(hotkey)
                except:
                    pass
            
            self.hotkeys.clear()
    
    def register_hotkey(self, key_combination: str, name: str, callback: Callable = None):
        """Register a hotkey
        
        Args:
            key_combination: Key combination (e.g., 'ctrl+shift+a')
            name: Name of the hotkey for identification
            callback: Optional callback function to call when hotkey is triggered
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            with self.lock:
                # Check if hotkey already exists
                if key_combination in self.hotkeys:
                    return False
                
                # Register the hotkey
                keyboard.add_hotkey(key_combination, self._on_hotkey_triggered, args=(key_combination,))
                
                # Store the hotkey info
                self.hotkeys[key_combination] = {
                    'name': name,
                    'callback': callback
                }
                
                return True
        except Exception as e:
            print(f"Error registering hotkey: {e}")
            return False
    
    def unregister_hotkey(self, key_combination: str):
        """Unregister a hotkey
        
        Args:
            key_combination: Key combination to unregister
        
        Returns:
            bool: True if unregistration was successful, False otherwise
        """
        try:
            with self.lock:
                # Check if hotkey exists
                if key_combination not in self.hotkeys:
                    return False
                
                # Unregister the hotkey
                keyboard.remove_hotkey(key_combination)
                
                # Remove the hotkey info
                del self.hotkeys[key_combination]
                
                return True
        except Exception as e:
            print(f"Error unregistering hotkey: {e}")
            return False
    
    def get_registered_hotkeys(self):
        """Get a list of registered hotkeys
        
        Returns:
            list: List of dictionaries with hotkey information
        """
        with self.lock:
            return [
                {
                    'key_combination': key,
                    'name': info['name']
                }
                for key, info in self.hotkeys.items()
            ]
    
    def _on_hotkey_triggered(self, key_combination: str):
        """Handle hotkey trigger
        
        Args:
            key_combination: Key combination that was triggered
        """
        with self.lock:
            if key_combination in self.hotkeys:
                # Get the hotkey info
                info = self.hotkeys[key_combination]
                
                # Call the callback if provided
                if info['callback']:
                    info['callback']()
                
                # Emit the signal
                self.hotkey_triggered.emit(info['name'])
    
    def _hotkey_thread(self):
        """Thread function for handling hotkeys"""
        while self.is_running:
            # Let keyboard module handle events
            keyboard.wait()

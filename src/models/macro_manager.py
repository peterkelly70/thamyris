"""
Macro system - Manages sound macros for the application
"""
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from typing import List, Dict, Any
import json
import os
import uuid


class MacroStep:
    """Class representing a step in a macro"""
    
    def __init__(self, sound_id: str = None, delay: float = 0.0):
        self.id = str(uuid.uuid4())
        self.sound_id = sound_id
        self.delay = delay  # Delay in seconds before playing this sound
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'sound_id': self.sound_id,
            'delay': self.delay
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        step = cls()
        step.id = data.get('id', str(uuid.uuid4()))
        step.sound_id = data.get('sound_id')
        step.delay = data.get('delay', 0.0)
        return step


class Macro:
    """Class representing a sound macro"""
    
    def __init__(self, name: str = "New Macro"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.steps: List[MacroStep] = []
        self.hotkey = None  # Optional hotkey assignment
    
    def add_step(self, sound_id: str, delay: float = 0.0):
        """Add a step to the macro"""
        step = MacroStep(sound_id, delay)
        self.steps.append(step)
        return step
    
    def remove_step(self, step_id: str):
        """Remove a step from the macro"""
        self.steps = [step for step in self.steps if step.id != step_id]
    
    def move_step_up(self, step_id: str):
        """Move a step up in the sequence"""
        for i, step in enumerate(self.steps):
            if step.id == step_id and i > 0:
                self.steps[i], self.steps[i-1] = self.steps[i-1], self.steps[i]
                return True
        return False
    
    def move_step_down(self, step_id: str):
        """Move a step down in the sequence"""
        for i, step in enumerate(self.steps):
            if step.id == step_id and i < len(self.steps) - 1:
                self.steps[i], self.steps[i+1] = self.steps[i+1], self.steps[i]
                return True
        return False
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'steps': [step.to_dict() for step in self.steps],
            'hotkey': self.hotkey
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary"""
        macro = cls()
        macro.id = data.get('id', str(uuid.uuid4()))
        macro.name = data.get('name', "Unnamed Macro")
        macro.steps = [MacroStep.from_dict(step_data) for step_data in data.get('steps', [])]
        macro.hotkey = data.get('hotkey')
        return macro


class MacroManager(QObject):
    """Class for managing sound macros"""
    
    # Signals
    macro_started = pyqtSignal(str)  # Macro ID
    macro_step_played = pyqtSignal(str, str)  # Macro ID, Step ID
    macro_finished = pyqtSignal(str)  # Macro ID
    
    def __init__(self, base_directory: str):
        super().__init__()
        self.macros: Dict[str, Macro] = {}
        self.active_macros: Dict[str, Dict[str, Any]] = {}
        self.base_directory = base_directory
        self.macros_directory = os.path.join(base_directory, 'resources', 'macros')
        
        # Create macros directory if it doesn't exist
        os.makedirs(self.macros_directory, exist_ok=True)
        
        # Load macros
        self.load_macros()
    
    def load_macros(self):
        """Load macros from files"""
        self.macros.clear()
        
        # Check if directory exists
        if not os.path.exists(self.macros_directory):
            return
        
        # Load each macro file
        for filename in os.listdir(self.macros_directory):
            if filename.endswith('.macro'):
                try:
                    with open(os.path.join(self.macros_directory, filename), 'r') as f:
                        data = json.load(f)
                        macro = Macro.from_dict(data)
                        self.macros[macro.id] = macro
                except Exception as e:
                    print(f"Error loading macro {filename}: {e}")
    
    def save_macros(self):
        """Save all macros to files"""
        # Create directory if it doesn't exist
        os.makedirs(self.macros_directory, exist_ok=True)
        
        # Save each macro
        for macro_id, macro in self.macros.items():
            try:
                filename = f"{self._sanitize_filename(macro.name)}.macro"
                with open(os.path.join(self.macros_directory, filename), 'w') as f:
                    json.dump(macro.to_dict(), f, indent=2)
            except Exception as e:
                print(f"Error saving macro {macro.name}: {e}")
    
    def create_macro(self, name: str = "New Macro"):
        """Create a new macro"""
        macro = Macro(name)
        self.macros[macro.id] = macro
        return macro
    
    def delete_macro(self, macro_id: str):
        """Delete a macro"""
        if macro_id in self.macros:
            macro = self.macros[macro_id]
            del self.macros[macro_id]
            
            # Delete the file
            try:
                filename = f"{self._sanitize_filename(macro.name)}.macro"
                file_path = os.path.join(self.macros_directory, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting macro file: {e}")
            
            return True
        return False
    
    def get_macro(self, macro_id: str):
        """Get a macro by ID"""
        return self.macros.get(macro_id)
    
    def get_all_macros(self):
        """Get all macros"""
        return list(self.macros.values())
    
    def play_macro(self, macro_id: str, play_callback):
        """Play a macro
        
        Args:
            macro_id: ID of the macro to play
            play_callback: Callback function to play a sound
                           Function signature: play_callback(sound_id)
        
        Returns:
            bool: True if macro started playing, False otherwise
        """
        if macro_id not in self.macros:
            return False
        
        macro = self.macros[macro_id]
        
        # Check if macro has steps
        if not macro.steps:
            return False
        
        # Create a timer for each step
        timers = []
        total_delay = 0
        
        for step in macro.steps:
            total_delay += step.delay
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(
                lambda s=step: self._play_step(macro_id, s.id, s.sound_id, play_callback)
            )
            timer.setInterval(int(total_delay * 1000))  # Convert to milliseconds
            timers.append(timer)
        
        # Store active macro info
        self.active_macros[macro_id] = {
            'timers': timers,
            'current_step': -1
        }
        
        # Start all timers
        for timer in timers:
            timer.start()
        
        # Emit signal
        self.macro_started.emit(macro_id)
        
        return True
    
    def stop_macro(self, macro_id: str):
        """Stop a playing macro"""
        if macro_id in self.active_macros:
            # Stop all timers
            for timer in self.active_macros[macro_id]['timers']:
                timer.stop()
            
            # Remove from active macros
            del self.active_macros[macro_id]
            
            # Emit signal
            self.macro_finished.emit(macro_id)
            
            return True
        return False
    
    def stop_all_macros(self):
        """Stop all playing macros"""
        macro_ids = list(self.active_macros.keys())
        for macro_id in macro_ids:
            self.stop_macro(macro_id)
    
    def _play_step(self, macro_id: str, step_id: str, sound_id: str, play_callback):
        """Play a step in a macro"""
        # Call the play callback
        play_callback(sound_id)
        
        # Emit signal
        self.macro_step_played.emit(macro_id, step_id)
        
        # Check if this is the last step
        if macro_id in self.active_macros:
            macro = self.macros[macro_id]
            active_info = self.active_macros[macro_id]
            active_info['current_step'] += 1
            
            # If all steps have been played, emit finished signal
            if active_info['current_step'] >= len(macro.steps) - 1:
                # Remove from active macros
                del self.active_macros[macro_id]
                
                # Emit signal
                self.macro_finished.emit(macro_id)
    
    def _sanitize_filename(self, filename: str):
        """Sanitize a filename to be safe for the filesystem"""
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename

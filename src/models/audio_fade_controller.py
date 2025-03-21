"""
Audio fade controller - Handles fade in/out effects for audio
"""
import numpy as np
from enum import Enum
from typing import Dict, Any


class FadeType(Enum):
    """Types of audio fades"""
    LINEAR = 0
    EXPONENTIAL = 1
    LOGARITHMIC = 2
    SINUSOIDAL = 3


class AudioFadeController:
    """Class for handling audio fade in/out effects"""
    
    def __init__(self):
        self.fade_in_duration = 0.5  # Default fade in duration in seconds
        self.fade_out_duration = 0.5  # Default fade out duration in seconds
        self.fade_type = FadeType.LINEAR  # Default fade type
    
    def set_fade_in_duration(self, duration: float):
        """Set the fade in duration in seconds"""
        self.fade_in_duration = max(0.0, duration)
    
    def set_fade_out_duration(self, duration: float):
        """Set the fade out duration in seconds"""
        self.fade_out_duration = max(0.0, duration)
    
    def set_fade_type(self, fade_type: FadeType):
        """Set the fade type"""
        self.fade_type = fade_type
    
    def apply_fade_in(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply fade in effect to audio
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Audio data with fade in applied
        """
        if self.fade_in_duration <= 0:
            return audio
        
        # Calculate number of samples for fade
        fade_samples = int(self.fade_in_duration * sample_rate)
        
        # Make sure we don't try to fade more samples than we have
        fade_samples = min(fade_samples, len(audio))
        
        if fade_samples <= 0:
            return audio
        
        # Create fade curve
        fade_curve = self._create_fade_curve(fade_samples, True)
        
        # Apply fade
        result = audio.copy()
        
        # Handle mono or stereo
        if len(result.shape) == 1:  # Mono
            result[:fade_samples] *= fade_curve
        else:  # Stereo or multi-channel
            for channel in range(result.shape[1]):
                result[:fade_samples, channel] *= fade_curve
        
        return result
    
    def apply_fade_out(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Apply fade out effect to audio
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Audio data with fade out applied
        """
        if self.fade_out_duration <= 0:
            return audio
        
        # Calculate number of samples for fade
        fade_samples = int(self.fade_out_duration * sample_rate)
        
        # Make sure we don't try to fade more samples than we have
        fade_samples = min(fade_samples, len(audio))
        
        if fade_samples <= 0:
            return audio
        
        # Create fade curve
        fade_curve = self._create_fade_curve(fade_samples, False)
        
        # Apply fade
        result = audio.copy()
        
        # Handle mono or stereo
        if len(result.shape) == 1:  # Mono
            result[-fade_samples:] *= fade_curve
        else:  # Stereo or multi-channel
            for channel in range(result.shape[1]):
                result[-fade_samples:, channel] *= fade_curve
        
        return result
    
    def _create_fade_curve(self, num_samples: int, fade_in: bool) -> np.ndarray:
        """Create a fade curve
        
        Args:
            num_samples: Number of samples in the fade
            fade_in: True for fade in, False for fade out
            
        Returns:
            Numpy array with fade curve values
        """
        x = np.linspace(0, 1, num_samples)
        
        if self.fade_type == FadeType.LINEAR:
            curve = x
        elif self.fade_type == FadeType.EXPONENTIAL:
            curve = x ** 2
        elif self.fade_type == FadeType.LOGARITHMIC:
            curve = np.sqrt(x)
        elif self.fade_type == FadeType.SINUSOIDAL:
            curve = (1 - np.cos(x * np.pi)) / 2
        else:
            curve = x  # Default to linear
        
        # Reverse for fade out
        if not fade_in:
            curve = curve[::-1]
        
        return curve

import importlib.resources
from pathlib import Path

def get_speech_wav_path():
    # Returns a pathlib.Path object to speech.wav
    return Path(importlib.resources.files(__package__) / 'speech.wav')

# Make the function available when importing from assets
__all__ = ['get_speech_wav_path']

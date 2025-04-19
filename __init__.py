from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeSubtitleAudio import MergeSubtitleAudio

import os

# List all files in assets folder
ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SRT_FILES = [f for f in os.listdir(ASSETS_PATH) if f.endswith(".srt")]
DUMMY_DIR_OPTIONS = [ASSETS_PATH]

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "MergeSubtitleAudio": MergeSubtitleAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeSubtitleAudio": "Merge Subtitle Audio",
}

WEB_DIRECTORY = "./web"

# Extend MergeSubtitleAudio node to include dropdown logic (monkey patching for simplicity)
if hasattr(MergeSubtitleAudio, "INPUT_TYPES"):
    original_input_types = MergeSubtitleAudio.INPUT_TYPES
    def patched_input_types(cls):
        config = original_input_types()
        config["required"]["srt_file"] = (SRT_FILES,)
        config["required"]["dummy_dir"] = (DUMMY_DIR_OPTIONS,)
        return config
    MergeSubtitleAudio.INPUT_TYPES = classmethod(patched_input_types)

from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeSubtitleAudio import MergeSubtitleAudio, ListSavedAudioFiles
from .MergeSelectedAudioFiles import MergeSelectedAudioFiles
from .MergeAllWave import MergeAllWave  # ✅ เพิ่มใหม่

import os

ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SRT_UPLOAD_PATH = os.path.join(ASSETS_PATH, "srt_uploads")
DUMMY_DIR_OPTIONS = [ASSETS_PATH]

# ป้องกัน error ถ้า folder ว่าง
SRT_FILES = []
if os.path.exists(SRT_UPLOAD_PATH):
    SRT_FILES = [os.path.join(SRT_UPLOAD_PATH, f) for f in os.listdir(SRT_UPLOAD_PATH) if f.endswith(".srt")]

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "MergeSubtitleAudio": MergeSubtitleAudio,
    "ListSavedAudioFiles": ListSavedAudioFiles,
    "MergeSelectedAudioFiles": MergeSelectedAudioFiles,
    "MergeAllWave": MergeAllWave,  # ✅ map คลาสใหม่
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeSubtitleAudio": "Merge Subtitle Audio - do not use",
    "ListSavedAudioFiles": "List Saved Audio Files - do not use",
    "MergeSelectedAudioFiles": "Merge Selected Audio Files - do not use",
    "MergeAllWave": "Merge All Wave",  # ✅ แสดงชื่อใน UI
}

WEB_DIRECTORY = "./web"

# ✅ เฉพาะ patch MergeSubtitleAudio เท่านั้น
if hasattr(MergeSubtitleAudio, "INPUT_TYPES"):
    original_input_types = MergeSubtitleAudio.INPUT_TYPES
    def patched_input_types(cls):
        config = original_input_types()
        config["required"]["srt_file"] = (SRT_FILES,)
        config["required"]["dummy_dir"] = (DUMMY_DIR_OPTIONS,)
        return config
    MergeSubtitleAudio.INPUT_TYPES = classmethod(patched_input_types)

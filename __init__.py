from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeAllWave import MergeAllWave
from .ListSavedAudioFiles import ListSavedAudioFiles  # ถ้าแยกไฟล์

import os

ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SRT_UPLOAD_PATH = os.path.join(ASSETS_PATH, "srt_uploads")

# ป้องกัน error ถ้า folder ว่าง
SRT_FILES = []
if os.path.exists(SRT_UPLOAD_PATH):
    SRT_FILES = [os.path.join(SRT_UPLOAD_PATH, f) for f in os.listdir(SRT_UPLOAD_PATH) if f.endswith(".srt")]

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "MergeAllWave": MergeAllWave,
    "ListSavedAudioFiles": ListSavedAudioFiles,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeAllWave": "Merge All Wave",
    "ListSavedAudioFiles": "List Saved Audio Files - do not use",
}

WEB_DIRECTORY = "./web"

from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeAllWave import MergeAllWave  # ✅ ใช้ตัวใหม่แทน


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

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeAllWave": "Merge All Wave",

}

WEB_DIRECTORY = "./web"

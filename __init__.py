from .SaveWavNode import SaveWAVNode
from .GetSubtitleByIndex import GetSubtitleByIndex

NODE_CLASS_MAPPINGS = {
    "SaveWAVNode": SaveWAVNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWAVNode": "Save WAV from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
}

WEB_DIRECTORY = "./web"

from .SaveWavNode import SaveWAVNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .SaveWavNodePadding import SaveWAVNodePadding

NODE_CLASS_MAPPINGS = {
    "SaveWAVNode": SaveWAVNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "SaveWAVNodePadding": SaveWAVNodePadding,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWAVNode": "Save WAV from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "SaveWAVNodePadding": "Save WAV with Padding",
}

WEB_DIRECTORY = "./web"

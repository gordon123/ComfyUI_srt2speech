from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .SaveWavNodePadding import SaveWavNodePadding

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "SaveWavNodePadding": SaveWavNodePadding,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save WAV from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "SaveWavNodePadding": "Save Wav with Padding",
}

WEB_DIRECTORY = "./web"

from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeWithDummySilence import MergeWithDummySilence
from .MergeSavedWavWithDummy import MergeSavedWavWithDummy

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "MergeWithDummySilence": MergeWithDummySilence,
    "MergeSavedWavWithDummy": MergeSavedWavWithDummy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeWithDummySilence": "Merge with Dummy Silence",
    "MergeSavedWavWithDummy": "Merge Saved Wav with Dummy",
}

WEB_DIRECTORY = "./web"

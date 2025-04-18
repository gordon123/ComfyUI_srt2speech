from .SaveWavNode import SaveWavNode
from .GetSubtitleByIndex import GetSubtitleByIndex
from .MergeWithDummySilence import MergeWithDummySilence
from .MergeSavedWavWithDummy import MergeSavedWavWithDummy
from .LoadMergedAudio import LoadMergedAudio

NODE_CLASS_MAPPINGS = {
    "SaveWavNode": SaveWavNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
    "MergeWithDummySilence": MergeWithDummySilence,
    "MergeSavedWavWithDummy": MergeSavedWavWithDummy,
    "LoadMergedAudio": LoadMergedAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveWavNode": "Save Wav from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
    "MergeWithDummySilence": "Merge with Dummy Silence",
    "MergeSavedWavWithDummy": "Merge Saved Wav with Dummy",
    "LoadMergedAudio": "Load Merged Audio",
}

WEB_DIRECTORY = "./web"

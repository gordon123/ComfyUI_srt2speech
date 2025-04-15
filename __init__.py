from .SRT2SpeechNode import SRT2SpeechNode
from .SplitSRTSentencesNode import SplitSRTSentencesNode
from .SplitAllSubtitlesNode import SplitAllSubtitlesNode
from .SubtitleIteratorNode import SubtitleIteratorNode
from .SaveWavNode import SaveWAVNode
from .GetSubtitleByIndex import GetSubtitleByIndex


NODE_CLASS_MAPPINGS = {
    "SRT2SpeechNode": SRT2SpeechNode,
    "SplitSRTSentencesNode": SplitSRTSentencesNode,
    "SplitAllSubtitlesNode": SplitAllSubtitlesNode,
    "SubtitleIteratorNode": SubtitleIteratorNode,
    "SaveWAVNode": SaveWAVNode,
    "GetSubtitleByIndex": GetSubtitleByIndex,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "SRT2SpeechNode": "SRT to Speech",
    "SplitSRTSentencesNode": "Split SRT Sentence (1st)",
    "SplitAllSubtitlesNode": "Split All Subtitles",
    "SubtitleIteratorNode": "Subtitle Iterator",
    "SaveWAVNode": "Save WAV from TTS",
    "GetSubtitleByIndex": "Get Subtitle By Index",
}


WEB_DIRECTORY = "./web"
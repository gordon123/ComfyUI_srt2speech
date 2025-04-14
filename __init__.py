  from .srt2speech import SRT2SpeechNode

  NODE_CLASS_MAPPINGS = {
      "SRT2SpeechNode": SRT2SpeechNode
  }

  NODE_DISPLAY_NAME_MAPPINGS = {
      "SRT2SpeechNode": "SRT to Speech"
  }

  __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

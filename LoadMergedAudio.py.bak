# ✅ Load merged audio from assets/merge_audio for preview or reuse

import os
import torchaudio

class LoadMergedAudio:
    @classmethod
    def INPUT_TYPES(cls):
        merge_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "merge_audio")
        os.makedirs(merge_dir, exist_ok=True)  # ✅ ensure folder exists
        files = [f for f in os.listdir(merge_dir) if f.endswith(".wav")]
        files.sort()
        return {
            "required": {
                "file_path": (files,)
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "load_audio"
    CATEGORY = "📺 Subtitle Tools"

    def load_audio(self, file_path):
        merge_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "merge_audio")
        full_path = os.path.join(merge_dir, file_path)
        waveform, sample_rate = torchaudio.load(full_path)
        return ({"waveform": waveform, "sample_rate": sample_rate},)

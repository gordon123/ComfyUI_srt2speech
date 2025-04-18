# ✅ Fix waveform shape and backend. This node will save the audio into the wav format. file name with the timestamp.
# ✅ Add dummy merge to fill silence if needed (PyDub)
# ✅ Update: Automatically list saved files in assets/audio_out for file selection

import os
import re
import torchaudio
import torch
from pydub import AudioSegment

class SaveWavNodePadding:
    @classmethod
    def INPUT_TYPES(cls):
        audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio_out")
        files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
        files.sort()
        return {
            "required": {
                "file_path": (files,),
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False}),
                "pad_audio": ("BOOLEAN", {"default": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge_with_dummy"
    CATEGORY = "📺 Subtitle Tools"

    def format_timestamp(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}_{int(m):02}_{int(s)}s{int(ms)}ms"

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def merge_with_dummy(self, file_path, timestamp, srt_file, pad_audio):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(base_path, "assets", "audio_out")
        full_audio_path = os.path.join(audio_dir, file_path)
        dummy_dir = os.path.join(base_path, "assets")

        if not os.path.exists(full_audio_path):
            raise FileNotFoundError(f"Audio file not found: {full_audio_path}")

        audio_segment = AudioSegment.from_file(full_audio_path)
        sample_rate = audio_segment.frame_rate

        if pad_audio:
            match = re.match(r"(.+?) --> (.+)", timestamp)
            if match:
                start_sec = self.get_seconds(match.group(1))
                end_sec = self.get_seconds(match.group(2))
                target_ms = int((end_sec - start_sec) * 1000)
                actual_ms = len(audio_segment)
                if actual_ms < target_ms:
                    dummy_path = os.path.join(dummy_dir, f"dummy{sample_rate // 1000}khz.wav")
                    dummy = AudioSegment.from_file(dummy_path)[:(target_ms - actual_ms)]
                    audio_segment += dummy

        output_path = full_audio_path.replace(".wav", "_merged.wav")
        audio_segment.export(output_path, format="wav")

        return (output_path,)

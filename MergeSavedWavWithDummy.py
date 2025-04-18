# ✅ Fix waveform shape and backend. This node will merge wav + dummy if too short.

import os
import re
import torchaudio
import torch
from pydub import AudioSegment

class MergeSavedWavWithDummy:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False}),
            },
            "optional": {
                "file_path": ("STRING", {"multiline": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge_wav"
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

    def merge_wav(self, timestamp, srt_file, file_path=None):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_dir = os.path.join(base_path, "assets", "audio_out")
        dummy_dir = os.path.join(base_path, "assets")

        match = re.match(r"(.+?) --> (.+)", timestamp)
        if not match:
            raise ValueError("Invalid timestamp format")

        start_time, end_time = match.group(1), match.group(2)
        target_ms = int((self.get_seconds(end_time) - self.get_seconds(start_time)) * 1000)

        # infer file name from timestamp if not explicitly passed
        if not file_path:
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)
            base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
            file_path = os.path.join(audio_dir, f"{start}_to_{end}__{base_name}.wav")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Wav file not found: {file_path}")

        audio = AudioSegment.from_file(file_path)
        actual_ms = len(audio)

        if actual_ms < target_ms:
            sample_rate = audio.frame_rate
            dummy_path = os.path.join(dummy_dir, f"dummy{sample_rate // 1000}khz.wav")
            if not os.path.exists(dummy_path):
                raise FileNotFoundError(f"Dummy file not found: {dummy_path}")
            dummy = AudioSegment.from_file(dummy_path)[:target_ms - actual_ms]
            audio += dummy

        merged_path = file_path.replace(".wav", "_merged.wav")
        audio.export(merged_path, format="wav")

        return (merged_path,)

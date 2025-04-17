# ✅ Merge saved wav with dummy silence if needed

import os
import re
import torchaudio
from pydub import AudioSegment

class MergeSavedWavWithDummy:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"multiline": False}),
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge"
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

    def merge(self, file_path, timestamp, srt_file):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        base_path = os.path.dirname(os.path.abspath(__file__))
        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)
        else:
            raise ValueError(f"Invalid timestamp format: {timestamp}")

        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        output_folder = os.path.join(base_path, "assets", "audio_out")
        os.makedirs(output_folder, exist_ok=True)
        out_path = os.path.join(output_folder, filename)

        audio = AudioSegment.from_file(file_path)
        actual_ms = len(audio)
        target_ms = int((self.get_seconds(end_time) - self.get_seconds(start_time)) * 1000)

        print(f"[DEBUG] File: {file_path}, actual={actual_ms}ms, expected={target_ms}ms")

        if actual_ms < target_ms:
            sample_rate = audio.frame_rate
            dummy_name = f"dummy{sample_rate // 1000}khz.wav"
            dummy_path = os.path.join(base_path, "assets", dummy_name)
            dummy = AudioSegment.from_file(dummy_path)
            silence_needed = target_ms - actual_ms
            audio += dummy[:silence_needed]

        audio.export(out_path, format="wav")
        return (out_path,)

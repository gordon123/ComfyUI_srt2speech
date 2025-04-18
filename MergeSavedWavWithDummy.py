# ✅ Fix waveform shape and backend. Merge saved wav file with dummy silence if needed.
# ✅ Automatically load files from audio_out folder

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
                "srt_file": ("STRING", {"multiline": False, "default": ""})
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
        out_folder = os.path.join(base_path, "assets", "audio_out")

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)

        # Auto match filename from pattern if not provided
        if not file_path:
            base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
            target_filename = f"{start}_to_{end}__{base_name}.wav"
            file_path = os.path.join(out_folder, target_filename)

        print(f"[INFO] Loading {file_path}")

        # Load and check duration
        audio = AudioSegment.from_file(file_path)
        actual_ms = len(audio)
        target_ms = int((self.get_seconds(end_time) - self.get_seconds(start_time)) * 1000)

        # Only pad if too short
        if actual_ms < target_ms:
            dummy_path = os.path.join(base_path, "assets", f"dummy{audio.frame_rate // 1000}khz.wav")
            silence = AudioSegment.from_file(dummy_path)[:(target_ms - actual_ms)]
            audio += silence
            print(f"[INFO] Padded with {len(silence)}ms dummy silence")

        merged_path = file_path.replace(".wav", "_merged.wav")
        audio.export(merged_path, format="wav")
        return (merged_path,)

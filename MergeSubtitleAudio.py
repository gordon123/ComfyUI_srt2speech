# 📦 Merge all subtitle audio wav files into a single audio file
# 🔉 Includes silence based on subtitle gaps

import os
import re
from pydub import AudioSegment

class MergeSubtitleAudio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_file": ("STRING", {"multiline": False}),
                "sample_rate": ("INT", {"default": 24000, "min": 8000, "max": 48000, "step": 1000}),
                "audio_folder": ("STRING", {"default": "assets/audio_out"}),
                "output_name": ("STRING", {"default": "full_sub_audio.wav"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_audio_path",)
    FUNCTION = "merge"
    CATEGORY = "📺 Subtitle Tools"

    def parse_srt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        entries = []
        blocks = re.split(r'\n\s*\n', content.strip())
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                index = lines[0]
                times = lines[1]
                text = " ".join(lines[2:])
                start, end = times.split(' --> ')
                entries.append((start.strip(), end.strip(), text.strip()))
        return entries

    def to_millis(self, timestamp):
        h, m, s = re.split('[:]', timestamp.replace(",", "."))
        s, ms = s.split('.')
        return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)

    def merge(self, srt_file, sample_rate, audio_folder, output_name):
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_path, audio_folder)
        srt_path = os.path.join(base_path, srt_file)
        output_path = os.path.join(base_path, "assets", "merge_audio", output_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        entries = self.parse_srt(srt_path)
        merged = AudioSegment.silent(duration=0, frame_rate=sample_rate)

        for start, end, _ in entries:
            filename_pattern = f"{self.format_filename(start)}_to_{self.format_filename(end)}"
            file = next((f for f in os.listdir(folder) if filename_pattern in f), None)
            start_ms = self.to_millis(start)
            if file:
                audio = AudioSegment.from_file(os.path.join(folder, file))
                silence_needed = start_ms - len(merged)
                if silence_needed > 0:
                    merged += AudioSegment.silent(duration=silence_needed, frame_rate=sample_rate)
                merged += audio
            else:
                print(f"[WARN] No audio for subtitle: {start} -> {end}")

        merged.export(output_path, format="wav")
        return (output_path,)

    def format_filename(self, timestamp):
        timestamp = timestamp.replace(",", ".")
        h, m, s = timestamp.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}_{int(m):02}_{int(s)}s{int(ms)}ms"

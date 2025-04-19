import os
import re
from pydub import AudioSegment

class MergeSubtitleAudio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_file": ([""],),  # Patched in __init__.py
                "dummy_dir": ([""],),  # Patched in __init__.py
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge"
    CATEGORY = "📺 Subtitle Tools"

    def parse_srt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip().split('\n\n')
        entries = []
        for block in content:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                times = lines[1]
                match = re.match(r"(.+?) --> (.+)", times)
                if match:
                    entries.append((match.group(1), match.group(2)))
        return entries

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def merge(self, srt_file, dummy_dir):
        srt_path = os.path.join(os.path.dirname(__file__), "assets", srt_file)
        dummy_16khz = AudioSegment.from_file(os.path.join(dummy_dir, "dummy16khz.wav"))
        dummy_24khz = AudioSegment.from_file(os.path.join(dummy_dir, "dummy24khz.wav"))
        audio_out = os.path.join(os.path.dirname(__file__), "assets", "audio_out")

        entries = self.parse_srt(srt_path)
        merged = AudioSegment.silent(duration=0)

        for i, (start, end) in enumerate(entries):
            start_sec = self.get_seconds(start)
            end_sec = self.get_seconds(end)
            duration_ms = int((end_sec - start_sec) * 1000)

            # Construct filename pattern
            filename_pattern = f"{start.replace(':', '_').replace('.', 's')}"
            matched = [f for f in os.listdir(audio_out) if filename_pattern in f]

            if matched:
                path = os.path.join(audio_out, matched[0])
                segment = AudioSegment.from_file(path)
                if len(segment) < duration_ms:
                    diff = duration_ms - len(segment)
                    pad = dummy_24khz[:diff] if segment.frame_rate == 24000 else dummy_16khz[:diff]
                    segment += pad
                elif len(segment) > duration_ms:
                    segment = segment[:duration_ms]
                merged += segment
            else:
                print(f"[WARN] No match for subtitle index {i} ({start} - {end})")
                silence = dummy_24khz[:duration_ms]
                merged += silence

        output_path = os.path.join(os.path.dirname(__file__), "assets", "merged_all.wav")
        merged.export(output_path, format="wav")

        return (output_path,)

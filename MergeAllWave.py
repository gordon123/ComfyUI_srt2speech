import os
import re
from pydub import AudioSegment

class MergeAllWave:
    @classmethod
    def INPUT_TYPES(cls):
        assets_path = os.path.dirname(os.path.abspath(__file__))
        srt_dir = os.path.join(assets_path, "assets", "srt_uploads")
        srt_files = [f for f in os.listdir(srt_dir) if f.endswith(".srt")]
        srt_files.sort()
        return {
            "required": {
                "srt_file": (srt_files,)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_file_path",)
    FUNCTION = "merge_all"
    CATEGORY = "📺 Subtitle Tools"

    def format_prefix(self, t):
        """Convert timestamp to match file prefix: 00_00_00s160ms"""
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}_{int(m):02}_{int(s):02}s{int(ms)}ms"

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def parse_srt(self, srt_path):
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')

        entries = []
        entry = {}
        for line in lines:
            if line.strip().isdigit():
                if entry:
                    entries.append(entry)
                    entry = {}
            elif "-->" in line:
                entry['timestamp'] = line.strip()
            elif line.strip():
                entry.setdefault('text', []).append(line.strip())
        if entry:
            entries.append(entry)
        return entries

    def merge_all(self, srt_file):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_out_path = os.path.join(base_path, "assets", "audio_out")
        srt_path = os.path.join(base_path, "assets", "srt_uploads", srt_file)
        srt_base = os.path.splitext(srt_file)[0]
        merge_output_path = os.path.join(base_path, "assets", f"merged__{srt_base}.wav")

        entries = self.parse_srt(srt_path)
        merged = AudioSegment.silent(duration=0)

        for entry in entries:
            timestamp = entry.get("timestamp", "")
            if not timestamp:
                continue

            match = re.match(r"(.+?) --> (.+)", timestamp)
            if not match:
                continue

            start, _ = match.group(1), match.group(2)
            prefix = self.format_prefix(start)

            try:
                audio_file = next(f for f in os.listdir(audio_out_path) if f.startswith(prefix))
                seg = AudioSegment.from_file(os.path.join(audio_out_path, audio_file))
                merged += seg
            except StopIteration:
                # Comment out the line below if you don't want debug messages
                print(f"[DEBUG] No match for {start} (prefix: {prefix}) → skipping")

        merged.export(merge_output_path, format="wav")
        return (merge_output_path,)

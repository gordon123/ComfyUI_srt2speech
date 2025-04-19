import os
import re
from pydub import AudioSegment

class MergeSubtitleAudio:
    @classmethod
    def INPUT_TYPES(cls):
        assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        srt_dir = os.path.join(assets_path, "srt_uploads")
        srt_files = [f for f in os.listdir(srt_dir) if f.endswith(".srt")]
        srt_files.sort()
        dummy_dir_options = [assets_path]
        return {
            "required": {
                "srt_file": (srt_files,),
                "dummy_dir": (dummy_dir_options,)
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_file_path",)
    FUNCTION = "merge"
    CATEGORY = "📺 Subtitle Tools"

    def format_timestamp(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}:{int(m):02}:{int(s)}.{int(ms):03}"

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

    def merge(self, srt_file, dummy_dir):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_out_path = os.path.join(base_path, "assets", "audio_out")
        merge_output_path = os.path.join(base_path, "assets", "merged_all.wav")
        srt_path = os.path.join(base_path, "assets", "srt_uploads", srt_file)

        entries = self.parse_srt(srt_path)

        merged = AudioSegment.silent(duration=0)

        dummy_16khz = AudioSegment.from_file(os.path.join(dummy_dir, "dummy16khz.wav"))
        dummy_24khz = AudioSegment.from_file(os.path.join(dummy_dir, "dummy24khz.wav"))

        for entry in entries:
            timestamp = entry.get("timestamp", "")
            if not timestamp:
                continue

            match = re.match(r"(.+?) --> (.+)", timestamp)
            if not match:
                continue

            start, end = match.group(1), match.group(2)
            start_sec = self.get_seconds(start)
            end_sec = self.get_seconds(end)
            target_ms = int((end_sec - start_sec) * 1000)

            file_prefix = f"{start.replace(':', '_').replace('.', 's')}"
            try:
                audio_file = next(f for f in os.listdir(audio_out_path) if file_prefix in f)
                seg = AudioSegment.from_file(os.path.join(audio_out_path, audio_file))
                actual_ms = len(seg)
                if actual_ms < target_ms:
                    padding = dummy_24khz[:target_ms - actual_ms]
                    seg += padding
                elif actual_ms > target_ms:
                    seg = seg[:target_ms]
                merged += seg
            except StopIteration:
                # fallback: if no file matches, insert silence
                merged += dummy_24khz[:target_ms]

        merged.export(merge_output_path, format="wav")
        return (merge_output_path,)

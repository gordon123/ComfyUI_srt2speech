import os
import re

class GetSubtitleIndexByFilename:
    @classmethod
    def INPUT_TYPES(cls):
        audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio_out")
        files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
        files.sort()
        return {
            "required": {
                "file_path": (files,),
                "srt_file": ("STRING", {"multiline": False})
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("index",)
    FUNCTION = "find_index"
    CATEGORY = "📺 Subtitle Tools"

    def parse_srt(self, srt_file):
        if not os.path.isabs(srt_file):
            base_path = os.path.dirname(os.path.abspath(__file__))
            srt_path = os.path.join(base_path, "assets", "srt_uploads", srt_file)
        else:
            srt_path = srt_file

        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        entries = re.split(r'\n\s*\n', content.strip())
        parsed = []
        for entry in entries:
            lines = entry.split("\n")
            if len(lines) >= 2:
                timestamp = lines[1]
                parsed.append(timestamp)
        return parsed

    def extract_start_time(self, filename):
        match = re.match(r"(\d{2})_(\d{2})_(\d{2})s(\d{1,3})ms", filename)
        if not match:
            raise ValueError("Cannot parse start time from filename")
        h, m, s, ms = map(int, match.groups())
        return h * 3600 + m * 60 + s + ms / 1000

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def find_index(self, file_path, srt_file):
        base_filename = file_path.split("__")[0]
        try:
            start_time_sec = self.extract_start_time(base_filename)
        except Exception as e:
            print("[ERROR] Filename parsing failed:", e)
            raise ValueError("Cannot parse start time from filename")

        entries = self.parse_srt(srt_file)

        for i, timestamp in enumerate(entries):
            match = re.match(r"(.+?) --> (.+)", timestamp)
            if match:
                sub_start = self.get_seconds(match.group(1))
                if abs(sub_start - start_time_sec) < 0.1:  # allow some tolerance
                    return (i,)

        raise ValueError("Matching subtitle not found for file: " + file_path)

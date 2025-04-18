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
                "srt_file": ("STRING", {"multiline": False}),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING",)
    RETURN_NAMES = ("index", "subtitle", "timestamp",)
    FUNCTION = "find_index"
    CATEGORY = "📺 Subtitle Tools"

    def parse_srt(self, srt_path):
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')

        index, text, timestamps = -1, [], []
        temp_text, temp_time = '', ''
        for line in lines:
            if re.match(r"^\d+$", line):
                if temp_text and temp_time:
                    text.append(temp_text.strip())
                    timestamps.append(temp_time.strip())
                index = int(line)
                temp_text, temp_time = '', ''
            elif '-->' in line:
                temp_time = line
            elif line.strip():
                temp_text += ' ' + line
        if temp_text and temp_time:
            text.append(temp_text.strip())
            timestamps.append(temp_time.strip())
        return list(zip(timestamps, text))

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def extract_start_seconds_from_filename(self, filename):
        # Example: 00_00_24s599ms_to_00_00_29s840ms__test-5min.wav
        match = re.match(r"(\d{2})_(\d{2})_(\d{2})s(\d{1,3})ms", filename)
        if not match:
            raise ValueError("Cannot parse start time from filename")
        h, m, s, ms = map(int, match.groups())
        return h * 3600 + m * 60 + s + ms / 1000

    def find_index(self, file_path, srt_file):
        file_base = os.path.basename(file_path)
        file_seconds = self.extract_start_seconds_from_filename(file_base)

        entries = self.parse_srt(srt_file)
        for idx, (timestamp, text) in enumerate(entries):
            start = timestamp.split('-->')[0].strip()
            start_sec = self.get_seconds(start)
            if abs(start_sec - file_seconds) < 0.5:  # allow slight rounding tolerance
                return (idx, text, timestamp)

        raise ValueError("Subtitle not found for this file")

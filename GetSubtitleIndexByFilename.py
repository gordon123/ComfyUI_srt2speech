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

    RETURN_TYPES = ("INT", "STRING", "STRING")
    RETURN_NAMES = ("index", "subtitle_text", "timestamp")
    FUNCTION = "find_index"
    CATEGORY = "📺 Subtitle Tools"

    def parse_timestamp(self, ts):
        ts = ts.replace(",", ".")
        h, m, s = ts.split(":")
        if "." in s:
            s, ms = s.split(".")
        else:
            s, ms = s, "0"
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def find_index(self, file_path, srt_file):
        # Extract start timestamp from filename
        match = re.match(r"(\d+_\d+s\d+ms)_to_", file_path)
        if not match:
            raise ValueError("Cannot parse start time from filename")

        start_str = match.group(1).replace("_", ":").replace("s", ".").replace("ms", "")
        start_sec = self.parse_timestamp(start_str)

        # Read the .srt file
        full_srt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "srt_uploads", srt_file)
        with open(full_srt_path, "r", encoding="utf-8") as f:
            content = f.read()

        entries = re.findall(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n", content, re.DOTALL)

        for idx, start, end, text in entries:
            start_sec_srt = self.parse_timestamp(start)
            end_sec_srt = self.parse_timestamp(end)
            if start_sec_srt <= start_sec <= end_sec_srt:
                return (int(idx)-1, text.strip(), f"{start} --> {end}")

        return (-1, "Not found", "")

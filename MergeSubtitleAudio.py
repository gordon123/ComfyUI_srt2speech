import os
import re
from pydub import AudioSegment

class MergeSubtitleAudio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_file": ("STRING", {"multiline": False}),
                "audio_dir": ("STRING", {"multiline": False, "default": "assets/audio_out"}),
                "dummy_dir": ("STRING", {"multiline": False, "default": "assets"}),
                "output_file": ("STRING", {"multiline": False, "default": "merged_output.wav"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge"
    CATEGORY = "📺 Subtitle Tools"

    def parse_srt(self, path):
        entries = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():
                timestamp = lines[i + 1].strip()
                entries.append(timestamp)
                i += 2
            else:
                i += 1
        return entries

    def timestamp_to_ms(self, timestamp):
        t = timestamp.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)

    def extract_wav_by_time(self, filename):
        match = re.match(r"(\d+_\d+s\d+ms)_to_(\d+_\d+s\d+ms)__.*", filename)
        if not match:
            return None, None
        start = match.group(1).replace("s", ":").replace("ms", ",").replace("_", ":")
        return start, filename

    def merge(self, srt_file, audio_dir, dummy_dir, output_file):
        base_path = os.path.dirname(os.path.abspath(__file__))
        srt_path = os.path.join(base_path, srt_file)
        audio_dir = os.path.join(base_path, audio_dir)
        dummy_dir = os.path.join(base_path, dummy_dir)
        output_path = os.path.join(base_path, dummy_dir, output_file)

        dummy_24khz = AudioSegment.from_file(os.path.join(dummy_dir, "dummy24khz.wav"))

        audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".wav")])
        timestamps = self.parse_srt(srt_path)

        merged = AudioSegment.silent(duration=0)

        for i, timestamp in enumerate(timestamps):
            start_ts, end_ts = timestamp.split(" --> ")
            start_ms = self.timestamp_to_ms(start_ts)
            end_ms = self.timestamp_to_ms(end_ts)
            duration_ms = end_ms - start_ms

            found = None
            for fname in audio_files:
                if fname.startswith(self.format_timestamp(start_ts)):
                    found = fname
                    break

            if found:
                clip = AudioSegment.from_file(os.path.join(audio_dir, found))
                if len(clip) > duration_ms:
                    clip = clip[:duration_ms]
                elif len(clip) < duration_ms:
                    pad = dummy_24khz[:duration_ms - len(clip)]
                    clip += pad
                merged += clip
            else:
                merged += dummy_24khz[:duration_ms]

        merged.export(output_path, format="wav")
        return (output_path,)

    def format_timestamp(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}_{int(m):02}_{int(s)}s{int(ms)}ms"

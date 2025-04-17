import os
import re
from pydub import AudioSegment

class MergeSavedWavWithDummy:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_path": ("STRING", {"multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge_audio"
    CATEGORY = "📺 Subtitle Tools"

    def parse_time(self, t):
        match = re.match(r"(\d+)_+(\d+)_+(\d+)s(\d+)ms", t)
        if match:
            h, m, s, ms = map(int, match.groups())
            return h * 3600 * 1000 + m * 60 * 1000 + s * 1000 + ms
        return 0

    def merge_audio(self, file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_base = os.path.join(base_dir, "assets")

        filename = os.path.basename(file_path)
        match = re.match(r"(.*?)_to_(.*?)__.*\\.wav", filename)

        if not match:
            print("[WARN] Filename format not matched.")
            return (file_path,)

        start_time = self.parse_time(match.group(1))
        end_time = self.parse_time(match.group(2))
        expected_ms = end_time - start_time

        audio = AudioSegment.from_file(file_path)
        actual_ms = len(audio)

        if actual_ms >= expected_ms:
            return (file_path,)

        sample_rate = audio.frame_rate
        dummy_file = f"dummy{sample_rate // 1000}khz.wav"
        dummy_path = os.path.join(dummy_base, dummy_file)

        if not os.path.exists(dummy_path):
            print(f"[ERROR] Dummy file not found: {dummy_path}")
            return (file_path,)

        silence_needed = expected_ms - actual_ms
        dummy = AudioSegment.from_file(dummy_path)[:silence_needed]
        merged = audio + dummy

        new_path = file_path.replace(".wav", "_merged.wav")
        merged.export(new_path, format="wav")
        print(f"[INFO] Exported padded: {new_path}")

        return (new_path,)

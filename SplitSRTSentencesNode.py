import re

class SplitSRTSentencesNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_text": ("STRING", {"multiline": True})
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "timestamp")
    FUNCTION = "split_srt"
    CATEGORY = "Subtitle Tools"

    def split_srt(self, srt_text):
        pattern = """(\d+)\n(\d{2}:\d{2}:\d{2},\d{3})\s-->\s(\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n(?=\d+\n|\Z)"""
        matches = re.findall(pattern, srt_text, re.DOTALL)

        results = []
        times = []

        for match in matches:
            index, start, end, text = match
            clean_text = text.strip().replace("\n", " ")
            if clean_text:
                results.append(clean_text)
                times.append(f"{start} --> {end}")

        if results:
            return (results[0], times[0])
        else:
            return ("", "")
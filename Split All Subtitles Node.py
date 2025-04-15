import re

class SplitAllSubtitlesNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_text": ("STRING", {"multiline": True})
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("subtitle_texts", "subtitle_times")
    FUNCTION = "split_all"
    CATEGORY = "📺 Subtitle Tools"

    def split_all(self, srt_text):
        pattern = r"""(\d+)\n(\d{2}:\d{2}:\d{2},\d{3})\s--\>\s(\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n(?=\d+\n|\Z)"""
        matches = re.findall(pattern, srt_text, re.DOTALL)

        results = []
        times = []

        for match in matches:
            index, start, end, text = match
            clean_text = text.strip().replace("\n", " ")
            if clean_text:
                results.append(clean_text)
                times.append(f"{start} --> {end}")

        joined_texts = "\n".join(results)
        joined_times = "\n".join(times)

        return (joined_texts, joined_times)

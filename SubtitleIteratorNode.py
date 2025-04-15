class SubtitleIteratorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "subtitle_texts": ("STRING", {"forceInput": True, "multiline": True}),
                "subtitle_times": ("STRING", {"forceInput": True, "multiline": True}),
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "timestamp")
    FUNCTION = "get_by_index"
    CATEGORY = "Subtitle Tools"

    def get_by_index(self, subtitle_texts, subtitle_times, index):
        subs = subtitle_texts.strip().split("\n")
        times = subtitle_times.strip().split("\n")

        if 0 <= index < len(subs):
            text = subs[index].strip()
            timestamp = times[index] if index < len(times) else ""
            return (text, timestamp)
        else:
            return ("", "")

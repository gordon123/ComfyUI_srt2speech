class SubtitleIteratorNode:
    def __init__(self):
        self.index = 0
        self.subs = []
        self.times = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "subtitle_texts": ("STRING", {"forceInput": True, "multiline": True}),
                "subtitle_times": ("STRING", {"forceInput": True, "multiline": True}),
                "next": (["Next"],),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("text", "timestamp")
    FUNCTION = "get_next"
    CATEGORY = "📺 Subtitle Tools"

    def get_next(self, subtitle_texts, subtitle_times, next):
        if isinstance(subtitle_texts, str):
            self.subs = subtitle_texts.strip().split("\n")
        if isinstance(subtitle_times, str):
            self.times = subtitle_times.strip().split("\n")

        if not self.subs or self.index >= len(self.subs):
            return ("", "")

        text = self.subs[self.index].strip()
        timestamp = self.times[self.index] if self.index < len(self.times) else ""
        self.index += 1

        return (text, timestamp)

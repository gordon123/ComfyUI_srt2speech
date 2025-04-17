#this node will make new directory srt_uploads in assets folder if it does not exist.
#Update the file path to your own directory if you want to use it in your own project.
#This node will read the srt file and return the subtitle text, timestamp, all subtitles, all timestamps and the srt file name.
import os
import re
import inflect

class GetSubtitleByIndex:
    @classmethod
    def INPUT_TYPES(cls):
        # Get base path dynamically (folder that this script is in)
        base_path = os.path.dirname(os.path.abspath(__file__))
        default_folder = os.path.join(base_path, "assets", "srt_uploads")
        os.makedirs(default_folder, exist_ok=True)

        srt_files = [f for f in os.listdir(default_folder) if f.lower().endswith(".srt")]
        if not srt_files:
            srt_files = ["(no .srt files found)"]

        return {
            "required": {
                "srt_file": (srt_files,),
                "index": ("INT", {"default": 0, "min": 0, "step": 1})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("subtitle_text", "timestamp", "all_subtitles", "all_timestamps", "srt_file")
    FUNCTION = "get_subtitle"
    CATEGORY = "📺 Subtitle Tools"

    def get_subtitle(self, srt_file, index):
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_path, "assets", "srt_uploads")
        file_path = os.path.join(folder_path, srt_file)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")

        subs = []
        times = []
        buffer = []
        for line in lines:
            if "-->" in line:
                times.append(line)
            elif line.strip().isdigit():
                continue
            elif line.strip() == "":
                if buffer:
                    subs.append(" ".join(buffer))
                    buffer = []
            else:
                buffer.append(line.strip())
        if buffer:
            subs.append(" ".join(buffer))

        if index < 0 or index >= len(subs):
            return ("", "", "No more subtitles!", "Subtitle index out of range", srt_file)

        text = subs[index]
        timestamp = times[index] if index < len(times) else ""

        # convert numbers to words
        engine = inflect.engine()
        def replace_numbers(t):
            return re.sub(r'\d+(\.\d+)?', lambda x: engine.number_to_words(x.group()), t)

        text = replace_numbers(text)

        return (text, timestamp, "\n".join(subs), "\n".join(times), srt_file)

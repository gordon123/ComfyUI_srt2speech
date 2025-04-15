import os
import re
import inflect

class GetSubtitleByIndex:
    @classmethod
    def INPUT_TYPES(cls):
        default_folder = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/srt_uploads"
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
    CATEGORY = "\ud83d\udcfa Subtitle Tools"

    def get_subtitle(self, srt_file, index):
        folder_path = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/srt_uploads"
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

        # แปลงตัวเลขในข้อความเป็นข้อความภาษาอังกฤษ
        engine = inflect.engine()
        def replace_numbers(t):
            return re.sub(r'\d+(\.\d+)?', lambda x: engine.number_to_words(x.group()), t)

        text = replace_numbers(text)

        return (text, timestamp, "\n".join(subs), "\n".join(times), srt_file)

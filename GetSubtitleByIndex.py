import os

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

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "timestamp", "all_subtitles", "all_timestamps")
    FUNCTION = "get_subtitle"
    CATEGORY = "Subtitle Tools"

    OUTPUT_NODE = True

    def get_subtitle(self, srt_file, index):
        folder_path = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/srt_uploads"
        file_path = os.path.join(folder_path, srt_file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return (f"Error reading file: {e}", "", "", "")

        blocks = content.strip().split("\n\n")
        subtitles = []
        timestamps = []

        for block in blocks:
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                time = lines[1]
                text = " ".join(lines[2:])
                timestamps.append(time)
                subtitles.append(text)

        selected_text = ""
        selected_time = ""

        if 0 <= index < len(subtitles):
            selected_text = subtitles[index]
            selected_time = timestamps[index]

        all_subtitles = "\n".join(subtitles)
        all_timestamps = "\n".join(timestamps)

        return (selected_text, selected_time, all_subtitles, all_timestamps)
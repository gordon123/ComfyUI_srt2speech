import os

class SRT2SpeechNode:
    default_folder = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/srt_uploads"

    @classmethod
    def INPUT_TYPES(cls):
        os.makedirs(cls.default_folder, exist_ok=True)
        srt_files = [f for f in os.listdir(cls.default_folder) if f.lower().endswith(".srt")]
        if not srt_files:
            srt_files = ["(no .srt files found)"]

        return {
            "required": {
                "srt_file": (srt_files,),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "read_srt"
    CATEGORY = "Subtitle Tools"

    def read_srt(self, srt_file):
        file_path = os.path.join(self.default_folder, srt_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {e}"
        return (content,)
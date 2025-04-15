import os

class SRT2SpeechNode:
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
            },
            "hidden": {
                "folder_path": default_folder
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "read_srt"
    CATEGORY = "📺 Subtitle Tools"

    def read_srt(self, srt_file, folder_path):
        file_path = os.path.join(folder_path, srt_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {e}"
        return (content,)  # ต้อง return เป็น tuple เสมอ

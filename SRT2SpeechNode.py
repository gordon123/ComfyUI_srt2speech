import os

class SRT2SpeechNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "D:/MyStuff/srt_uploads",
                    "multiline": False
                })
            },
            "optional": {
                "refresh_list": (["Refresh"],)
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "read_srt"
    CATEGORY = "Custom"

    def read_srt(self, folder_path, refresh_list="Refresh"):
        try:
            srt_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".srt")]
            if not srt_files:
                return ("No .srt files found in folder.",)

            options = "\n".join(srt_files)
            return (f"Found SRT files:\n{options}\n(Use a dropdown selector version to load one)",)
        except Exception as e:
            return (f"Error accessing folder: {e}",)

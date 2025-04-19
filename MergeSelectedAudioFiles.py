import os
import inspect
from ..utils.shared_types import any_typ  # สมมติว่ามี shared type
import folder_paths  # หรือวิธีอื่นในการ resolve path

class SelectMultipleAudioFiles:
    @classmethod
    def INPUT_TYPES(cls):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio_out")
        audio_files = [f for f in os.listdir(base_path) if f.endswith(".wav")]
        audio_files.sort()

        dyn_inputs = {
            "file1": (audio_files, {"tooltip": "Select first audio file"})
        }

        # Dynamic: ถ้ากำลังสร้าง input info
        if inspect.stack()[2].function == "get_input_info":
            class AllInputs:
                def __contains__(self, key):
                    return True

                def __getitem__(self, key):
                    return (audio_files, {"tooltip": f"Select audio file {key}"})

            dyn_inputs = AllInputs()

        return {
            "required": dyn_inputs,
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("selected_files",)
    FUNCTION = "get_files"
    CATEGORY = "📺 Subtitle Tools / 📁 File Tools"

    def get_files(self, **kwargs):
        file_list = []
        for k, v in kwargs.items():
            if k.startswith("file") and isinstance(v, str):
                file_list.append(v)
        return (file_list,)

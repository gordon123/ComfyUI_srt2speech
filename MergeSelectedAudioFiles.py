import os
import re
from pydub import AudioSegment
from nodes import core  # ✅ Import core to support dynamic UI

class MergeSelectedAudioFiles:
    @classmethod
    def INPUT_TYPES(cls):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio_out")
        audio_files = [f for f in os.listdir(base_path) if f.endswith(".wav")]
        audio_files.sort()

        dyn_inputs = {
            "file1": (audio_files, {"tooltip": "Select first audio file to merge"})
        }

        # ✅ Enable dynamic dropdowns when ComfyUI supports it
        if core.is_execution_model_version_supported():
            class AllInputs:
                def __contains__(self, key): return True
                def __getitem__(self, key): return (audio_files, {"tooltip": f"Select audio file {key}"})
            dyn_inputs = AllInputs()

        return {
            "required": dyn_inputs,
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge"
    CATEGORY = "\ud83d\udcc1 File Tools"

    def merge(self, **kwargs):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(base_path, "assets", "audio_out")
        output_path = os.path.join(base_path, "assets", "merged_selected.wav")

        # Collect selected files
        selected_files = [v for k, v in sorted(kwargs.items()) if k.startswith("file") and isinstance(v, str)]
        segments = []
        for fname in selected_files:
            fpath = os.path.join(audio_path, fname)
            if os.path.exists(fpath):
                try:
                    seg = AudioSegment.from_file(fpath)
                    segments.append(seg)
                except Exception as e:
                    print(f"[ERROR] Failed to load: {fname} → {e}")

        if segments:
            merged = segments[0]
            for s in segments[1:]:
                merged += s
            merged.export(output_path, format="wav")
            print(f"[INFO] Exported merged WAV: {output_path}")
        else:
            output_path = "No valid audio files to merge."

        return (output_path,)

import os
from pydub import AudioSegment

class MergeSelectedAudioFiles:
    @classmethod
    def INPUT_TYPES(cls):
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio_out")
        audio_files = [f for f in os.listdir(base_path) if f.endswith(".wav")]
        audio_files.sort()

        return {
            "required": {
                "file1": (audio_files,),
                "file2": (audio_files,),
                "file3": (audio_files,),
                "file4": (audio_files,),
                "file5": (audio_files,),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_path",)
    FUNCTION = "merge"
    CATEGORY = "📁 File Tools"

    def merge(self, file1, file2, file3, file4, file5):
        base_path = os.path.dirname(os.path.abspath(__file__))
        audio_path = os.path.join(base_path, "assets", "audio_out")
        output_path = os.path.join(base_path, "assets", "merged_selected.wav")

        files = [file1, file2, file3, file4, file5]
        segments = []
        for fname in files:
            if not fname:
                continue
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

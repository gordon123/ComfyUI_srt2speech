import os
import re
import soundfile as sf

class SaveWAVNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING", {"multiline": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save_wav"
    CATEGORY = "Subtitle Tools"

    def save_wav(self, audio, timestamp):
        output_dir = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/audio_out"
        os.makedirs(output_dir, exist_ok=True)

        clean_name = re.sub(r"[^0-9]", "_", timestamp)
        filename = f"{clean_name}.wav"
        save_path = os.path.join(output_dir, filename)

        try:
            waveform = audio["waveform"].squeeze().cpu().numpy()
            sample_rate = audio["sample_rate"]
            sf.write(save_path, waveform, sample_rate)
            return (save_path,)
        except Exception as e:
            return (f"Error saving WAV: {e}",)
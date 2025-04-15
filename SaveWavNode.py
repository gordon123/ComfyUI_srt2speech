import os
import re
import soundfile as sf

class SaveWAVNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "waveform": ("TENSOR",),
                "sample_rate": ("INT",),
                "timestamp": ("STRING", {"multiline": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_path",)
    FUNCTION = "save_wav"
    CATEGORY = "📺 Subtitle Tools"

    def save_wav(self, waveform, sample_rate, timestamp):
        output_dir = "/workspace/ComfyUI/custom_nodes/ComfyUI_srt2speech/assets/audio_out"
        os.makedirs(output_dir, exist_ok=True)

        # clean timestamp to use in filename (replace : and , with _)
        clean_name = re.sub(r"[^0-9]", "_", timestamp)
        filename = f"{clean_name}.wav"
        save_path = os.path.join(output_dir, filename)

        try:
            waveform_np = waveform.squeeze().cpu().numpy()
            sf.write(save_path, waveform_np, sample_rate)
            return (save_path,)
        except Exception as e:
            return (f"Error saving WAV: {e}",)

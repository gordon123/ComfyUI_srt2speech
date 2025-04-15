import os
import torch
import soundfile as sf

class SaveWAVNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING",),
                "srt_file": ("STRING",),
            }
        }

    RETURN_TYPES = ("STRING", "AUDIO")
    RETURN_NAMES = ("saved_path", "audio")
    FUNCTION = "save_audio"
    CATEGORY = "\ud83c\udfa7 Audio Tools"

    def save_audio(self, audio, timestamp, srt_file):
        output_dir = os.path.join(
            os.path.dirname(__file__), "assets/audio_out"
        )
        os.makedirs(output_dir, exist_ok=True)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        # Clean timestamp for filename
        time_tag = timestamp.replace(":", "_").replace(",", "_").replace(" ", "___")

        # Extract srt base name (e.g., test-5min from test-5min.srt)
        srt_name = os.path.splitext(os.path.basename(srt_file))[0]

        filename = f"{time_tag}__{srt_name}.wav"
        full_path = os.path.join(output_dir, filename)

        try:
            sf.write(full_path, waveform.squeeze(0).cpu().numpy(), sample_rate)
        except Exception as e:
            return (f"Failed to save: {e}", audio)

        return (full_path, audio)

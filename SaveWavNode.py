import os
import torch
import soundfile as sf
import re

class SaveWAVNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING",),
                "srt_file": ("STRING", {"multiline": False, "default": "test.srt"})
            }
        }

    RETURN_TYPES = ("STRING", "AUDIO")
    RETURN_NAMES = ("saved_path", "audio")
    FUNCTION = "save"
    CATEGORY = "📺 Subtitle Tools"

    def save(self, audio, timestamp, srt_file):
        folder = "./custom_nodes/ComfyUI_srt2speech/assets/audio_out"
        os.makedirs(folder, exist_ok=True)

        def sanitize_filename(name):
            return re.sub(r"[^\w\-_.]", "_", name)

        safe_timestamp = sanitize_filename(timestamp.replace("-->", "to").replace(",", "_").replace(":", "_"))
        safe_srt = sanitize_filename(srt_file.replace(".srt", ""))
        filename = f"{safe_timestamp}__{safe_srt}.wav"
        full_path = os.path.join(folder, filename)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        sf.write(full_path, waveform.squeeze().cpu().numpy(), samplerate=sample_rate)

        return (full_path, audio)

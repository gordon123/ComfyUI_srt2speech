import os
import re
import torchaudio
import torch

class SaveWAVNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING", "AUDIO",)
    RETURN_NAMES = ("saved_path", "audio",)
    FUNCTION = "save_wav"
    CATEGORY = "📺 Subtitle Tools"

    def format_timestamp(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return f"{int(h):02}_{int(m):02}_{int(s)}s{int(ms)}ms"

    def save_wav(self, audio, timestamp, srt_file):
        folder = "./custom_nodes/ComfyUI_srt2speech/assets/audio_out"
        os.makedirs(folder, exist_ok=True)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        # ✅ Fix waveform shape and backend
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)  # [samples] → [1, samples]
        elif waveform.ndim == 3:
            waveform = waveform.squeeze(0)    # [1, channels, samples] → [channels, samples]
        elif waveform.ndim != 2:
            raise ValueError(f"Unexpected waveform shape: {waveform.shape}")

        # ✅ Use sox_io to avoid FFmpeg-related issues
        torchaudio.set_audio_backend("sox_io")

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start = self.format_timestamp(match.group(1))
            end = self.format_timestamp(match.group(2))

        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        filepath = os.path.join(folder, filename)

        print(f"Saving WAV: shape={waveform.shape}, sample_rate={sample_rate}, name={filename}")
        torchaudio.save(filepath, waveform, sample_rate)

        return (filepath, audio)

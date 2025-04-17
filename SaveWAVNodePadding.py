# -*- coding: utf-8 -*-
# Save audio with optional dummy padding using appropriate dummy sample rate

import os
import re
import torchaudio
import torch

class SaveWavNodePadding:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False, "default": ""}),
                "pad_with_dummy": ("BOOLEAN", {"default": False})
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

    def get_seconds(self, t):
        t = t.replace(",", ".")
        h, m, s = t.split(":")
        s, ms = s.split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    def save_wav(self, audio, timestamp, srt_file, pad_with_dummy):
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_path, "assets", "audio_out")
        os.makedirs(folder, exist_ok=True)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        elif waveform.ndim == 3:
            waveform = waveform.squeeze(0)
        elif waveform.ndim != 2:
            raise ValueError(f"Unexpected waveform shape: {waveform.shape}")

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)

            if pad_with_dummy:
                start_sec = self.get_seconds(start_time)
                end_sec = self.get_seconds(end_time)
                target_duration = end_sec - start_sec
                current_duration = waveform.shape[1] / sample_rate
                if current_duration < target_duration:
                    missing_samples = int((target_duration - current_duration) * sample_rate)
                    dummy_filename = f"dummy{sample_rate//1000}khz.wav"
                    dummy_path = os.path.join(base_path, "assets", dummy_filename)
                    dummy, dummy_sr = torchaudio.load(dummy_path)
                    if dummy_sr != sample_rate:
                        raise ValueError(f"Sample rate mismatch: dummy {dummy_sr} vs audio {sample_rate}")
                    if dummy.shape[1] < missing_samples:
                        reps = (missing_samples // dummy.shape[1]) + 1
                        dummy = dummy.repeat(1, reps)
                    waveform = torch.cat([waveform, dummy[:, :missing_samples]], dim=1)

        torchaudio.set_audio_backend("sox_io")  # ✅ Safe backend
        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        filepath = os.path.join(folder, filename)

        print(f"[INFO] Saving WAV: shape={waveform.shape}, sample_rate={sample_rate}, name={filename}")
        torchaudio.save(filepath, waveform, sample_rate)

        return (filepath, audio)

# -*- coding: utf-8 -*-
# This node will fill the quiet time with silence if TTS ends before the subtitle ends

import os
import re
import torchaudio
import torch
import torch.nn.functional as F

class SaveWavNodePadding:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                "timestamp": ("STRING", {"multiline": False}),
                "srt_file": ("STRING", {"multiline": False, "default": ""}),
                "pad_audio": ("BOOLEAN", {"default": True})
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

    def pad_audio_to_duration(self, waveform, sample_rate, target_duration_sec):
        print(f"[DEBUG] Padding check - waveform shape: {waveform.shape}, sample_rate: {sample_rate}, target_duration_sec: {target_duration_sec}")
        current_duration = waveform.shape[1] / sample_rate
        if current_duration < target_duration_sec:
            pad_samples = int((target_duration_sec - current_duration) * sample_rate)
            print(f"[DEBUG] Padding with {pad_samples} samples")
            return F.pad(waveform, (0, pad_samples))
        return waveform

    def save_wav(self, audio, timestamp, srt_file, pad_audio):
        base_path = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(base_path, "assets", "audio_out")
        dummy_path = os.path.join(base_path, "assets", "dummy.wav")
        os.makedirs(folder, exist_ok=True)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        print(f"[DEBUG] Raw waveform shape: {waveform.shape}")

        try:
            if waveform.ndim == 1:
                waveform = waveform.unsqueeze(0)
                print("[DEBUG] Reshaped 1D to 2D waveform")
            elif waveform.ndim == 3:
                waveform = waveform.squeeze(0)
                print("[DEBUG] Squeezed 3D to 2D waveform")
            elif waveform.ndim != 2:
                raise ValueError(f"[ERROR] Invalid waveform shape: {waveform.shape}")
        except Exception as e:
            print(f"[FALLBACK] waveform error: {e} → loading dummy")
            waveform, sample_rate = torchaudio.load(dummy_path)

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)

            if pad_audio:
                start_sec = self.get_seconds(start_time)
                end_sec = self.get_seconds(end_time)
                waveform = self.pad_audio_to_duration(waveform, sample_rate, end_sec - start_sec)

        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        filepath = os.path.join(folder, filename)

        try:
            print(f"[INFO] Saving WAV: shape={waveform.shape}, sample_rate={sample_rate}, name={filename}")
            torchaudio.save(filepath, waveform, sample_rate)
        except Exception as e:
            print(f"[FALLBACK] Save failed: {e} → using dummy")
            waveform, sample_rate = torchaudio.load(dummy_path)
            torchaudio.save(filepath, waveform, sample_rate)

        return (filepath, audio)

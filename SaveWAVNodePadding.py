# ✅ Fix waveform shape and backend. This node will save the audio into the wav format. file name with the timestamp.
# ✅ Add dummy merge to fill silence if needed (PyDub)

import os
import re
import torchaudio
import torch
from pydub import AudioSegment

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

    def save_wav(self, audio, timestamp, srt_file, pad_audio):
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

        torchaudio.set_audio_backend("sox_io")

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            start = self.format_timestamp(start_time)
            end = self.format_timestamp(end_time)

            audio_segment = AudioSegment(
                waveform.numpy().T.tobytes(),
                frame_rate=sample_rate,
                sample_width=waveform.element_size(),
                channels=waveform.shape[0]
            )

            if pad_audio:
                actual_ms = len(audio_segment)
                target_ms = int((self.get_seconds(end_time) - self.get_seconds(start_time)) * 1000)

                if actual_ms < target_ms:
                    dummy_path = os.path.join(base_path, "assets", f"dummy{sample_rate // 1000}khz.wav")
                    dummy = AudioSegment.from_file(dummy_path)[:(target_ms - actual_ms)]
                    audio_segment += dummy

        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        filepath = os.path.join(folder, filename)

        audio_segment.export(filepath, format="wav")

        return (filepath, audio)

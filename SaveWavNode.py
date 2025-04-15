import os
import re
import torchaudio

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

    def save_wav(self, audio, timestamp, srt_file):
        folder = "./custom_nodes/ComfyUI_srt2speech/assets/audio_out"
        os.makedirs(folder, exist_ok=True)

        waveform = audio["waveform"]
        sample_rate = audio["sample_rate"]

        def clean(t):
            return re.sub(r"[^\d_]", "", t.replace(",", ".").replace(":", "_"))

        start, end = "start", "end"
        match = re.match(r"(.+?) --> (.+)", timestamp)
        if match:
            start = clean(match.group(1))
            end = clean(match.group(2))

        base_name = os.path.splitext(os.path.basename(srt_file))[0] if srt_file else "nosrt"
        filename = f"{start}_to_{end}__{base_name}.wav"
        filepath = os.path.join(folder, filename)

        torchaudio.save(filepath, waveform, sample_rate)
        return (filepath, audio)
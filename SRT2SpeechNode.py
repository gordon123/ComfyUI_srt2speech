import os
import srt
from TTS.api import TTS

class SRT2SpeechNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "srt_file": ("STRING", {"default": ""}),
                "output_dir": ("STRING", {"default": "output_audio"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "srt_to_speech"
    CATEGORY = "Audio"

    def srt_to_speech(self, srt_file, output_dir):
        # อ่านไฟล์ .srt
        with open(srt_file, "r", encoding="utf-8") as f:
            subs = list(srt.parse(f.read()))

        # สร้างโฟลเดอร์สำหรับไฟล์เสียง
        os.makedirs(output_dir, exist_ok=True)

        # โหลดโมเดล TTS
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

        # แปลงแต่ละข้อความเป็นเสียง
        for i, sub in enumerate(subs):
            text = sub.content
            audio_path = os.path.join(output_dir, f"segment_{i}.wav")
            tts.tts_to_file(text=text, file_path=audio_path)

        return (f"Audio files saved in {output_dir}",)

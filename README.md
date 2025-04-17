# ComfyUI_srt2speech
This repo is my first Custom node with my very basic knowledge of coding, ComfyUI_srt2speech​ <br> 
I tested this TTS3 on the Runpod, with ComfyUI native installing. <br>  
I make this custom node to read srt subtitle file and send it to MegaTTS node to generate dub Eng, or Chinese for now.​ <br> 
It should work with other TTS or similar for ComfyUI, in the end I wil combine with Wan2.1 or any other Lipsync. ​ <br> 
My aim try to do !1CLICK make all the job.​ <br> 
(ComfyUI portable version, please use embed python folder!)  <br> 

This instruction for myself is using [Runpod.com Gpu cloud service](https://runpod.io?ref=c0v5p0ys), if you use your own local computer, please check your file path. <br>

## For my personal TESTING repo! I use MegaTTS as text to speech, install this repo first.

1. Install ComfyUI-MegaTTS custom node via custom manager [ComfyUI-MegaTTS](https://github.com/1038lab/ComfyUI-MegaTTS) <br>
2. Go to custom node,
   
```
pip install -r requirements.ext
```
   
3. Install ffmpeg, ffmprobe
   
```   
apt update && apt install -y ffmpeg
```

4. restart ComfyUI <br>
5. create your own 10sec-15sec *.wav file with mono! 16-24 kHz, or take any .wav file in this repo folder <br>
6. use Voice maker to download all the model first time ! <br>
7. it will create new folder in /workspace/ComfyUI/models/TTS and all models from [MegaTTS3](https://huggingface.co/ByteDance/MegaTTS3) <br>
8. copy .wav and .npy from assets example files into  /workspace/ComfyUI/custom_nodes/ComfyUI-MegaTTS/voices <br>
9. now it ready to do Text2speech <br>

--- 
**===== to create your own voice model ===** <br>

1. I use Audacity to record myself about 10-15sec, reading some English clearly avoid noise <br>
2. Export it as a "*.wav" (Make file name for your to remember easily) with Mono, 16 - 24 kHz and upload here ["wav_queue" folder of Google drive](https://drive.google.com/drive/folders/1gCWL1y_2xu9nIFhUX_OW5MbcFuB7J5Cl) <br>
**PS support only English, Chinese  <br>
** For security reason, they don't release encoder  <br> 

4. Wait a few days,  Developer will give you a file with trained to your voice *.npy and *.wav here ["user_batch_1"](https://drive.google.com/drive/folders/1QhcHWcy20JfqWjgqZX1YM3I6i9u4oNlr) <br>

---
**To install my repo**
1. use git clone
then activate virtual environment 
```
source myvenv/bin/activate
```
2. pip instal the requirements.txt

---
**To download files in my asset to the Runpod workspace, activate venv.**  <br>
These files for my own Convenient to use this demo voice for my code, it is the same from original TTS3 repo in the google drive above, if you are using Runpod, you can use code below to copy it into MegaTTS/voices

```
source myvenv/bin/activate
```
download all .wav and .npy, copy and paste the code below into the Runpod terminal <br>

MegaTTS node require, .wav file or .nyp file put in their custom node | ComfyUI/custom_nodes/ComfyUI-MegaTTS/voices folder <br>

```
python3 -c "
import os, requests
out = '/workspace/ComfyUI/custom_nodes/ComfyUI-MegaTTS/voices'
os.makedirs(out, exist_ok=True)
api_url = 'https://api.github.com/repos/gordon123/ComfyUI_srt2speech/contents/assets/wav-npy'
r = requests.get(api_url)
for f in r.json():
    if f['name'].endswith(('.wav', '.npy')):
        print('Downloading', f['name'])
        data = requests.get(f['download_url']).content
        with open(os.path.join(out, f['name']), 'wb') as out_file:
            out_file.write(data)
"

```

---
**To use my Custom node**
--- SOON ----




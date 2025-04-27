[![ดูคลิปนี้บน YouTube](https://img.youtube.com/vi/pXEbXhNceUo/hqdefault.jpg)](https://youtu.be/pXEbXhNceUo)
How to use, check in youtube.

# ComfyUI_srt2speech
This repo is my first Custom node with my very basic knowledge of coding, ComfyUI_srt2speech​ <br> 
I tested my srt2speech with other ComfyUI_MegaTTS custom node on the Runpod, with ComfyUI native installing. <br>  
I make this custom node to read srt subtitle file and send it to MegaTTS node to generate dub Eng, or Chinese for now.​ <br> 
It should work with other TTS or similar for ComfyUI, in the end I will combine with Wan2.1 or any other Lipsync. ​ <br> 
My aim try to do !1CLICK make all the job.​ <br> 

This instruction for myself is using [Runpod.com Gpu cloud service](https://runpod.io?ref=c0v5p0ys), if you use your own local computer, please check your file path. <br>

## For my personal TESTING repo! I use MegaTTS as text to speech, install this repo first.

1. Install ComfyUI-MegaTTS custom node via custom manager [ComfyUI-MegaTTS](https://github.com/1038lab/ComfyUI-MegaTTS) by AIlab <br>
2. Go to custom node,
   
```
pip install -r requirements.txt
```
   
3. Install ffmpeg, ffmprobe
   
```   
apt update && apt install -y ffmpeg
```

4. restart ComfyUI <br>
5. create your own 10sec-15sec *.wav file with mono! 16-24 kHz, or take any .wav file in this asset folder <br>
6. use Voice maker to download all the model first time ! <br>
7. it will create new folder in /workspace/ComfyUI/models/TTS and all models from [MegaTTS3](https://huggingface.co/ByteDance/MegaTTS3) <br>
8. copy .wav and .npy from assets example files into  /workspace/ComfyUI/custom_nodes/ComfyUI-MegaTTS/voices <br>
9. now it ready to do Text2speech <br>

--- 
**===== to clone your own voice model from MegaTTS custom node ===** <br>

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
**To download files in my asset to the Runpod workspace, activate venv first. If you use your local computer just copy/paste and ignore code below**  <br>
These files for my own Convenient to use this demo voice for my code, it is the same from original TTS3 repo in the google drive above. If you are using Runpod, you can use code below to copy it into ComfyUI_MegaTTS/voices

```
source myvenv/bin/activate
```
To download all *.wav and *.npy from my asset folder, copy and paste the code below into the Runpod terminal in side voice folder of MegaTTS custom node <br>

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
If you are using ComfyUI-MegaTTS same as mine, you can follow instruction here, otherwise other TTS should also work.

1. install MegaTTS of AIlab via Custom manager
2. go to ComfyUI-MegaTTS  and run 

```
pip install -r requirements.txt
```

3. If you use local computer, check if you have ffmpeg, for me I use Runpod GPU cloud, linux system run this command

```   
apt update && apt install -y ffmpeg
```

Researt Comfyui server, reload webui page

4. Go to my [ComfyUI_srt2speech](https://github.com/gordon123/ComfyUI_srt2speech/tree/main/assets/wav-npy) download any models of .wav and .npy both must be the same name, and use wav file upload into voice maker click Run first time. **For more example how to clone your own voice go to ComfyUI-MegaTTS github page.

5. Run MegaTTS voice maker once. It will be downloaded  some models in this folder models/TTS/MegaTTS3
6. Restart ComfyUi, refresh webui
7. Upload all *.wav and *.npy into the ComfyUI-MegaTTS/voices/ folder (small voices)
8. Refresh webui and now you can use reference_voice in the MegaTTS3
![alt text](<example_workflow/srt2speech and MegaTTS3 workflow.png>)

9. set Run to run instant to be auto generated text2speech the whole subtitle

<img src="Screenshot 2025-04-19 at 20.50.41.png" alt="drawing" style="width:200px;"/> <br>
Enjoys!




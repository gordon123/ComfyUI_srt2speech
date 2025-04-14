# ComfyUI_srt2speech
ComfyUI_srt2speech​


## TESTING
Install this custom node in custom manager ComfyUI-MegaTTS <br>

ไปใน custom node, pip install -r requirements.ext <br>
apt update && apt install -y ffmpeg <br>

restart comfy <br>
create 10s *.wav file with mono! 16-24 kHz <br>

use Voice maker to download all the model first time ! <br>

it will create new folder in /workspace/ComfyUI/models/TTS <br>

copy .wav and .npy from assets example files into  /workspace/ComfyUI/custom_nodes/ComfyUI-MegaTTS/voices <br>

now it ready to do Text2speech <br>

===== to create your own voice model === <br>

I use Audacity to record myself about 10-15sec <br>
export "*.wav" (Make file name for your to remember easily) with mono, 16 - 24 kHz and upload here "wav_queue" folder of Google drive https://drive.google.com/drive/folders/1gCWL1y_2xu9nIFhUX_OW5MbcFuB7J5Cl <br>
support only Eng, Chinese  <br> 

wait a few days you will get your file with .npy here "user_batch_1" https://drive.google.com/drive/folders/1QhcHWcy20JfqWjgqZX1YM3I6i9u4oNlr <br>

```
source myvenv/bin/activate
```
download all .wav and .npy
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






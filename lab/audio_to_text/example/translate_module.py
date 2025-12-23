import os
from pathlib import Path
from multimodaltranslation.audio.translate import translate_audio



script_dir = Path(__file__).resolve()
AUDIO_PATH = str(script_dir.parent.parent.parent.parent)
AUDIO_PATH = os.path.join(AUDIO_PATH,"audio_files","sample1","english.wav")

with open(AUDIO_PATH, "rb") as f:
    AUDIO_BYTES = f.read()

audio_str = AUDIO_BYTES.hex()
translation = translate_audio(AUDIO_BYTES, "en", ["fr"])
print(translation)

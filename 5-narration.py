# from gtts import gTTS
# story="Here are more damn trees. Stupid trees!"
# tts = gTTS(story, lang="en")
# tts.save("narration.mp3")


from elevenlabs.client import ElevenLabs
from elevenlabs import play
import json
from pathlib import Path

from dotenv import dotenv_values

config = dotenv_values(".env")
albumPath = config["albumPath"]

json_file_path = config["metadataFilePath"]


album_name = "sage"
client = ElevenLabs(
    api_key=config["elevenLabsApi"],
)

# with open("deepseekResponse.json", "r") as json_file:
#     response = json.load(json_file)

# Extract the response text
# response_text = response["response"]

# Split the response text by newline characters and filter out any empty lines
# lines = [line.strip() for line in response_text.split("\n") if line.strip()]

# # Now `lines` is a list of strings
# print(lines)
# print(len(lines))

with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

for metad in data:

    audio = client.text_to_speech.convert(
        text=metad["line"],
        voice_id="2N5vgOWfEOpjQLCuXlA6",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio)
    album_dir = Path(albumPath[:-1])
    fileName = ".".join(metad["filename"].split(".")[:-1]) + ".mp3"
    mp3File = album_dir / fileName
    with open(mp3File, "wb") as f:
        f.write(audio_bytes)

    print("Audio saved as narration.mp3")

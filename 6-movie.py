from moviepy.editor import *
import os
import json

from dotenv import dotenv_values

config = dotenv_values(".env")

albumPath = config["albumPath"]

ALBUM_NAME = config["ALBUM_NAME"]

json_file_path = config["metadataFilePath"]

output_video = albumPath + ALBUM_NAME + ".mp4"
flip_sound_path = "page-flip-47177.mp3"  # Sound effect for page flipping


with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Get sorted list of images and audio files
# images = [f for f in os.listdir(directory) if f.endswith((".png", ".jpg", ".jpeg"))]

# audios = [f for f in os.listdir(directory) if f.endswith(".mp3")]

# Ensure equal number of images and audio files
# if len(images) != len(audios):
#     print("Error: Number of images and audio files do not match.")
#     exit()

clips = []


# Create a short silence (0.5 seconds) between the flip sound and the main audio
# silence_duration =   # Adjust as needed
silence_front = AudioClip(lambda t: 0, duration=0.5, fps=44100)
silence_back = AudioClip(lambda t: 0, duration=0.2, fps=44100)
# flip_sound = AudioFileClip(flip_sound_path)


for i, metaData in enumerate(data):
    fileName = ".".join(metaData["filename"].split(".")[:-1])

    # Load audio and image
    audio_clip = AudioFileClip(albumPath + fileName + ".mp3")
    audio_clip = concatenate_audioclips([silence_front, audio_clip, silence_back])
    duration = audio_clip.duration
    image_clip = ImageClip(albumPath + fileName + ".jpg").set_duration(duration)

    transition = image_clip.crossfadein(0.5)

    # # Add page flipping effect (transition)
    # if i > 0:
    #     transition = image_clip.crossfadein(0.5)  # Smooth fade effect
    #     # clips.append(
    #     #     flip_sound.set_start(sum(c.duration for c in clips))
    #     # )  # Insert flip sound
    # else:
    #     transition = image_clip

    transition = transition.set_audio(audio_clip)  # Attach the respective audio
    clips.append(transition)

print(clips)
print(len(clips))
# Concatenate all clips
final_video = concatenate_videoclips(clips, method="compose")

# Write to file
final_video.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")

print(f"Video saved as {output_video}")

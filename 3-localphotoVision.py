import json
from google.cloud import vision


# Function to get labels from Google Vision API for a specific image
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

from dotenv import dotenv_values

config = dotenv_values(".env")

json_file_path = config["metadataFilePath"]
albumPath = config["albumPath"]


# Load model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def get_vision_labels(img_path):
    # Open image
    img = Image.open(img_path)

    # Generate caption
    inputs = processor(images=img, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    print("Generated Caption:", caption)
    return caption


# Function to update the JSON file with Vision API data
def update_json_with_vision_data(json_file_path):
    # Open the existing JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    print(data)
    # Iterate over each image ID and populate data
    for idx, imageMetadata in enumerate(data):
        image_path = imageMetadata["filename"]
        # Get vision labels for the image
        labels = get_vision_labels(albumPath + image_path)
        # Add the labels to the JSON data for that image ID
        data[idx]["description"] = labels

    # Save the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Updated {json_file_path} with Vision API data.")


# Update the JSON file with Vision API data
update_json_with_vision_data(json_file_path)

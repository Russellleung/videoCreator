import json
from google.cloud import vision

from dotenv import dotenv_values

config = dotenv_values(".env")

json_file_path = config["metadataFilePath"]
albumPath = config["albumPath"]

# Function to get labels from Google Vision API for a specific image
def get_vision_labels(image_path):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Open the image file
    with open(image_path, "rb") as img_file:
        content = img_file.read()

    # Create an Image object to send to the API
    image = vision.Image(content=content)

    # Perform label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations  # List of label annotations

    # Extract label descriptions and confidence scores
    label_data = []
    for label in labels:
        # label_data.append({"description": label.description, "confidence": label.score})
        label_data.append(label.description)
    return label_data


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
        print(labels)
        # Add the labels to the JSON data for that image ID
        data[idx]["labels"] = labels

    # Save the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Updated {json_file_path} with Vision API data.")


# # Example usage
# # Dictionary with image IDs and paths to the images
# images_data = {
#     'image_001': 'path_to_image_1.jpg',
#     'image_002': 'path_to_image_2.jpg',
#     'image_003': 'path_to_image_3.jpg',
# }

# Path to the existing JSON file


# Update the JSON file with Vision API data
update_json_with_vision_data(json_file_path)

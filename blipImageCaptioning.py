from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


# Load model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
# Open image
img_path = "Downloaded_Albums/sage/PXL_20250119_100306021.jpg"
img = Image.open(img_path)

# Generate caption
inputs = processor(images=img, return_tensors="pt")
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)

print("Generated Caption:", caption)

import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import matplotlib.pyplot as plt

# Set device to GPU if available, else fallback to CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load processor and model for 'microsoft/trocr-base-handwritten'
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=True)
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten').to(device)

# Function to read image and ensure it's in RGB format
def read_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return image

# OCR function to process image and predict text
def ocr(image, processor, model):
    # Preprocess the image and move to the appropriate device
    pixel_values = processor(image, return_tensors='pt').pixel_values.to(device)
    # Generate predictions (token IDs)
    generated_ids = model.generate(pixel_values)
    # Decode the generated tokens into text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

# Load the specific image
image_path = 'Hello_123.png'  # Image path in the same directory
image = read_image(image_path)

# Perform OCR
text = ocr(image, processor, model)


# Print the OCR result in the terminal
print("OCR Result: ", text)

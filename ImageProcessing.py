import torch
from nltkScraper import pos_dict2
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from textblob import TextBlob
import nltk

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=False)
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')


def read_image(image_path):
    image = Image.open(image_path).convert('RGB')
    return image


def ocr(image, processor, model):
    # Preprocess the image and move to the appropriate device
    pixel_values = processor(image, return_tensors='pt').pixel_values
    # Generate predictions (token IDs)
    generated_ids = model.generate(pixel_values)
    # Decode the generated tokens into text
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text


def filter_text(image_path):
    image = read_image(image_path)
    text = ocr(image, processor, model)
    final_text = ""
    for char in text:
        if char not in ("(", ")", ".", "\""):
            final_text += char
    print("Message:", final_text, "\n")
    return final_text


def spellcheck(text_to_correct):
    blob = TextBlob(text_to_correct)
    corrected_text = blob.correct()
    return str(corrected_text)


# Print the OCR result in the terminal
# print("OCR Result: ", text)


def sort_by_pos(text_to_sort):
    tokens = nltk.word_tokenize(text_to_sort)

    # Tagging parts of speech
    tags = nltk.pos_tag(tokens)

    # Create a dictionary to hold the words categorized by their part of speech
    pos_dict = {}

    for word, pos in tags:
        if pos not in pos_dict:
            pos_dict[pos] = []
        pos_dict[pos].append(word)

    # Print each part of speech tag followed by the words that belong to that tag
    for pos in pos_dict:
        definition = pos_dict2.get(pos)
        print(f"{pos} ({definition}): ")
        print(", ".join(pos_dict[pos]))
        print()


# Sort and display the POS tags with their corresponding words
# sort_by_pos(text)
stringy = filter_text("deskewed.jpg")
sort_by_pos(stringy)



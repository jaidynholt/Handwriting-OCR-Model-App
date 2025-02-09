import torch
from nltkScraper import pos_dict2
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from textblob import TextBlob
import nltk

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten', use_fast=False)
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')


def read_image(image_path):
    """opens and ensures image is in RGB format (trOCR likes RGB)"""
    image = Image.open(image_path).convert('RGB')
    return image


def ocr(image, processor, model):
    pixel_values = processor(image, return_tensors='pt').pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text


def filter_text(image_path):
    """Calls ocr function and ensures only digits, spaces and alphabetical charactors are allo"""
    image = read_image(image_path)
    text = ocr(image, processor, model)
    final_text = ""
    for char in text:
        if char.isalpha() or char.isspace() or char.isdigit():
            final_text += char
    print("Message:", final_text, "\n")
    return final_text


def spellcheck(text_to_correct):
    """ Optional function to run a spell check on outputted text - may be less effective """
    blob = TextBlob(text_to_correct)
    corrected_text = blob.correct()
    return str(corrected_text)



def sort_by_pos(text_to_sort):
    """Utilizes ntlk library to classify the part(s) of speech your word/phrase consists of"""
    tokens = nltk.word_tokenize(text_to_sort)
    tags = nltk.pos_tag(tokens)

    # Create a dictionary to hold the words categorized by their part of speech
    pos_dict = {}

    for word, pos in tags:
        if pos not in pos_dict:
            pos_dict[pos] = []
        pos_dict[pos].append(word)

    for pos in pos_dict:
        definition = pos_dict2.get(pos)
        print(f"{pos} ({definition}): ")
        print(", ".join(pos_dict[pos]))
        print()


# Sort and display the POS tags with their corresponding words
# sort_by_pos(text)
stringy = filter_text("final_output.jpg")
sort_by_pos(stringy)



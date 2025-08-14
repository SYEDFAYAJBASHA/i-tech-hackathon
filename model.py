!sudo apt-get install tesseract-ocr -y
!sudo apt-get install poppler-utils -y
!pip install pytesseract opencv-python-headless transformers pdf2image img2pdf gradio

import cv2
import pytesseract
import re
from matplotlib import pyplot as plt
from google.colab import files
from pytesseract import Output
from transformers import pipeline
import pdf2image
import img2pdf
import io
import os
from PIL import Image
import numpy as np
import gradio as gr

try:
    ner = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER")
    print("BERT NER model initialized successfully.")
    bert_available = True
except Exception as e:
    print(f"BERT model initialization failed: {e}")
    print("Proceeding with no redaction if AI is unavailable.")
    bert_available = False

def is_sensitive(word):
    if not bert_available:
        return False, "Skipped due to unavailable AI"
    entities = ner(word)
    for entity in entities:
        if entity['entity'].startswith(('B-PER', 'I-PER', 'B-ORG', 'I-ORG', 'B-LOC', 'I-LOC')):
            return True, f"Contains {entity['entity'].split('-')[1]} entity"
    if re.match(r'\S+@\S+\.\S+', word):  # Email
        return True, "Contains an email address"
    if re.fullmatch(r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}', word):  # Date
        return True, "Contains a date"
    if re.fullmatch(r'[\d\$\.,]+', word):  # Financial data
        return True, "Contains financial data"
    return False, "Non-sensitive text"

def process_image(img, filename):
    config = r'--oem 3 --psm 6'
    ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT, config=config)
    n_boxes = len(ocr_data['text'])
    redaction_log = []
    for i in range(n_boxes):
        word = ocr_data['text'][i].strip()
        if word == "":
            continue
        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]
        redact, reason = is_sensitive(word)
        if redact:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
            redaction_log.append(f"Word: {word}, Reason: {reason}")
        else:
            redaction_log.append(f"Word: {word}, Reason: {reason} (kept)")
    return img, redaction_log

def process_pdf(pdf_path):
    images = pdf2image.convert_from_path(pdf_path)
    redacted_images = []
    all_redaction_logs = []
    for i, img in enumerate(images):
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        redacted_img, redaction_log = process_image(img_cv, f"page_{i+1}")
        redacted_images.append(Image.fromarray(cv2.cvtColor(redacted_img, cv2.COLOR_BGR2RGB)))
        all_redaction_logs.extend([f"Page {i+1}: {log}" for log in redaction_log])
    output_pdf = "redacted_output.pdf"
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert([img.tobytes() for img in redacted_images]))  # Fixed conversion
    # Return first page as image for display
    if redacted_images:
        return redacted_images[0], "\n".join(all_redaction_logs)
    return None, "No pages processed"

def process_text(text_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = text.split()
    redacted_text = []
    redaction_log = []
    for word in words:
        if not word.strip():
            redacted_text.append(word)
            continue
        redact, reason = is_sensitive(word)
        if redact:
            redacted_text.append("[REDACTED]")
            redaction_log.append(f"Word: {word}, Reason: {reason}")
        else:
            redacted_text.append(word)
            redaction_log.append(f"Word: {word}, Reason: {reason} (kept)")
    output_text = "redacted_output.txt"
    with open(output_text, 'w', encoding='utf-8') as f:
        f.write(" ".join(redacted_text))
    return output_text, redaction_log

def process_file(file):
    file_path = file.name
    file_extension = os.path.splitext(file_path)[1].lower()
    output_file = None
    redaction_log = []

    if file_extension in ('.png', '.jpg', '.jpeg'):
        print(f"Processing image file: {file_path}")
        img = cv2.imread(file_path)
        redacted_img, redaction_log = process_image(img, file_path)
        output_file = "redacted_output.png"
        cv2.imwrite(output_file, redacted_img)
        return redacted_img, "\n".join(redaction_log)

    elif file_extension == '.pdf':
        print(f"Processing PDF file: {file_path}")
        redacted_img, redaction_log = process_pdf(file_path)
        if redacted_img is not None:
            return redacted_img, redaction_log
        return None, redaction_log

    elif file_extension == '.txt':
        print(f"Processing text file: {file_path}")
        output_file, redaction_log = process_text(file_path)
        with open(output_file, 'r', encoding='utf-8') as f:
            return f.read(), "\n".join(redaction_log)

    else:
        return None, "Unsupported file type. Please upload a .png, .jpg, .jpeg, .pdf, or .txt file."

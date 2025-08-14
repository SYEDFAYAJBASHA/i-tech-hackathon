# Document Redaction Tool

This Python application redacts sensitive information from images, PDFs, and text files using OCR (Optical Character Recognition) and Named Entity Recognition (NER). It identifies and masks sensitive data such as names, organizations, locations, emails, dates, and financial information, providing a redacted output and a log of the redaction process.

## Features
- **Supported File Types**: Processes `.png`, `.jpg`, `.jpeg`, `.pdf`, and `.txt` files.
- **Sensitive Data Detection**: Uses a BERT-based NER model (`dslim/bert-base-NER`) to identify entities like persons, organizations, and locations, along with regex patterns for emails, dates, and financial data.
- **Redaction**: Masks sensitive information in images and PDFs by overlaying black rectangles and replaces sensitive text in `.txt` files with `[REDACTED]`.
- **Output**: Generates redacted files (images as `.png`, PDFs as `.pdf`, text as `.txt`) and a detailed redaction log.
- **User Interface**: Provides a Gradio-based web interface for easy file uploads and visualization of results.

## Requirements
To run the application, install the following dependencies:

```bash
sudo apt-get install tesseract-ocr -y
sudo apt-get install poppler-utils -y
pip install pytesseract opencv-python-headless transformers pdf2image img2pdf gradio
Dependencies

Python Libraries:

cv2 (OpenCV): Image processing.
pytesseract: OCR for extracting text from images and PDFs.
transformers: BERT-based NER model for entity detection.
pdf2image: Converts PDF pages to images.
img2pdf: Converts images back to PDF for redacted output.
gradio: Web-based interface for user interaction.
numpy, PIL: Image handling and manipulation.
re: Regular expressions for detecting emails, dates, and financial data.
matplotlib: Optional for visualizing images (not used in the core functionality).


System Dependencies:

tesseract-ocr: OCR engine.
poppler-utils: PDF manipulation tools.



Installation

Clone this repository:
bashgit clone https://github.com/your-username/document-redaction-tool.git
cd document-redaction-tool

Install system dependencies:
bashsudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils -y

Install Python dependencies:
bashpip install -r requirements.txt

(Optional) Create a requirements.txt file:
textpytesseract
opencv-python-headless
transformers
pdf2image
img2pdf
gradio
numpy
pillow


Usage

Run the application:
bashpython redaction_tool.py

Access the Gradio interface:

The script launches a web interface (locally or publicly if share=True).
Upload a .png, .jpg, .jpeg, .pdf, or .txt file.
View the redacted output (image or text) and the redaction log.


Output:

Images: Redacted image saved as redacted_output.png.

PDFs: Redacted PDF saved as redacted_output.pdf.
Text Files: Redacted text saved as redacted_output.txt.
A redaction log details which words were redacted and why.



Example

Upload a PDF containing sensitive information (e.g., names, emails).
The tool processes each page, identifies sensitive data, and masks it.
Output includes:

A redacted PDF with black rectangles over sensitive text.
A log like:
textPage 1: Word: John, Reason: Contains PER entity
Page 1: Word: example@email.com, Reason: Contains an email address
Page 1: Word: Hello, Reason: Non-sensitive text (kept)




Notes

NER Model: The application uses dslim/bert-base-NER. If the model fails to initialize, it falls back to regex-based redaction (emails, dates, financial data).
Limitations:


  

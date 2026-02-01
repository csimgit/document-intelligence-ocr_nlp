## OCR + NLP End-to-End Pipeline 

![Demo](demo/image_to_text_demo.gif)

An end-to-end **Optical Character Recognition (OCR) and Natural Language Processing (NLP)** system built for extracting structured text and insights from images, screenshots, and handwritten notes.
Supports screen auto-capture, snipping-style region selection, multilingual and handwritten OCR, followed by NLP tasks including summarization, named entity recognition, and keyword extraction — all delivered through an interactive Streamlit web app.

This project supports:

- Screen auto-capture (no image upload needed)
- Snipping-style region selection (like Windows Snipping Tool)
- Handwritten text OCR
- Multilingual OCR
- NLP pipeline (summarization, NER, keyword extraction)
- Interactive Streamlit web application

---

## Features

### OCR Capabilities
- **Printed text OCR** using Tesseract
- **Handwritten OCR** using EasyOCR (deep-learning based)
- **Multilingual OCR support**
  - English, French, Hindi, Spanish, etc.
- Automatic text extraction from:
  - Uploaded images
  - Full-screen capture
  - Selected screen region (snipping)

---

### NLP Capabilities
After OCR extraction, the following NLP tasks are performed:

- Language detection
- Text cleaning and normalization
- Text summarization (offline extractive summarizer)
- Named Entity Recognition (NER)
- Keyword extraction using TF-IDF

---

### User Interface (Streamlit)
- Upload image
- Auto-capture screen
- Draw rectangle to OCR selected area
- Choose OCR engine
- Choose language
- Download extracted text (`.txt`)
- Download structured output (`.json`)

---


#### Create Virtual Environment
.env
venv/

#### Install libraries
```bash
pip install -r requirements.txt



PDF Title and Heading Extractor
This document outlines the solution for the Adobe India Hackathon (Round 1A). The goal is to build a Dockerized, offline tool that accurately extracts the title and hierarchical headings (H1, H2, H3) from PDF files and outputs the results in a structured JSON format.

My Approach
The solution follows a multi-stage pipeline designed for accuracy and efficiency, processing each PDF to extract its structural elements.

PDF Parsing and Candidate Extraction:

The process begins in process_pdfs.py, which scans the /app/input directory for PDF files.

For each PDF, the core logic in pdf_processor/extractor.py is invoked.

Using the PyMuPDF library, the script iterates through the first 50 pages of the document. It extracts every text span along with its detailed properties (font, size, weight, color, and position). Each non-empty text span is considered a potential candidate for being a title or a heading.

Feature Engineering:

For each text candidate, the pdf_processor/features.py module generates a rich set of features. These include:

Font-based features: Font size, bold/italic weight.

Text-based features: All-caps, presence of numbering (e.g., "1.1", "A.").

Layout-based features: Centered alignment, relative position on the page.

Language features: The language of the text is detected using langid.

Title and Heading Identification:

Title Extraction: A specialized heuristic function (extract_title_candidate) analyzes candidates from the first page. It assigns a score based on features common to titles (large font size, bold weight, centered alignment) to identify the most likely document title.

Heading Classification: All other text candidates are passed to a hybrid classification system in pdf_processor/model.py.

A pre-trained scikit-learn classifier predicts the heading level (H1, H2, H3) based on the engineered feature vector.

If the model is not present, the system gracefully falls back to a rule-based engine that uses font size thresholds to determine the heading level.

Output Generation:

The final list of headings is filtered to ensure it conforms to the exact JSON schema required by the challenge ({"level": "H1", "text": "...", "page": 1}).

The pdf_processor/utils.py module ensures all output text is cleaned and normalized.

The final dictionary containing the title and the outline is saved as a JSON file in the /app/output directory.

Models and Libraries Used
This solution relies exclusively on open-source libraries and a lightweight, pre-trained model.

Library

Version

Purpose

PyMuPDF

1.23.7

The core engine for parsing PDF files, extracting text, fonts, and layout information with high performance.

scikit-learn

1.4.2

Used for the machine learning model that classifies text spans into heading levels (H1, H2, H3).

Joblib

1.4.2

Handles the loading of the pre-trained scikit-learn classifier and label encoder from disk.

langid

1.1.6

Detects the language of text spans to fulfill the bonus requirement for multilingual handling.

pycountry

22.3.5

Converts the two-letter language codes from langid into human-readable names.

NumPy

1.26.4

A fundamental dependency for scikit-learn for numerical operations.

How to Build and Run the Solution
This solution is containerized with Docker and can be built and run with the following commands.

1. Build the Docker Image
Navigate to the project's root directory (where the Dockerfile is located) and run the following command. This will build the image and tag it as pdf-processor.

docker build --platform linux/amd64 -t pdf-processor .

2. Run the Container
Before running, ensure you have an input directory containing your PDF files and an empty output directory in your project's root.

For Windows (using PowerShell):
docker run --rm -v "${PWD}/input:/app/input:ro" -v "${PWD}/output:/app/output" --network none pdf-processor

For Linux / macOS:
docker run --rm -v "$(pwd)/input":/app/input:ro -v "$(pwd)/output":/app/output --network none pdf-processor

The script will automatically process all PDFs from your local input folder and save the corresponding .json files into your local output folder.
import os
import json
from pathlib import Path
from pdf_processor.extractor import process_pdf

def run_processing():
    """
    Scans for PDF files in the input directory, processes each file to extract
    structured data, and saves the output as a JSON file.
    """
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process all PDF files found in the input directory
    for pdf_file in input_dir.glob("*.pdf"):
        input_path = str(pdf_file)
        output_path = output_dir / f"{pdf_file.stem}.json"
        
        print(f"Processing: {pdf_file.name}...")
        try:
            # Call the core PDF processing function
            result = process_pdf(input_path)
            
            # Write the structured data to a JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Successfully created: {output_path.name}")
            
        except Exception as e:
            print(f"Failed to process {pdf_file.name}: {e}")

if __name__ == '__main__':
    run_processing()
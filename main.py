
"""
    A barebones script to extract invoice items from a LEGO PDF invoice and convert them into a CSV file.

    It leverages the PyMuPDF library for reading and extracting text from PDF files, and 
    OpenAI's GPT model for processing and interpreting the extracted text to identify and extract invoice items. 
    The extracted items are then formatted into JSON and subsequently converted into
    a CSV file for easier handling and analysis. 

    This script requires the `openai` and `pymupdf` packages to be installed. 
      eg.  pip install openai pymupdf
    
    Also make sure your OpenAI API_KEY is set in os env
        macOs: export OPENAI_API_KEY='your_api_key_here'
        windows/powershell: $env:OPENAI_API_KEY="your_api_key_here"

    It is designed to be used as a command-line tool, where the user provides the path to the PDF file as an argument.
"""

import sys
import csv
import json
import fitz  # PyMuPDF

class LegoInvoiceExtractor:
    def __init__(self, client):
        self.client = client

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from a given PDF file."""
        
        try:
            with fitz.open(pdf_path) as doc:
                return "".join(page.get_text() for page in doc)
        except Exception as e:
            print(f"Failed to open or process the PDF: {e}")
            sys.exit(1)


    def extract_invoice_items(self, pdf_text):
        """Extracts LEGO invoice items using OpenAI's completion API."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "user", "content": pdf_text},
                    {"role": "user", "content": """Extract the 8 fields listed for all invoice items `[{"Article":, "Product":, "Description":, "Quantity":, "Unit Price":, "Discount":, "Net Price":, "Net Amount"}]` as JSON. Do not include additional comments."""}
                ],
                temperature=0,
                max_tokens=8000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            data = json.loads(response.json())
            return json.loads(data['choices'][0]['message']['content'])
        except Exception as e:
            print(f"API call failed: {e}")
            sys.exit(1)



    def json_to_csv(self, data, csv_file='out.csv'):
        """Converts JSON data to a CSV file."""

        headers = ["Article", "Product", "Description", "Quantity", "Unit Price", "Discount", "Net Price", "Net Amount"]

        # Attempt to parse the data from JSON string to Python object if it's a string
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON string: {e}")
                return

        try:
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            print(f"CSV file has been created: {csv_file}")
        except Exception as e:
            print(f"Failed to write CSV: {e}")



def main(pdf_file_name):
    # Assuming `client` is an initialized OpenAI client object
    from openai import OpenAI
    client = OpenAI()
    
    extractor = LegoInvoiceExtractor(client)
    pdf_text = extractor.extract_text_from_pdf(pdf_file_name)
    invoice_items = extractor.extract_invoice_items(pdf_text)
    extractor.json_to_csv(invoice_items, f'{pdf_file_name}.csv')



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need an input PDF")
        print(f"Usage: {sys.argv[0]} /path/to/input.pdf")
        sys.exit(1)
    main(sys.argv[1])

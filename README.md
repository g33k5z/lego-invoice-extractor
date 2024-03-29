# Lego Invoice Extractor

A barebones python script to extract invoice items from a LEGO PDF invoice and convert them into a CSV file.

It leverages the PyMuPDF library for reading and extracting text from PDF files, and 
OpenAI's GPT model for processing and interpreting the extracted text to identify and extract invoice items. 
The extracted items are then formatted into JSON and subsequently converted into
a CSV file for easier handling and analysis. 

#### This script requires the `openai` and `pymupdf` packages to be installed. 
 ```python
pip install openai pymupdf
```

#### Also make sure your OpenAI API_KEY is set in os env
macOS
```shell 
export OPENAI_API_KEY='your_api_key_here'
```
Windows/PowerShell
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

#### Usage
It is designed to be used as a command-line tool, where the user provides the path to the PDF file as an argument.
```console
python main.py LegoInvoice.pdf

// CSV file has been created: LegoInvoice.pdf
```

#### GPT Prompt
We define the GPT prompt for item extraction as the below. This can be modified, extended as needed. 

Just make sure the csv headser match in `json_to_csv()`.
```shell
Extract the 8 fields listed for all invoice items
  `[{"Article":, "Product":, "Description":, "Quantity":, "Unit Price":, "Discount":, "Net Price":, "Net Amount"}]`
as JSON.
Do not include additional comments.
```

#### Example Lego Invoice PDF input
<img width="1147" alt="Screenshot 2024-02-22 at 4 26 43 PM" src="https://github.com/g33k5z/lego-invoice-extractor/assets/6076074/98c98a40-b382-4049-904d-6bea1c03f333">



##### OpenAI Quotas
Depending on your quota, you may need to limit the pdf pages you input to 1 at at a time or lower the token response to help stay under the limits.

```python

def extract_invoice_items(self, pdf_text):
...
 response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k", #change model if needed
                messages=[
                      ...
                ],
                temperature=0,
                max_tokens=8000, #lower max tokens 
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
...
```

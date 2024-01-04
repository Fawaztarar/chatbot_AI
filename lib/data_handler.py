import os
from PyPDF2 import PdfReader
import pdfplumber  # If you're using this elsewhere

# Define the path to your data folder
data_folder = '/Users/fawaztarar/Documents/chatgpt/chatgpt-retrieval/data'

def read_pdf(file_name):
    file_path = os.path.join(data_folder, file_name)
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text



def read_text_file(file_name):
    file_path = os.path.join(data_folder, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Similarly update other functions like read_pdf_combined, read_pdf_with_pdfplumber, etc.

# ... Other functions ...


from PyPDF2 import PdfReader
import os

# ... other parts of your file ...

def read_pdf_combined(file_name):
    file_path = os.path.join(data_folder, file_name)
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:  # Updated to use len(reader.pages)
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                text = read_pdf_with_pdfplumber(file_path)
                break
    return text


def read_pdf_with_pdfplumber(file_name):
    file_path = os.path.join(data_folder, file_name)
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def read_pdf_with_pdfplumber_combined(file_name):
    file_path = os.path.join(data_folder, file_name)
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text



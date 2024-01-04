import pytest
import os
from lib.data_handler import read_pdf, read_text_file, read_pdf_combined, read_pdf_with_pdfplumber, read_pdf_with_pdfplumber_combined



def test_read_pdf():
    result = read_pdf('makers_brochure.pdf')  # Assumes 'test_file.pdf' exists in data_folder
    assert result is not None
    assert 'There are many reasons why Maker' in result

    # Add more assertions based on the expected content of your test PDF

def test_read_text_file():
    result = read_text_file('data.txt')  # Assumes 'test_file.txt' exists in data_folder
    assert result is not None
    assert 'developers can start careers' in result
    # Add more assertions based on the expected content of your test text file

# Write similar tests for other functions like read_pdf_combined, etc.


def test_read_pdf_combined():
    result = read_pdf_combined('makers_brochure.pdf')  # Assumes 'test_file.pdf' exists in data_folder
    assert result is not None
    assert 'There are many reasons why Maker' in result

    # Add more assertions based on the expected content of your test PDF

def test_read_pdf_with_pdfplumber():
    result = read_pdf_with_pdfplumber('makers_brochure.pdf')  # Assumes 'test_file.pdf' exists in data_folder
    assert result is not None
    assert 'There are many reasons why Maker' in result

    # Add more assertions based on the expected content of your test PDF

def test_read_pdf_with_pdfplumber_combined():
    result = read_pdf_with_pdfplumber_combined('makers_brochure.pdf')  # Assumes 'test_file.pdf' exists in data_folder
    assert result is not None
    assert 'There are many reasons why Maker' in result

    # Add more assertions based on the expected content of your test PDF
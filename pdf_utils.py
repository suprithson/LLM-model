import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTFigure
import PyPDF2
import pandas as pd

# Function to crop image
def crop_image(element, page_obj, cropped_pdf_path='cropped_image.pdf'):
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
    page_obj.mediabox.lower_left = (image_left, image_bottom)
    page_obj.mediabox.upper_right = (image_right, image_top)
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(page_obj)
    with open(cropped_pdf_path, 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Function to convert PDF to images and extract text
def convert_to_images_and_extract_text(input_file, output_image='PDF_image.png'):
    images = convert_from_path(input_file)
    image_path = 'temp/' + output_image
    image = images[0]
    image.save(image_path, "PNG")
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

# Function to parse OCR text to DataFrame
def parse_ocr_text_to_df(ocr_text):
    lines = ocr_text.strip().split("\n")
    columns = ['Text']
    data = [{'Text': line} for line in lines if line.strip()]
    df = pd.DataFrame(data, columns=columns)
    return df

# Function to extract text from PDF images
def extract_text_from_pdf_images(pdf_path):
    text_from_images = {}
    pdf_reader = PyPDF2.PdfReader(pdf_path)

    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        for element in page_layout:
            if isinstance(element, LTFigure):
                page_obj = pdf_reader.pages[page_num]
                crop_image(element, page_obj)
                ocr_text = convert_to_images_and_extract_text('cropped_image.pdf')
                df = parse_ocr_text_to_df(ocr_text)
                text_from_images[f'Page_{page_num}'] = df

                # Clean up - remove temporary files
                os.remove('cropped_image.pdf')
                os.remove('temp/PDF_image.png')

    return text_from_images

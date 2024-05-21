from flask import Flask, render_template, request
import os
import sys  # Import sys module here
print("/Users/hey/Desktop/ss/pdf_utils.py")
from pdf_utils import extract_text_from_pdf_images # type: ignore
import os

if not os.path.exists('temp'):
    os.makedirs('temp')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])

def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        print("File uploaded successfully:", file_path)  # Debugging statement
        try:
            extracted_data = extract_text_from_pdf_images(file_path)
            os.remove(file_path)  # Remove the uploaded file
            print("Extraction successful")  # Debugging statement
            return render_template('result.html', extracted_data=extracted_data)
        except Exception as e:
            print("Error during extraction:", e)  # Debugging statement
            os.remove(file_path)  # Remove the uploaded file
            return "Error during extraction"
    return "No file uploaded"


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('temp'):
        os.makedirs('temp')
    app.run(debug=True)

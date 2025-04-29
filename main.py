from flask import Flask, request, jsonify, render_template
import os
import io
from PyPDF2 import PdfReader
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS

# Set your Gemini API Key
genai.configure(api_key="AIzaSyBWhUT8W4Y9YQOKS-Ww8qYcd3R2TYfRbOw")
model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")


@app.route('/')
def index():
    return render_template('pdfupload.html')


@app.route('/pdfupload/', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"detail": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"detail": "No file selected"}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({"detail": "Only PDF files are allowed"}), 400

    try:
        pdf_bytes = file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_text = " ".join([page.extract_text() or "" for page in reader.pages])

        if not extracted_text.strip():
            return jsonify({"detail": "No readable text found in PDF"}), 400

        prompt = f"Summarize the following PDF content:\n\n{extracted_text[:5000]}"
        response = model.generate_content(prompt)
        summary = response.text

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

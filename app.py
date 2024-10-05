from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

# Path to save uploaded images and processed images
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'image' not in request.files:
            return "No file part"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        
        # Save the uploaded image
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)
        
        # Process the image with rembg to remove background
        output_filename = f"bg_removed_{file.filename}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        with open(input_path, 'rb') as input_image_file:
            input_image = input_image_file.read()
        
        # Remove background
        output_image = remove(input_image)

        # Save the image with a transparent background
        with open(output_path, 'wb') as output_image_file:
            output_image_file.write(output_image)
        
        # Render the template with the uploaded and output image paths
        return render_template('index.html', uploaded_image=url_for('static', filename=f'uploads/{file.filename}'),
                               output_image=url_for('static', filename=f'output/{output_filename}'),
                               output_filename=output_filename)
    
    return render_template('index.html')


@app.route('/download/<filename>')
def download_file(filename):
    # Serve the file for download directly, without showing the image
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

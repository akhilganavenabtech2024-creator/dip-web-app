import os
import cv2
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload and processed directories
UPLOAD_FOLDER = os.path.join('static', 'uploads')
PROCESSED_FOLDER = os.path.join('static', 'processed')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html')
            
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html')

        if file:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # Read image using OpenCV
            img = cv2.imread(input_path)
            operation = request.form.get('operation')

            # Process Image
            if operation == 'grayscale':
                processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif operation == 'blur':
                processed_img = cv2.GaussianBlur(img, (15, 15), 0)
            elif operation == 'canny':
                processed_img = cv2.Canny(img, 100, 200)
            else:
                processed_img = img

            processed_filename = f"processed_{filename}"
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
            cv2.imwrite(output_path, processed_img)

            return render_template('index.html', 
                                   original_image=filename, 
                                   processed_image=processed_filename)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
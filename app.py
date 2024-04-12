from flask import Flask, render_template, request
import cv2
import numpy as np
from base64 import b64encode
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform_image():
    file = request.files['image'].read()
    matrix_data = request.form['matrix']
    matrix = np.fromstring(matrix_data, sep=' ').reshape(2, 3)
    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    transformed = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
    _, buffer = cv2.imencode('.jpg', transformed)
    encoded_image = b64encode(buffer).decode('utf-8')
    return f'data:image/jpeg;base64,{encoded_image}'

if __name__ == '__main__':
    app.run(debug=True)

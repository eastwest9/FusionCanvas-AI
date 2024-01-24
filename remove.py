# rembg 패키지에서 remove 클래스 불러오기
from rembg import remove 

# PIL 패키지에서 Image 클래스 불러오기
from PIL import Image

# flask server
import requests
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from flask import request, render_template

spring_server_url="http://127.0.0.1:8080/image/list"

app = Flask(__name__)
@app.route('/spring', methods=['POST'])
def spring():
    try:
        # 이미지 받아오기
        image_bytes = request.data

        # 이미지 처리 로직
        img = Image.open(BytesIO(image_bytes))

        # 배경 제거하기
        out = remove(img)
        out.save("test.png")

        with open('test.png', 'rb') as image_file:
            send_image_to_spring(image_file)
        return jsonify({'message': 'Processed image sent to Spring.'})

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400


def send_image_to_spring(image_file):
    files = {'imageFile': ('image.png', image_file, 'image/png')}

    response = requests.post(spring_server_url, files=files)

    if response.status_code == 200:
        print('Image sent successfully to Spring.')
    else:
        print('Failed to send image to Spring.')

if __name__ == '__main__':
    app.run(debug=True, host= "127.0.0.1", port=5000)


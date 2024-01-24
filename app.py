from flask import Flask, render_template, Response, jsonify, request
from io import BytesIO
from PIL import Image
from rembg import remove
from min_dalle import MinDalle
import torch
import requests
import secrets
import numpy as np

app = Flask(__name__)
spring_server_url = "http://127.0.0.1:8080/"

# Define Data type
dtype = "float32"  # @param ["float32", "float16", "bfloat16"]
model1 = MinDalle(
    dtype=getattr(torch, dtype),
    device='cpu',
    is_mega=True,
    is_reusable=True
)


progressive_outputs = False
seamless = False
grid_size = 1
temperature = 1
supercondition_factor = 16
top_k = 256



@app.route('/generateImage', methods=['POST'])
def generate_image():
    try:
        # 텍스트 받아오기
        text_bytes = request.data

        # 텍스트 변환하기
        text = text_bytes.decode('utf-8')
        generated_image = model1.generate_image(
            text=text,
            seed=-1,
            grid_size=grid_size,
            is_seamless=seamless,
            temperature=temperature,
            top_k=int(top_k),
            supercondition_factor=float(supercondition_factor))

        resized_image = generated_image.resize((512, 512), Image.LANCZOS)
        resized_image.save("generated_image.png")
        with open('generated_image.png', 'rb') as image_file:
            send_image_to_spring(image_file, spring_server_url + 'generatorImage/save')
            return jsonify({'message': 'Processed image sent to Spring.'})

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400

@app.route('/removeImage', methods=['POST'])
def remove_image():
    try:
        # 이미지 받아오기
        image_bytes = request.data

        # 이미지 처리 로직
        img = Image.open(BytesIO(image_bytes))
        resize_image = img.resize((512, 512), Image.LANCZOS)
        # 배경 제거하기
        out = remove(resize_image)

        out.save("test.png")
        background_image_path = "generated_image.png"
        overlay_image_path = "test.png"
        output_image_path = "output.png"
        # 이미지 합성
        overlay_images(background_image_path, overlay_image_path, output_image_path, transparency=0.5)
        with open('output.png', 'rb') as image_file:
            send_image_to_spring(image_file, spring_server_url + 'imageProcess/concat')
        return jsonify({'message': 'Processed image sent to Spring.'})

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400



def generate_unique_name():
    # 원하는 길이의 무작위 문자열 생성
    length = 10  # 원하는 이름 길이로 수정 가능
    unique_name = secrets.token_hex(length)

    # 중복 여부 확인 및 필요한 경우 다시 생성
    # 이 부분에서 중복 이름을 데이터베이스나 다른 저장소를 통해 확인할 수 있습니다.

    return unique_name


def send_image_to_spring(image_file, url):
    files = {'imageFile': ('image.png', image_file, 'image/png')}

    response = requests.post(url, files=files)
    print(response.status_code)
    if response.status_code == 200:
        print('Image sent successfully to Spring.')
    else:
        print('Failed to send image to Spring.')

def overlay_images(background_path, overlay_path, output_path, transparency=0.5):
    # 배경 이미지 열기
    background = Image.open(background_path)

    # 오버레이 이미지 열기
    overlay = Image.open(overlay_path)

    # 배경 이미지 크기에 맞게 오버레이 이미지 크기 조절
    overlay = overlay.resize(background.size, Image.LANCZOS)

    # 배경 이미지의 모드를 RGBA로 변환
    background = background.convert("RGBA")

    # 오버레이 이미지의 배경 제거
    overlay = remove(np.array(overlay))

    # 오버레이 이미지를 배경 이미지에 합성
    blended = Image.alpha_composite(background, Image.fromarray(overlay))

    # 결과 이미지 저장
    blended.save(output_path, format="PNG")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000")


"""
@app.route('/resultImage', methods=['POST'])
def concat_image():
    try:
        background_image_path = "generated_image.png"
        overlay_image_path = "test.png"
        output_image_path = "output.png"
        # 이미지 합성
        overlay_images(background_image_path, overlay_image_path, output_image_path, transparency=0.5)
        with open('output.png', 'rb') as image_file:
            send_image_to_spring(image_file, spring_server_url + 'result/image')
        return jsonify({'message': 'Processed image sent to Spring.'})
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400
        """
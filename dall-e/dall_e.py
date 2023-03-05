import requests
import json
import base64
from PIL import Image
from io import BytesIO
import os
import argparse

# OpenAI DALL-E API 키
# venv 환경에서는 OPEN_AI 환경 변수를 별도로 설정해야 해서 편의를 위해 파일로 저장
# api_key = os.getenv('OPEN_AI')

try:
    with open("api.key", "rt") as f:
        api_key = f.read()
        api_key = api_key.strip().replace("\n", "")
except FileNotFoundError:
    raise FileNotFoundError("""
    api.key 파일이 없습니다.
    """)

# API 호출 URL
url = 'https://api.openai.com/v1/images/generations'

# 헤더 정보
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# 명령어 옵션 파싱
parser = argparse.ArgumentParser(description='Generate images from keywords using OpenAI DALL-E API.')
parser.add_argument('keywords', metavar='keyword', type=str, nargs='+',
                    help='a list of keywords to generate images')

# 입력된 키워드를 문자열로 변환
keywords = ', '.join(parser.parse_args().keywords)

# API 호출 파라미터
data = {
    'model': 'image-alpha-001',
    'prompt': 'An image of ' + keywords,
    'num_images': 1,
    'size': '512x512',
    'response_format': 'url'
}

# API 호출
response = requests.post(url, headers=headers, data=json.dumps(data))

# 응답 데이터 파싱
result = json.loads(response.text)

# 이미지 URL 읽기
img_url = result['data'][0]['url']
print(img_url)

# 이미지 다운로드
img_data = requests.get(img_url).content

# 이미지 출력
# /tmp 디렉토리에 임시 파일로 저장됨
img = Image.open(BytesIO(img_data))
img.show()

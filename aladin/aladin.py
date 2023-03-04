import json

import requests

# 알라딘 OpenAPI 키 발급
# https://www.aladin.co.kr/ttb/wblog_manage.aspx
api_key = 'YOUR_API_KEY'

# 알라딘 Open API 매뉴얼
# https://docs.google.com/document/d/1mX-WxuoGs8Hy-QalhHcvuV17n50uGI2Sg_GHofgiePE/edit
url = f'http://www.aladin.co.kr/ttb/api/ItemList.aspx'

# API 호출
response = requests.get(
    url=url,
    params={
        'ttbkey': api_key,
        'QueryType': 'ItemNewSpecial',
        'MaxResults': 100,
        'start': 1,
        'SearchTarget': 'Book',
        'CategoryId': 8482,
        'Output': 'js',
        'Version': 20131101,
    }
)

# 응답 데이터 파싱
books = json.loads(response.text)
print(books.keys())

for book in books['item']:
    print(book)

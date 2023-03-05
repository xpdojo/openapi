import time

import openai
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# OPENAI API키 설정
with open('api.key', 'rt') as f:
    key = f.read()
    key = key.strip().replace("\n", "")
    openai.api_key = key


# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# 뉴스 페이지 크롤링
def crawl_page(
        url: str,
        class_name: str,
):
    try:
        driver = set_chrome_driver(False)
        driver.get(url)
        # 요소 변경 가능
        article_page = driver.find_element(By.CLASS_NAME, class_name)
        text = article_page.text
        driver.close()
    except NoSuchElementException:
        text = ""
    return text


# ChatGPT 요약
def summarize(text):
    # 프롬프트 (요약해줘!)
    prompt = f'''
    Summarize below in three paragraphs and interpret whether it is a positive or negative sentiment.

    {text}
    '''

    # 요약 요청
    completion = openai.Completion.create(
        engine="text-davinci-003",
        max_tokens=2_048,
        prompt=prompt,
        temperature=0.3,
    )
    return completion.choices[0].text


# 파파고 번역
def papago_translate(text):
    papago = set_chrome_driver(False)
    try:
        papago.get('https://papago.naver.com/?sk=en&tk=ko&hn=1')
        time.sleep(1)
        papago.find_element(By.ID, 'txtSource').send_keys(text)
        papago.find_element(By.ID, 'btnTranslate').click()
        time.sleep(2)
        papago_translated = papago.find_element(By.ID, 'targetEditArea')
        result = papago_translated.text
    except NoSuchElementException:
        result = 'Papago Error'
    finally:
        papago.close()
    return result


# 최종 wrapper
def summarize_article(
        url: str,
        class_name: str,
):
    """
    https://teddylee777.github.io/python/news-article/

    :param url: 요약하려는 영문 article
    :param class_name: article이 포함된 태그의 class name
    """
    origin = crawl_page(url=url, class_name=class_name)
    print('<원문>')
    print(f'{origin}\n')
    summarized = summarize(origin)
    print('<원문 요약>')
    print(f'{summarized}\n')
    korean_translated = papago_translate(summarized)
    print('<한글 요약본>')
    print(f'{korean_translated}\n')


summarize_article(
    url="https://www.investing.com/analysis/traders-send-wheat-prices-spiking-as-allied-tanks-aid-to-roll-into-ukraine-200634894",
    class_name="articlePage",
)

# summarize_article(
#     url="https://www.baeldung.com/java-string-interpolation",
#     class_name="post-content",
# )

# summarize_article(
#     url="https://dev.to/javinpaul/12-best-resources-to-learn-git-online-in-2023-4apo",
#     class_name="crayons-article__main",
# )

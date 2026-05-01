from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

"""
기아차 홈페이지에서 FAQ 크롤링 -> CSV 저장
"""

CSV_FILE = "kia_faq.csv"

# FAQEntry 클래스
class FAQEntry:
    def __init__(self, category, question, answer, site):
        self.category = category
        self.question = question
        self.answer = answer
        self.site = site

    def __repr__(self):
        return f'FAQEntry<category={self.category}, question={self.question}, answer={self.answer}, site={self.site}>'

# FAQ 크롤링 함수
def run():
    # 1. Chrome 실행
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    # 2. FAQ 페이지 접속
    site_name = "기아자동차"

    faq_list = []

    # page_number : category_name 매핑
    page_dict = {
        1: "내차팔기",
        6: "회원",
        7: "방문평가/데이터평가",
        9: "탁송",
        10: "명의이전",        
        12: "내차사기",
        13: "환불/취소",
        14: "결제(할부금융)",
        15: "보증",
        16: "리멤버스",
    }

    # 3. FAQ 페이지 접속
    for page_number, category_name in page_dict.items():
        url = f"https://cpo.kia.com/cs/list/?category={page_number}"
        driver.get(url)
        time.sleep(3)

        questions = driver.find_elements(By.CSS_SELECTOR, "ul.question__lst > li.question__item")
        for q_item in questions:
            question = q_item.find_element(By.CSS_SELECTOR, "div.question__tit").text.strip()

            toggle_btn = q_item.find_element(By.CSS_SELECTOR, "button.question__btn")
            driver.execute_script("arguments[0].scrollIntoView(true);", toggle_btn)
            driver.execute_script("arguments[0].click();", toggle_btn)
            time.sleep(0.3)

            answer = q_item.find_element(By.CSS_SELECTOR, "p.question__detail").text.strip()

            faq_list.append(FAQEntry(category_name, question, answer, site_name))



    # 4. CSV 저장
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Question", "Answer", "Site"])
        
        for faq in faq_list:
            writer.writerow([faq.category, faq.question, faq.answer, site_name])
            print(faq)

        driver.quit()

    print(f"CSV 저장 완료: {CSV_FILE}")

if __name__ == "__main__":
    run()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

CSV_FILE = "kcar_faq.csv"


class FAQEntry:
    def __init__(self, category, question, answer, site):
        self.category = category
        self.question = question
        self.answer = answer
        self.site = site


def wait_until_questions_stable(driver, timeout=15):
    end_time = time.time() + timeout
    last_count = -1
    stable_count = 0
    items = []

    while time.time() < end_time:
        items = driver.find_elements(
            By.XPATH,
            "//*[contains(text(), '?')]"
        )

        items = [
            q for q in items
            if q.is_displayed()
            and q.text.strip()
            and len(q.text.strip()) < 100
        ]

        current_count = len(items)

        if current_count == last_count and current_count > 0:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= 3:
            return items

        last_count = current_count
        time.sleep(0.5)

    return items


def run():
    driver = webdriver.Chrome()
    driver.maximize_window()

    site_name = "케이카"
    url = "https://www.kcar.com/cs/csQstn"

    categories = [
        "내차사기",
        "내차팔기",
        "회원정보관리",
        "금융",
        "렌트",
        "보증서비스",
        "기타"
    ]

    faq_list = []
    seen = set()

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        for category in categories:
            print(f"\n[{category}] 수집 시작")

            category_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//*[normalize-space()='{category}']")
                )
            )

            driver.execute_script("arguments[0].click();", category_btn)

            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), '?')]")
                )
            )

            question_items = wait_until_questions_stable(driver, timeout=15)

            question_items = [
                q for q in question_items
                if q.text.strip() not in categories
            ]

            print("질문 개수:", len(question_items))

            for q in question_items:
                try:
                    question = q.text.strip()

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        q
                    )
                    time.sleep(0.3)

                    driver.execute_script("arguments[0].click();", q)

                    time.sleep(0.8)

                    question_row = q.find_element(
                        By.XPATH,
                        "./ancestor::*[self::li or self::div][1]"
                    )

                    answer_box = question_row.find_element(
                        By.XPATH,
                        "following-sibling::*[1]"
                    )

                    answer = answer_box.text.strip()
                    full_text = parent.text.strip()
                    lines = [
                        line.strip()
                        for line in full_text.splitlines()
                        if line.strip()
                    ]

                    answer_lines = []
                    found_answer = False

                    for line in lines:
                        if line == question:
                            continue

                        if line.startswith("A"):
                            found_answer = True
                            line = line.replace("A", "", 1).strip()

                            if line:
                                answer_lines.append(line)

                            continue

                        if found_answer:
                            if line.startswith("Q"):
                                break
                            answer_lines.append(line)

                    answer = "\n".join(answer_lines).strip()

                    key = (category, question)

                    if question and answer and key not in seen:
                        seen.add(key)
                        faq_list.append(
                            FAQEntry(category, question, answer, site_name)
                        )

                        print("질문:", question)
                        print("답변:", answer[:80])

                except Exception as e:
                    print("질문 처리 실패:", e)

        with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Question", "Answer", "Site"])

            for faq in faq_list:
                writer.writerow([
                    faq.category,
                    faq.question,
                    faq.answer,
                    faq.site
                ])

        print(f"\nCSV 저장 완료: {CSV_FILE}")
        print("총 수집 개수:", len(faq_list))

    finally:
        driver.quit()


if __name__ == "__main__":
    run()
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

CSV_FILE = "kcarcenters.csv"


class CenterEntry:
    def __init__(self, name, address, phone, car_count, site):
        self.name = name
        self.address = address
        self.phone = phone
        self.car_count = car_count
        self.site = site


def run():
    driver = webdriver.Chrome()
    driver.maximize_window()

    site_name = "케이카"
    url = "https://www.kcar.com/db/drCntr"

    center_list = []

    try:
        driver.get(url)
        time.sleep(5)

        # 직영점 카드 목록
        center_items = driver.find_elements(
            By.CSS_SELECTOR,
            "div[class*='center'], div[class*='branch'], li, div"
        )

        seen = set()

        for item in center_items:
            try:
                text = item.text.strip()

                if not text:
                    continue

                if "직영점 차량" not in text:
                    continue

                if "찾아오시는 길" not in text:
                    continue

                lines = [line.strip() for line in text.splitlines() if line.strip()]

                name = ""
                address_lines = []
                phone = ""
                car_count = ""

                for line in lines:
                    if "직영점" in line and "차량" not in line:
                        name = line

                    elif line.startswith("0") and "-" in line:
                        phone = line

                    elif "직영점 차량" in line:
                        car_count = line.replace("직영점 차량", "").strip()

                    elif "찾아오시는 길" in line or "주소문자받기" in line:
                        continue

                    else:
                        if not name:
                            continue
                        if not phone and "직영점 차량" not in line:
                            address_lines.append(line)

                address = " ".join(address_lines).strip()

                key = (name, address, phone, car_count)

                if name and address and phone and key not in seen:
                    seen.add(key)
                    center_list.append(
                        CenterEntry(name, address, phone, car_count, site_name)
                    )

                    print("직영점:", name)
                    print("주소:", address)
                    print("전화:", phone)
                    print("차량:", car_count)
                    print("-" * 40)

            except Exception:
                continue

        with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Address", "Phone", "CarCount", "Site"])

            for center in center_list:
                writer.writerow([
                    center.name,
                    center.address,
                    center.phone,
                    center.car_count,
                    center.site
                ])

        print(f"CSV 저장 완료: {CSV_FILE}")
        print("총 수집 개수:", len(center_list))

    finally:
        driver.quit()


if __name__ == "__main__":
    run()
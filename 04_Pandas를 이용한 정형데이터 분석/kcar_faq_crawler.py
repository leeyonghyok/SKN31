# kcar.com 자주 하는 질문 크롤러
# 대상 페이지: https://www.kcar.com/cs/csQstn
# API 베이스: https://api.kcar.com

import requests
import pandas as pd
import html
import re
import time
from datetime import datetime

BASE_URL = "https://api.kcar.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Referer": "https://www.kcar.com/cs/csQstn",
    "Origin": "https://www.kcar.com",
}


def clean_html(text: str) -> str:
    """HTML 엔티티 디코딩 후 태그 제거"""
    if not text:
        return ""
    decoded = html.unescape(text)
    clean = re.sub(r"<[^>]+>", "", decoded)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def get_categories() -> list[dict]:
    """카테고리 목록 조회 (masterCd=KCA_FAQ_CATE)"""
    url = f"{BASE_URL}/cs/csMenu"
    params = {"masterCd": "KCA_FAQ_CATE"}
    r = requests.get(url, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    categories = data["data"]["menuCd"]
    result = [
        {"code": c["subCd"], "name": c["subCdNm"]}
        for c in categories
        if c.get("useYn") == "Y" and c.get("delYn") == "N"
    ]
    return result


def get_faq_list() -> list[dict]:
    """전체 FAQ 목록 조회"""
    url = f"{BASE_URL}/cs/faqList"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data["data"]["faqList"]


def crawl_kcar_faq() -> pd.DataFrame:
    """카테고리별 질문/답변 크롤링 후 DataFrame 반환"""
    print("=" * 50)
    print("K Car 자주 하는 질문 크롤링 시작")
    print(f"시작 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 1. 카테고리 목록 조회
    print("\n[1/2] 카테고리 목록 조회 중...")
    categories = get_categories()
    cat_map = {c["code"]: c["name"] for c in categories}
    print(f"  카테고리 수: {len(categories)}개")
    for c in categories:
        print(f"    {c['code']} - {c['name']}")

    # 2. FAQ 전체 조회
    print("\n[2/2] FAQ 목록 조회 중...")
    time.sleep(0.5)
    faq_list = get_faq_list()
    print(f"  총 FAQ 수: {len(faq_list)}개")

    # 3. 데이터 정리
    rows = []
    for item in faq_list:
        cat_code = item.get("qstnClsf", "")
        rows.append({
            "카테고리코드": cat_code,
            "카테고리명": cat_map.get(cat_code, "기타"),
            "고유번호": item.get("sq", ""),
            "질문": clean_html(item.get("titl", "")),
            "답변": clean_html(item.get("cnts", "")),
        })

    df = pd.DataFrame(rows)

    # 카테고리 순서대로 정렬
    cat_order = {c["code"]: i for i, c in enumerate(categories)}
    df["_order"] = df["카테고리코드"].map(cat_order).fillna(999)
    df = df.sort_values(["_order"]).drop(columns=["_order"]).reset_index(drop=True)

    # 4. 카테고리별 통계 출력
    print("\n[결과] 카테고리별 FAQ 수:")
    for cat_name, group in df.groupby("카테고리명", sort=False):
        print(f"  {cat_name}: {len(group)}개")

    print(f"\n전체: {len(df)}개")
    return df


def save_results(df: pd.DataFrame):
    """크롤링 결과를 CSV와 Excel로 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"kcar_faq_{timestamp}.csv"
    excel_path = f"kcar_faq_{timestamp}.xlsx"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"\nCSV 저장: {csv_path}")

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        # 전체 시트
        df.to_excel(writer, sheet_name="전체", index=False)
        # 카테고리별 시트
        for cat_name, group in df.groupby("카테고리명", sort=False):
            sheet_name = cat_name[:31]  # Excel 시트명 31자 제한
            group.drop(columns=["카테고리코드"]).to_excel(
                writer, sheet_name=sheet_name, index=False
            )
    print(f"Excel 저장: {excel_path}")

    return csv_path, excel_path


if __name__ == "__main__":
    df = crawl_kcar_faq()

    print("\n" + "=" * 50)
    print("샘플 데이터 (각 카테고리 첫 번째 항목):")
    print("=" * 50)
    for cat_name, group in df.groupby("카테고리명", sort=False):
        first = group.iloc[0]
        print(f"\n[{cat_name}]")
        print(f"  Q: {first['질문']}")
        ans = first['답변']
        print(f"  A: {ans[:100]}{'...' if len(ans) > 100 else ''}")

    save_results(df)

import requests
from bs4 import BeautifulSoup

url = "https://news.daum.net"
# 뉴스제목: <a>의 content, 링크주소: <a>의 href 속성값
a_selector = r"#\35 8d84141-b8dd-413c-9500-447b39ec29b9 > ul > li > a"

# user-agent: 1.개발자도구>콘솔: navigator.userAgent, 2. google검색: my user agent 로 검색
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

def get_daum_news_list():
    """
    다음 뉴스 기사 목록을 크롤링하는 함수.
    news.daum.net의 기사 목록에서 "제목", "링크" 들을 수집.

    aguments
    return
        DataFrame: 조회결과들을 담은 DataFrame(표)
    raise
        Exception: 처리 실패시 발생
    """
    # 1. 요청
    res = requests.get(url, headers={"user-agent":user_agent})
    # 한글 처리
    res.encoding = "utf-8"
    
    # 2. 응답 페이지에서 필요한 정보 추출
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "lxml")
        a_list = soup.select(a_selector)
        result_list = []
        for a_tag in a_list:
            # title = a_tag.get_text()
            strong_tag = a_tag.select_one("strong.tit_txt") # Tag.select() -> Tag 하위 태그에서 찾는다.
            title = strong_tag.text
            link = a_tag.get("href")
            result_list.append([title.strip(), link])
        
        return result_list
    else:
        raise Exception(f"요청 실패. 응답코드: {res.status_code}")      


if __name__ == "__main__":
    result = get_daum_news_list()
    
    # 저장할 디렉토리를 생성
    import os
    from datetime import datetime
    import pandas as pd
    save_dir = "daum_news_list"
    os.makedirs(save_dir, exist_ok=True)
    
    # 저장할 파일명 - 특정 기간마다 크롤링 수행할 경우 실행 날짜/시간을 이용해서 만들어 준다.
    d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"{save_dir}/{d}.csv"

    # DataFrame 생성
    result_df = pd.DataFrame(result, columns=['제목', "링크주소"])
    
    # csv 파일로 저장.
    result_df.to_csv(file_path, index=False)
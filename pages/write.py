import streamlit as st
import pandas as pd
from datetime import datetime
import csv

# 사이드 바 숨기기
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# 파라미터 읽어오기
current_type = st.query_params.to_dict()["type"]
current_search_class = st.query_params.to_dict()["class"]
current_search_text = st.query_params.to_dict()["text"]
current_page = st.query_params.to_dict()["page"]
st.session_state.type = current_type
st.session_state.search_class = current_search_class
st.session_state.search_text = current_search_text
st.session_state.page = int(current_page)

def load_data():
    df = pd.read_csv("./data/books_metadata.csv")
    return df

def insert_list(df, url, img_url, title, authors, publisher, published_at, summary, translation):
    # 새 행 데이터 정의
    # if len(df) == 0:
    #     values = {"id": 1, "url": url, "img_url": img_url, "title": title, "authors": authors, "publisher": publisher, "published_at": published_at, "review_cnt": 0.0, "rating": 0.0, "summary": summary, "translation": translation}
    # else:
    #     values = {"id": df.iloc[len(df) - 1][0] + 1, "url": url, "img_url": img_url, "title": title, "authors": authors, "publisher": publisher, "published_at": published_at, "review_cnt": 0.0, "rating": 0.0, "summary": summary, "translation": translation}

    if len(df) == 0:
        values = (1, url, img_url, title, authors, publisher, published_at, 0.0, 0.0, summary, translation)
    else:
        values = (df.iloc[len(df) - 1][0] + 1, url, img_url, title, authors, publisher, published_at, 0.0, 0.0, summary, translation)

    # 기존 CSV 파일에 행 추가
    with open("./data/books_metadata.csv", mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(values)

    return len(df) + 1

# 변수 설정
df = load_data()
st.session_state.all_count = len(df)
main_url = "https://rgt-books-store-1004.streamlit.app"


# 오늘의 날짜 가져오기
today = datetime.today()


st.title("책 추가하기")
st.markdown(f"{today.strftime('%Y.%m.%d')}, made by 이혜진")


with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        url = st.text_input("구매 링크")
    with col2:
        img_url = st.text_input("이미지 링크")

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("책 제목")
    with col2:
        authors = st.text_input("저자")

    col1, col2 = st.columns(2)
    with col1:
        publisher = st.text_input("발행처")
    with col2:
        published_at = st.text_input("발행일")


    summary = st.text_area("한글요약")
    translation = st.text_area("영어요약")


    submitted = st.form_submit_button("Submit")


if submitted:

    if not url:
        st.error("구매링크를 입력해주세요!")
    elif not img_url:
        st.error("이미지링크를 입력해주세요!")
    elif not title:
        st.error("제목을 입력해주세요!")
    elif not authors:
        st.error("저자를 입력해주세요!")
    elif not publisher:
        st.error("발행처를 입력해주세요!")
    elif not published_at:
        st.error("발행일을 입력해주세요!")
    elif not summary:
        st.error("한글요약을 입력해주세요!")
    elif not translation:
        st.error("영어요약을 입력해주세요!")
    else:
        st.session_state.all_count = insert_list(df, url, img_url, title, authors, publisher, published_at, summary, translation)
        st.write("성공!!!")


print(st.session_state.all_count)
st.markdown(f'''
    <a href="{main_url}/?type=all&class=&text=&page={((st.session_state.all_count-1) // 10)+1}" target="_parent">
        목록
    </a>
''', unsafe_allow_html=True)
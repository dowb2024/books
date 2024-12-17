import streamlit as st
import pandas as pd
from datetime import datetime
import time
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
current_id = st.query_params.to_dict()["id"]
st.session_state.type = current_type
st.session_state.search_class = current_search_class
st.session_state.search_text = current_search_text
st.session_state.page = int(current_page)
st.session_state.id = int(current_id)

def load_data():
    df = pd.read_csv("./data/books_metadata.csv")
    return df

def load_inout_data():
    df_inout = pd.read_csv("./data/books_inout_history.csv")
    return df_inout

def select_list(df, id):
    data = []
    for i in range(len(df)):
        if df.iloc[i][0] == id:
            data.append(df.iloc[i])

    result = pd.DataFrame(data, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])
    return result


def select_inout(df_inout, id):
    data = []
    for i in range(len(df_inout)):
        if df_inout.iloc[i][0] == id:
            data.append(df.iloc[i])

    result = pd.DataFrame(data, columns=["id", "register_date", "modify_date", "in_count", "out_count", "description"])
    return result

def sum_in_count(df_inout, id):
    data = 0
    for i in range(len(df_inout)):
        if df_inout.iloc[i][0] == id:
            data += df_inout.iloc[i][3]
    return data

def sum_out_count(df_inout, id):
    data = 0
    for i in range(len(df_inout)):
        if df_inout.iloc[i][0] == id:
            data += df_inout.iloc[i][4]
    return data

def insert_inout(register_date, modify_date, in_count, out_count, description):

    values = (st.session_state.id, register_date, modify_date, in_count, out_count, description)

    # 기존 CSV 파일에 행 추가
    with open("./data/books_inout_history.csv", mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(values)


# 변수 설정
df = load_data()
df_list = select_list(df, st.session_state.id)
df_inout = load_inout_data()
url = "https://rgt-books-store-1004.streamlit.app"


# 오늘의 날짜 가져오기
today = datetime.today()

st.title("책 재고 관리")
st.markdown(f"{today.strftime('%Y.%m.%d')}, made by 이혜진")

st.write("")
col1, col2 = st.columns(2)
with col1:
    st.markdown("아이디")
with col2:
    st.markdown(st.session_state.id)

col1, col2 = st.columns(2)
with col1:
    st.markdown("제목")
with col2:
    st.markdown(df_list.iloc[0][3])

col1, col2 = st.columns(2)
with col1:
    st.markdown("현재 수량")
with col2:
    st.session_state.total_counter = sum_in_count(df_inout, st.session_state.id)-sum_out_count(df_inout, st.session_state.id)
    st.markdown(st.session_state.total_counter)

with st.form("form"):

    col1, col2 = st.columns(2)
    with col1:
        in_count = st.text_input("입고 개수")
    with col2:
        out_count = st.text_input("출고 개수")

    description = st.text_area("설명")
    
    submitted = st.form_submit_button("Submit")


if submitted:

    if not in_count:
        st.error("입고 개수를 입력해주세요!")
    elif not out_count:
        st.error("출고 개수를 입력해주세요!")
    elif st.session_state.total_counter + int(in_count) < int(out_count):
        st.error("현재수량이 출고 개수보다 작습니다. 출고 개수를 정확히 입력해주세요!")
    elif not description:
        st.error("설명을 입력해주세요!")
    else:

        # 오늘의 날짜/시간 가져오기
        now = datetime.now()

        if len(df_inout) == 0:
            register_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))
            modify_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))
        else:
            register_date = df_inout.iloc[0][1]
            modify_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))

        insert_inout(register_date, modify_date, in_count, out_count, description)
        st.session_state.total_counter = sum_in_count(df_inout, st.session_state.id)-sum_out_count(df_inout, st.session_state.id)
        st.write("성공!!!")
        time.sleep(3)  # 3초 대기
        st.rerun()


st.markdown(f'''
    <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_parent">
        목록
    </a>
''', unsafe_allow_html=True)
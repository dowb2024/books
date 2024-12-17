import streamlit as st
import pandas as pd
import pymysql
from datetime import datetime
import time

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

def get_connection():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password=st.secrets["SQL_PASSWORD"],
        database="mystore",
    )
    return conn

def select_list(conn):
    read_sql = f"SELECT * FROM books WHERE id={st.session_state.id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])
    return df

def select_inout(conn):
    read_sql = f"SELECT * FROM books_inout_history WHERE id={st.session_state.id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["id", "register_date", "modify_date", "in_count", "out_count", "description"])
    return df

def sum_in_count(conn):
    read_sql = f"SELECT sum(in_count) FROM books_inout_history WHERE id={st.session_state.id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        result = cursor.fetchone()  # 튜플로 한 행을 반환

        if result and result[0] is not None:  # 값이 있을 경우에만 처리
            data = int(result[0])  # 첫 번째 값만 정수로 변환
        else:
            data = 0  # 값이 없거나 NULL일 경우 0으로 설정

    return data

def sum_out_count(conn):
    read_sql = f"SELECT sum(out_count) FROM books_inout_history WHERE id={st.session_state.id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        result = cursor.fetchone()  # 튜플로 한 행을 반환

        if result and result[0] is not None:  # 값이 있을 경우에만 처리
            data = int(result[0])  # 첫 번째 값만 정수로 변환
        else:
            data = 0  # 값이 없거나 NULL일 경우 0으로 설정

    return data

def insert_inout(conn, register_date, modify_date, in_count, out_count, description):

    write_sql = """
        INSERT IGNORE INTO books_inout_history(
            id,
            register_date,
            modify_date,
            in_count,
            out_count,
            description
        )
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    values = (st.session_state.id, register_date, modify_date, in_count, out_count, description)

    with conn.cursor() as cursor:
        cursor.execute(write_sql, values)
        conn.commit()


# 데이터 베이스 연결
conn = get_connection()

# 변수 설정
df_list = select_list(conn)
url = "http://localhost:8501"


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
    st.session_state.total_counter = sum_in_count(conn)-sum_out_count(conn)
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
        df_inout = select_inout(conn)

        # 오늘의 날짜/시간 가져오기
        now = datetime.now()

        if len(df_inout) == 0:
            register_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))
            modify_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))
        else:
            register_date = df_inout.iloc[0][1]
            modify_date = str(now.strftime('%Y.%m.%d %H:%M:%S'))

        insert_inout(conn, register_date, modify_date, in_count, out_count, description)
        st.session_state.total_counter = sum_in_count(conn) - sum_out_count(conn)
        st.write("성공!!!")
        time.sleep(3)  # 3초 대기
        st.rerun()


st.markdown(f'''
    <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_parent">
        목록
    </a>
''', unsafe_allow_html=True)
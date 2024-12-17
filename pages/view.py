import streamlit as st
import pandas as pd
import pymysql

# 사용자 정의 CSS 삽입
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# @st.cache_data
# def load_data():
#     df = pd.read_csv("./data/books_metadata.csv")
#     return df
#
# # 데이터 샘플
# df = load_data()

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

# 변수 설정
conn = get_connection()
df = select_list(conn)
url = "http://localhost:8501"


col1, col2 = st.columns(2)
with col1:
    st.markdown("책사진")
with col2:
    st.image(df.iloc[0][2])

col1, col2 = st.columns(2)
with col1:
    st.markdown("아이디")
with col2:
    st.markdown(df.iloc[0][0])

col1, col2 = st.columns(2)
with col1:
    st.markdown("제목")
with col2:
    st.markdown(df.iloc[0][3])

col1, col2 = st.columns(2)
with col1:
    st.markdown("저자")
with col2:
    st.markdown(df.iloc[0][4])

col1, col2 = st.columns(2)
with col1:
    st.markdown("발행처")
with col2:
    st.markdown(df.iloc[0][5])

col1, col2 = st.columns(2)
with col1:
    st.markdown("발행일")
with col2:
    st.markdown(df.iloc[0][6])

col1, col2 = st.columns(2)
with col1:
    st.markdown("리뷰점수")
with col2:
    st.markdown(df.iloc[0][7])

col1, col2 = st.columns(2)
with col1:
    st.markdown("랭킹")
with col2:
    st.markdown(df.iloc[0][8])

col1, col2 = st.columns(2)
with col1:
    st.markdown("한글 요약")
with col2:
    st.markdown(df.iloc[0][9])

col1, col2 = st.columns(2)
with col1:
    st.markdown("영문 요약")
with col2:
    st.markdown(df.iloc[0][10])

st.markdown(f'''
    <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_parent">
        목록
    </a>
''', unsafe_allow_html=True)

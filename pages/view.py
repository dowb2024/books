import streamlit as st
import pandas as pd

# 사용자 정의 CSS 삽입
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

@st.cache_data
def load_data():
    df = pd.read_csv("./data/books_metadata.csv")
    return df

def select_list(df, id):
    data = []
    for i in range(len(df)):
        if df.iloc[i][0] == id:
            data.append(df.iloc[i])
    result = pd.DataFrame(data, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])
    return result

# 변수 설정
df_load = load_data()
df = select_list(df_load, st.session_state.id)
url = "https://rgt-books-store-1004.streamlit.app"


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
    <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_self">
        목록
    </a>
''', unsafe_allow_html=True)

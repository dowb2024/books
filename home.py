import streamlit as st
import pandas as pd
from datetime import date
import pymysql
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

def get_connection():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password=st.secrets["SQL_PASSWORD"],
        database="mystore",
    )
    return conn

def _execute_insert(conn, sql, buffer):
    with conn.cursor() as cursor:
        result = cursor.executemany(sql, buffer)
        conn.commit()
        print("write:", result)


def bulk_write(conn, sql, data_file_path, batchsize=100):
    with open(data_file_path, encoding='utf-8') as fr:
        reader = csv.reader(fr)
        buffer = []
        for i, row in enumerate(reader):
            if i == 0:
                continue
            row = [x if x else None for x in row]
            buffer.append(row)
            if len(buffer) == batchsize:
                _execute_insert(conn, sql, buffer)
                buffer = []
        if buffer:
            _execute_insert(conn, sql, buffer)


# 데이터 베이스 연결
conn = get_connection()

# write_books_sql = """
# INSERT IGNORE INTO
#     books(
#         id,
#         url,
#         img_url,
#         title,
#         authors,
#         publisher,
#         published_at,
#         review_cnt,
#         rating,
#         summary,
#         translation
#     )
# VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
# """
# bulk_write(conn, write_books_sql, "./data/books_metadata.csv", batchsize=100)

def select_list(conn):
    read_sql = "SELECT * FROM books"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])
    return df

def delete_list(conn, id):
    delete_sql = f"DELETE FROM books WHERE id = {id}"
    with conn.cursor() as cursor:
        cursor.execute(delete_sql)
        conn.commit()

def select_inout(conn, id):
    read_sql = f"SELECT * FROM books_inout_history WHERE id={id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["id", "register_date", "modify_date", "in_count", "out_count", "description"])
    return df

def sum_in_count(conn, id):
    read_sql = f"SELECT sum(in_count) FROM books_inout_history WHERE id={id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        result = cursor.fetchone()  # 튜플로 한 행을 반환

        if result and result[0] is not None:  # 값이 있을 경우에만 처리
            data = int(result[0])  # 첫 번째 값만 정수로 변환
        else:
            data = 0  # 값이 없거나 NULL일 경우 0으로 설정

    return data

def sum_out_count(conn, id):
    read_sql = f"SELECT sum(out_count) FROM books_inout_history WHERE id={id}"
    with conn.cursor() as cursor:
        cursor.execute(read_sql)
        result = cursor.fetchone()  # 튜플로 한 행을 반환

        if result and result[0] is not None:  # 값이 있을 경우에만 처리
            data = int(result[0])  # 첫 번째 값만 정수로 변환
        else:
            data = 0  # 값이 없거나 NULL일 경우 0으로 설정

    return data

# @st.cache_data
# def load_data():
#     df = pd.read_csv("./data/books_metadata1.csv")
#     return df
#
# # 데이터 샘플
# df = load_data()

# 변수 설정
items_per_page = 10
url = "http://localhost:8501"


# 현재 페이지 상태 관리
if "type" not in st.session_state and "page" not in st.session_state:
    st.session_state.type = "all"
    st.session_state.search_class = ""
    st.session_state.search_text = ""
    st.session_state.page = 1
    # st.query_params.from_dict({"type": "all", "class": "", "text": "", "page": "1"})

# 파라미터 읽어오기
current_type = st.query_params.to_dict()["type"]
current_search_class = st.query_params.to_dict()["class"]
current_search_text = st.query_params.to_dict()["text"]
current_page = st.query_params.to_dict()["page"]
st.session_state.type = current_type
st.session_state.search_class = current_search_class
st.session_state.search_text = current_search_text
st.session_state.page = int(current_page)


def view_list(conn, df, items_per_page):

    # 총 페이지 수 계산
    total_pages = len(df) // items_per_page + (1 if len(df) % items_per_page != 0 else 0)

    # 현재 페이지 데이터 계산
    start_idx = (st.session_state.page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_data = df[start_idx:end_idx]

    # 데이터 출력
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown("번호")
    with col2:
        st.markdown("아이디")
    with col3:
        st.markdown("제목")
    with col4:
        st.markdown("저자")
    with col5:
        st.markdown("현재수량")
    with col6:
        st.markdown("삭제")

    for i in range(len(current_data)):
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown(((st.session_state.page - 1) * 10) + (i + 1))
        with col2:
            st.markdown(current_data.iloc[i][0])
        with col3:
            st.markdown(f'''
                <a href="{url}/view?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_parent">
                    {current_data.iloc[i][3]}
                </a>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(current_data.iloc[i][4])
        with col5:
            if len(select_inout(conn, current_data.iloc[i][0])) != 0:
                st.markdown(f'''
                    <a href="{url}/inout?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_parent">
                        {sum_in_count(conn, current_data.iloc[i][0]) - sum_out_count(conn, current_data.iloc[i][0])}
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                     <a href="{url}/inout?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_parent">
                        0
                     </a>
               ''', unsafe_allow_html=True)
        with col6:
            if st.button("삭제", key=f"{current_data.iloc[i][0]}"):
                delete_list(conn, current_data.iloc[i][0])

    # 페이지 번호 표시 (링크 형태로)
    st.markdown("")
    if st.session_state.page % 10 != 0:
        start = ((st.session_state.page // 10) * 10) + 1
    else:
        start = (((st.session_state.page // 10) - 1) * 10) + 1
    if st.session_state.page % 10 != 0 and ((st.session_state.page // 10) + 1) * 10 <= total_pages:
        end = (((st.session_state.page // 10) + 1) * 10) + 1
    elif st.session_state.page % 10 == 0:
        end = st.session_state.page + 1
    else:
        end = total_pages + 1

    page_links = []
    for i in range(start, end):
        if i == st.session_state.page:
            # 현재 페이지는 볼드 처리
            page_links.append(f"{i}")
        else:
            # 다른 페이지는 클릭 가능한 링크로 표시
            page_links.append(f'''
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={i}" target="_parent">
                    {i}
                </a>
            ''')

    cols = st.columns(12)
    with cols[0]:
        if st.session_state.page > 10:
            st.markdown(f'''
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={((st.session_state.page-1)//10)*10}" target="_parent">
                            <<
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.markdown("")

    for j in range(len(page_links)):
        with cols[j+1]:
            st.markdown(f"|{page_links[j]}", unsafe_allow_html=True)

    if len(page_links) != 10:
        for k in range(len(page_links), 10):
            with cols[k+1]:
                st.markdown("")

    with cols[11]:
        if (((st.session_state.page-1)//10)+1) * 10 <= total_pages:
            st.markdown(f'''
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={(((st.session_state.page-1)//10)*10)+11}" target="_parent">
                            >>
                </a>
            ''', unsafe_allow_html=True)
        else:
            st.markdown("")

# 검색 함수
def search_books(books):

    result = []
    if st.session_state.search_class == "제목":
        for i in range(len(books)):
            title_match = st.session_state.search_text.lower() in books.iloc[i][3].lower() if st.session_state.search_text else True
            if title_match:
                result.append(books.iloc[i])

    else:
        for i in range(len(books)):
            author_match = st.session_state.search_text.lower() in books.iloc[i][4].lower() if st.session_state.search_text else True
            if author_match:
                result.append(books.iloc[i])

    df_result = pd.DataFrame(result, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])

    return df_result



# 오늘의 날짜 가져오기
today = date.today()

# 화면에 오늘 날짜 표시
st.title("ADMIN OF RGT BOOKS STORE")
st.markdown(f"{today.strftime('%Y.%m.%d')}, made by 이헤진")

# 등록 링크
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'''
            <a href="{url}/?type=all&class=&text=&page=1" target="_parent">
                [홈]
            </a>
        ''', unsafe_allow_html=True)
    st.write("")
with col2:
    st.markdown(f'''
            <a href="{url}/write?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_parent">
                [등록]
            </a>
        ''', unsafe_allow_html=True)
    st.write("")

# 검색 입력창
with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        search_class = st.selectbox("구분", ["제목", "저자"])
    with col2:
        search_text = st.text_input("검색어")
    submitted = st.form_submit_button("Submit")

if submitted:

    if not search_class:
        st.error("구분을 선택해주세요!")
    elif not search_text:
        st.error("검색어를 입력해주세요!")
    else:
        st.session_state.type = "search"
        st.session_state.search_class = search_class
        st.session_state.search_text = search_text
        st.session_state.page = 1
        df = select_list(conn)
        result = search_books(df)
        view_list(conn, result, items_per_page)

elif st.session_state.type == "search":
    df = select_list(conn)
    result = search_books(df)
    view_list(conn, result, items_per_page)

else:
    df = select_list(conn)
    view_list(conn, df, items_per_page)




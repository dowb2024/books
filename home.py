import streamlit as st
import pandas as pd
from datetime import date
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


def load_data():
    df = pd.read_csv("./data/books_metadata.csv")
    return df

def load_inout_data():
    df_inout = pd.read_csv("./data/books_inout_history.csv")
    return df_inout

def select_inout(df_inout, id):
    data = []
    for i in range(len(df_inout)):
        if df_inout.iloc[i][0] == id:
            data.append(df_inout.iloc[i])
    df = pd.DataFrame(data, columns=["id", "register_date", "modify_date", "in_count", "out_count", "description"])
    return df


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

def delete_list(df, id):
    data = []
    for i in range(len(df)):
        if df.iloc[i][0] != id:
            data.append(df.iloc[i])
    result = pd.DataFrame(data, columns=["id", "url", "img_url", "title", "authors", "publisher", "published_at", "review_cnt", "rating", "summary", "translation"])
    result.to_csv('./data/books_metadata.csv', index=False)

def view_list(df, df_inout, items_per_page):

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
                <a href="{url}/view?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_blank">
                    {current_data.iloc[i][3]}
                </a>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(current_data.iloc[i][4])
        with col5:
            if len(select_inout(df_inout, current_data.iloc[i][0])) != 0:
                st.markdown(f'''
                    <a href="{url}/inout?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_blank">
                        {sum_in_count(df_inout, current_data.iloc[i][0]) - sum_out_count(df_inout, current_data.iloc[i][0])}
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                     <a href="{url}/inout?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}&id={current_data.iloc[i][0]}" target="_blank">
                        0
                     </a>
               ''', unsafe_allow_html=True)
        with col6:
            if st.button("삭제", key=f"{current_data.iloc[i][0]}"):
                delete_list(df, current_data.iloc[i][0])
                time.sleep(3)  # 3초 대기
                st.rerun()

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
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={i}" target="_blank">
                    {i}
                </a>
            ''')

    cols = st.columns(12)
    with cols[0]:
        if st.session_state.page > 10:
            st.markdown(f'''
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={((st.session_state.page-1)//10)*10}" target="_blank">
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
                <a href="{url}/?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={(((st.session_state.page-1)//10)*10)+11}" target="_blank>
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

# 변수 설정
items_per_page = 10
url = "https://rgt-books-store-1004.streamlit.app"

# 화면에 오늘 날짜 표시
st.title("ADMIN OF RGT BOOKS STORE")
st.markdown(f"{today.strftime('%Y.%m.%d')}, made by 이혜진")

# 등록 링크
st.write("")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'''
        <a href="{url}/?type=all&class=&text=&page=1" target="_self"> 
            [홈]
        </a>
    ''', unsafe_allow_html=True)
    st.write("")
with col2:
    st.markdown(f'''
        <a href="{url}/write?type={st.session_state.type}&class={st.session_state.search_class}&text={st.session_state.search_text}&page={st.session_state.page}" target="_blank">
            [등록]
        </a>
    ''', unsafe_allow_html=True)
    st.write("")
with col3:
    st.markdown("")
with col4:
    st.markdown("")

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

        # 데이터 샘플
        df = load_data()
        df_inout = load_inout_data()
        if len(df) > 0:
            result = search_books(df)
            if len(result) > 0:
                view_list(result, df_inout, items_per_page)
            else:
                st.markdown("검색결과가 없습니다!")


elif st.session_state.type == "search":
    # 데이터 샘플
    df = load_data()
    df_inout = load_inout_data()
    if len(df) > 0:
        result = search_books(df)
        if len(result) > 0:
            view_list(result, df_inout, items_per_page)
        else:
            st.markdown("검색결과가 없습니다!")
else:
    # 데이터 샘플
    df = load_data()
    df_inout = load_inout_data()
    if len(df) > 0:
        view_list(df, df_inout, items_per_page)




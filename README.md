# RGT books'store 관리자 페이지 구현

<문제>
당신은 온라인 서점을 위한 웸 애플리케이션을 개발하고 있습니다. 이 애플리케이션은  상점 주인이 책을 검색하고, 상세정보를 보고 편집하며, 각 책의 판매 수량을 확인 할 수 있어야 합니다.

1. 프론트엔드(Next.js 혹은 개발자가 편한 시스템으로 개발)
1) 책 목록 페이지 구현
- 페이지네이션 적용 (한 페이지 당 10개 항목)
- 제목과 저자로 필터링할 수 있는 검색 기능 구현
2) 책 상세 정보 페이지/뷰 구현
3) 책 추가/제거 및 수량 조절 기능

2. 백엔드 (기술 선택 자유)
1) 데이터베이스와 통신하는 기본적인 RESTful API 설계 및 구현
- 책 목록 조회(GET /api/books)
- 책 상세 정보 조회(GET  /api/books/:id)
- 책 추가(POST /api/books)
- 책 정보 수정(PUT /api/books/:id)
- 책 삭제(DELETE /api/books /:id)

2) 해당 부분 구현에 있어 이슈가 있을 시 목업 데이터를 만들어 서 사용 가능함.

<도구>
1) 언어 : Python, streamlit
2) DB : MariaDB
3) 배포 : streamlit, gitHub
4) 도구 : PyCharm, MySQL Workbench 8.0 CE

<구현>
1. Python(streamlit) + MariaDB
링크 : http://localhost:8501/?type=all&class=&text=&page=1

2. Python(streamlit) + CSV
외부 아이피의 부재로 CSV파일로 대체
링크 : https://rgt-books-store-1004.streamlit.app/?type=all&class=&text=&page=1

* 반드시 ‘type=all&class=&text=&page=1’파라미터를 입력

<참고>
web front-end 개발자 면접전 과제_이혜진.pdf




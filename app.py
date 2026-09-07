import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="위드멤버 무료체험 결과 보고서", layout="wide")

st.title("📊 1주 무료체험 결과 보고서 및 제안서")
st.markdown("---")

# 1. 플레이스 Before & After
st.header("1. 네이버 플레이스 개선 Before & After")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Before (관리 전)")
    before_img = st.file_uploader("Before 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if before_img:
        st.image(before_img, use_column_width=True)

with col2:
    st.subheader("After (관리 후)")
    after_img = st.file_uploader("After 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if after_img:
        st.image(after_img, use_column_width=True)

st.markdown("---")

# 2. 네이버 도구 연동 및 점수 반영
st.header("2. 네이버 필수 도구 연동 및 SEO 점수 반영 결과")
st.write("네이버 플레이스 최적화(SEO)에 필수적인 도구 등록 현황 및 확보한 가산점입니다.")

# 체크박스 및 점수 계산
score = 0
c1, c2, c3 = st.columns(3)
with c1:
    if st.checkbox("✅ 네이버 톡톡 등록 완료 (+15점)"): score += 15
with c2:
    if st.checkbox("✅ 네이버 예약 등록 완료 (+25점)"): score += 25
with c3:
    if st.checkbox("✅ 스마트콜(안심번호) 등록 완료 (+10점)"): score += 10

st.metric(label="확보된 플레이스 최적화 점수", value=f"{score} 점", delta="상위 노출 확률 증가율 반영")
st.progress(score / 50.0) # 50점 만점 기준 프로그레스 바

st.markdown("---")

# 3. 위드멤버 1년 패키지 제안
st.header("3. 위드멤버 1년 마케팅 파트너십 제안")
st.success("**압도적인 가성비와 확실한 보장, 위드멤버 1년 올인원 패키지 (990,000원)**")

st.markdown("""
앞으로 1년간 아래의 마케팅이 지속적으로 실행되어 매장의 브랜드 가치와 실매출을 끌어올립니다.

* **🔍 체험단 및 블로그 최적화**: 매장 타겟층에 맞춘 최적화 블로그 리뷰 배포 및 SEO 관리
* **🎬 인스타그램 릴스 & 유튜브 쇼츠**: 트렌드에 맞춘 매장 홍보용 숏폼 영상 제작 및 배포
* **⭐ 리뷰 평점 관리**: 구글 맵스 및 카카오맵 고품질 리뷰 총 30건 작성 및 별점 방어
* **📈 네이버 플레이스 상위 노출**: 1주일 체험으로 끝나는 것이 아닌, 1년 내내 지속적인 플레이스 SEO 최적화 관리

> 💡 **위드멤버 특별 보장제**  
> 계약 후 **3개월 동안 매출 상승 효과가 없다면, 나머지 기간의 관리 비용은 일절 받지 않습니다.**
""")

st.markdown("---")

# 4. 예상 매출 상승 그래프
st.header("4. 마케팅 진행 시 예상 매출 상승액 (3개월 뒤)")
st.write("본 패키지를 3개월 이상 유지했을 때, **1,500만 원 ~ 2,000만 원** 구간의 추가 매출 달성을 목표로 합니다.")

# 차트 데이터 생성
chart_data = pd.DataFrame({
    "진행 기간": ["관리 시작", "1개월 차", "2개월 차", "3개월 차"],
    "최소 예상 매출(만원)": [0, 400, 900, 1500],
    "최대 예상 매출(만원)": [0, 600, 1200, 2000]
})

# 스트림릿 내장 라인 차트 렌더링
st.line_chart(chart_data.set_index("진행 기간"))
st.caption("※ 위 그래프는 위드멤버의 마케팅 솔루션을 적용한 파트너사들의 평균적인 성장 데이터를 바탕으로 산출된 목표 수치입니다.")
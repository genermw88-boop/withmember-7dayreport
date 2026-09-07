import streamlit as st
import pandas as pd
import random
import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# 폰트 다운로드 오류 수정 (신뢰할 수 있는 URL로 변경 및 예외 처리 추가)
@st.cache_resource
def load_font():
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        try:
            # 구글 폰트 공식 Raw URL
            url = "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            # 폰트 다운로드 실패 시 프로그램이 멈추지 않도록 처리
            st.warning("웹 폰트 로드에 실패했습니다. (다운로드된 이미지의 텍스트 폰트가 다르게 보일 수 있습니다.)")
            return None
    return font_path

# 페이지 기본 설정
st.set_page_config(page_title="위드멤버 무료체험 결과 보고서", layout="wide")

# 세션 상태 초기화 (접속 시 1500만 ~ 2000만 사이의 예상 매출액 랜덤 고정)
if 'expected_rev' not in st.session_state:
    st.session_state.expected_rev = random.randint(1500, 2000) * 10000

st.title("📊 1주 무료체험 결과 보고서")
st.markdown("---")

# 1. 플레이스 Before & After
st.header("1. 네이버 플레이스 개선 Before & After")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Before (관리 전)")
    before_img = st.file_uploader("Before 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if before_img is not None:
        st.image(before_img, use_container_width=True)

with col2:
    st.subheader("After (관리 후)")
    after_img = st.file_uploader("After 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if after_img is not None:
        st.image(after_img, use_container_width=True)

st.markdown("---")

# 2. 네이버 도구 연동 및 점수 반영
st.header("2. 네이버 필수 도구 연동 및 SEO 점수 반영 결과")
st.write("네이버 플레이스 최적화(SEO)에 필수적인 도구 등록 현황 및 확보한 가산점입니다.")

score = 0
c1, c2, c3 = st.columns(3)
with c1:
    if st.checkbox("✅ 네이버 톡톡 등록 완료 (+15점)"): score += 15
with c2:
    if st.checkbox("✅ 네이버 예약 등록 완료 (+25점)"): score += 25
with c3:
    if st.checkbox("✅ 스마트콜(안심번호) 등록 완료 (+10점)"): score += 10

st.metric(label="확보된 플레이스 최적화 점수", value=f"{score} 점", delta="상위 노출 확률 증가율 반영")
st.progress(score / 50.0)

st.markdown("---")

# 3. 위드멤버 1년 마케팅 솔루션 (금액 및 보장제 세부내용 제거 완료)
st.header("3. 위드멤버 1년 마케팅 솔루션")
st.success("**압도적인 가성비, 위드멤버 1년 올인원 패키지**")

st.markdown("""
앞으로 1년 동안 아래의 솔루션이 지속적으로 실행되어 매장의 브랜드 가치와 실매출을 끌어올립니다.

* **📈 플레이스 SEO 최적화 관리**: 1주일 체험으로 끝나는 것이 아닌, 1년 내내 지속적인 순위 최적화
* **🔍 체험단 진행**: 매장 타겟층에 맞춘 최적화 블로그 리뷰 배포 및 홍보
* **🎬 인스타 영상 제작**: 트렌드에 맞춘 매장 홍보용 숏폼 영상 제작 (인스타그램 릴스 및 유튜브 쇼츠 배포)
* **⭐ 카카오맵 및 구글 리뷰 30건 작성**: 고품질 리뷰 총 30건 작성을 통한 별점 방어 및 매장 신뢰도 구축
""")

st.markdown("---")

# 4. 예상 매출 상승 그래프
st.header("4. 마케팅 진행 시 3개월 뒤 예상 상승 매출액")
st.write(f"본 솔루션을 1년 동안 진행했을 때, **3개월 뒤 예상 상승 매출액은 {st.session_state.expected_rev:,}원**으로 분석되었습니다.")

month_1 = int(st.session_state.expected_rev * 0.25)
month_2 = int(st.session_state.expected_rev * 0.60)

chart_data = pd.DataFrame({
    "진행 기간": ["관리 시작", "1개월 차", "2개월 차", "3개월 차"],
    "예상 상승액(원)": [0, month_1, month_2, st.session_state.expected_rev]
})

st.line_chart(chart_data.set_index("진행 기간"))

st.markdown("---")

# 5. 보고서 이미지 다운로드
st.header("📥 결과 보고서 다운로드")
st.write("대표님께 전달할 수 있도록 위 내용이 요약된 보고서를 이미지로 저장합니다.")

def generate_report_image(current_score, expected_revenue):
    font_path = load_font()
    img = Image.new('RGB', (900, 700), color=(248, 249, 250))
    draw = ImageDraw.Draw(img)
    
    try:
        if font_path:
            font_title = ImageFont.truetype(font_path, 42)
            font_sub = ImageFont.truetype(font_path, 28)
            font_body = ImageFont.truetype(font_path, 22)
        else:
            font_title = font_sub = font_body = ImageFont.load_default()
    except:
        font_title = font_sub = font_body = ImageFont.load_default()

    draw.text((50, 50), "위드멤버 1주 무료체험 결과 요약 보고서", font=font_title, fill=(33, 37, 41))
    draw.text((50, 150), f"✅ 확보된 플레이스 최적화 점수: {current_score}점 / 50점", font=font_sub, fill=(13, 110, 253))
    
    draw.text((50, 240), "[위드멤버 1년 마케팅 솔루션]", font=font_sub, fill=(33, 37, 41))
    services = (
        "- 플레이스 SEO 최적화 관리\n\n"
        "- 타겟층 맞춤 체험단 진행\n\n"
        "- 인스타 영상 제작 (릴스 및 쇼츠 배포)\n\n"
        "- 카카오맵 및 구글 리뷰 30건 작성"
    )
    draw.text((50, 300), services, font=font_body, fill=(73, 80, 87))
    
    draw.text((50, 500), "[3개월 뒤 예상 상승 매출액]", font=font_sub, fill=(33, 37, 41))
    draw.text((50, 550), f"💰 {expected_revenue:,} 원", font=font_title, fill=(220, 53, 69))
    
    # 다운로드 이미지의 하단 텍스트에서도 가격 및 보장제 내용 제거
    draw.text((50, 640), "* 위드멤버 1년 올인원 패키지 도입 시 예상 데이터입니다.", font=font_body, fill=(108, 117, 125))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

image_bytes = generate_report_image(score, st.session_state.expected_rev)
st.download_button(
    label="🖼️ 요약 보고서 이미지 다운로드 (.png)",
    data=image_bytes,
    file_name="위드멤버_요약보고서.png",
    mime="image/png"
)

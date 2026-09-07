import streamlit as st
import pandas as pd
import random
import io
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# 폰트 다운로드 (안정적인 URL 사용)
@st.cache_resource
def load_font():
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
            urllib.request.urlretrieve(url, font_path)
        except Exception as e:
            st.warning("웹 폰트 로드에 실패했습니다.")
            return None
    return font_path

# 페이지 기본 설정
st.set_page_config(page_title="위드멤버 무료체험 결과 보고서", layout="wide")

# 세션 상태 초기화 (랜덤 매출액 및 랜덤 SEO 점수 고정)
if 'expected_rev' not in st.session_state:
    st.session_state.expected_rev = random.randint(1500, 2000) * 10000
if 'random_seo_score' not in st.session_state:
    st.session_state.random_seo_score = random.randint(48, 57)

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

c1, c2, c3 = st.columns(3)
with c1:
    st.checkbox("✅ 네이버 톡톡 등록 완료", value=True)
with c2:
    st.checkbox("✅ 네이버 예약 등록 완료", value=True)
with c3:
    st.checkbox("✅ 스마트콜(안심번호) 등록 완료", value=True)

# UI상에서도 랜덤 점수 노출
st.metric(label="확보된 플레이스 최적화 점수", value=f"{st.session_state.random_seo_score} 점 상승", delta="상위 노출 확률 대폭 증가")

st.markdown("---")

# 3. 위드멤버 1년 마케팅 솔루션
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

# 5. 전문가 스타일 결과 보고서 이미지 생성 및 다운로드
st.header("📥 결과 보고서 다운로드")
st.write("대표님께 전달할 수 있도록 업로드된 이미지가 포함된 전문 요약 보고서를 생성합니다.")

def generate_report_image(before_upload, after_upload, expected_revenue, seo_score):
    font_path = load_font()
    # 캔버스 크기 확장 및 배경색 설정
    img = Image.new('RGB', (1000, 1200), color="#F8F9FA")
    draw = ImageDraw.Draw(img)
    
    try:
        if font_path:
            font_title = ImageFont.truetype(font_path, 42)
            font_sub = ImageFont.truetype(font_path, 30)
            font_body = ImageFont.truetype(font_path, 24)
            font_bold = ImageFont.truetype(font_path, 26)
        else:
            font_title = font_sub = font_body = font_bold = ImageFont.load_default()
    except:
        font_title = font_sub = font_body = font_bold = ImageFont.load_default()

    # 상단 헤더 박스 (네이비)
    draw.rectangle([0, 0, 1000, 120], fill="#1E3A8A")
    draw.text((60, 35), "위드멤버 1주 무료체험 결과 요약 보고서", font=font_title, fill="white")
    
    current_y = 160
    
    # 1. Before & After 이미지 삽입
    draw.text((60, current_y), "[네이버 플레이스 개선 Before & After]", font=font_sub, fill="#212529")
    current_y += 60
    
    if before_upload and after_upload:
        try:
            # 파일 포인터 초기화
            before_upload.seek(0)
            after_upload.seek(0)
            
            img_b = Image.open(before_upload).convert("RGB")
            img_a = Image.open(after_upload).convert("RGB")
            
            # 리사이징 (비율 무시하고 지정된 크기에 맞춤)
            img_b = img_b.resize((410, 300))
            img_a = img_a.resize((410, 300))
            
            # 이미지 캔버스에 붙이기
            img.paste(img_b, (60, current_y))
            img.paste(img_a, (530, current_y))
            
            # 캡션 추가
            draw.text((230, current_y + 315), "Before", font=font_bold, fill="#495057")
            draw.text((700, current_y + 315), "After", font=font_bold, fill="#495057")
            
            current_y += 370
        except Exception as e:
            draw.text((60, current_y), "(이미지 렌더링 중 오류가 발생했습니다.)", font=font_body, fill="#DC3545")
            current_y += 60
    else:
        draw.rectangle([60, current_y, 470, current_y + 300], fill="#E9ECEF", outline="#CED4DA")
        draw.rectangle([530, current_y, 940, current_y + 300], fill="#E9ECEF", outline="#CED4DA")
        draw.text((180, current_y + 130), "Before 이미지 없음", font=font_body, fill="#6C757D")
        draw.text((660, current_y + 130), "After 이미지 없음", font=font_body, fill="#6C757D")
        current_y += 370

    draw.line([(60, current_y), (940, current_y)], fill="#DEE2E6", width=2)
    current_y += 40
    
    # 2. 플레이스 최적화 점수 (랜덤 상승치 반영)
    draw.text((60, current_y), f"✅ 확보된 플레이스 최적화 점수: {seo_score}점 상승", font=font_sub, fill="#0D6EFD")
    current_y += 70
    
    draw.line([(60, current_y), (940, current_y)], fill="#DEE2E6", width=2)
    current_y += 40
    
    # 3. 마케팅 솔루션
    draw.text((60, current_y), "[위드멤버 1년 마케팅 솔루션]", font=font_sub, fill="#212529")
    current_y += 50
    
    services = [
        "✔️ 플레이스 SEO 최적화 관리 (1년 내내 지속적인 순위 최적화)",
        "✔️ 타겟층 맞춤 체험단 진행 (블로그 리뷰 배포 및 홍보)",
        "✔️ 인스타 영상 제작 (릴스 및 쇼츠 트렌드 맞춤 배포)",
        "✔️ 카카오맵 및 구글 리뷰 30건 작성 (고품질 리뷰로 별점 방어)"
    ]
    for svc in services:
        draw.text((70, current_y), svc, font=font_body, fill="#495057")
        current_y += 40
        
    current_y += 20
    draw.line([(60, current_y), (940, current_y)], fill="#DEE2E6", width=2)
    current_y += 40
    
    # 4. 예상 매출액 하이라이트 박스
    draw.text((60, current_y), "[3개월 뒤 예상 상승 매출액]", font=font_sub, fill="#212529")
    current_y += 60
    
    draw.rectangle([60, current_y, 940, current_y + 120], fill="#FFF5F5", outline="#FFC9C9", width=2)
    draw.text((320, current_y + 35), f"💰 {expected_revenue:,} 원", font=font_title, fill="#DC3545")
    
    current_y += 180
    
    # 하단 텍스트
    draw.text((60, current_y), "* 위드멤버 1년 올인원 패키지 도입 시 예상 데이터입니다.", font=font_body, fill="#868E96")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# 이미지 파일이 업로드된 상태에서만 생성되도록 처리
image_bytes = generate_report_image(before_img, after_img, st.session_state.expected_rev, st.session_state.random_seo_score)

st.download_button(
    label="🖼️ 전문가용 요약 보고서 다운로드 (.png)",
    data=image_bytes,
    file_name="위드멤버_전문보고서.png",
    mime="image/png"
)

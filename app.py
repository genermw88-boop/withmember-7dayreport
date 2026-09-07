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

# 이미지 비율 유지 리사이징 함수
def resize_with_aspect_ratio(image, target_width, target_height):
    img_ratio = image.width / image.height
    target_ratio = target_width / target_height
    
    if img_ratio > target_ratio:
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * img_ratio)
        
    try:
        resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except AttributeError:
        resized_img = image.resize((new_width, new_height), Image.LANCZOS)
        
    new_image = Image.new("RGB", (target_width, target_height), "white")
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    new_image.paste(resized_img, (offset_x, offset_y))
    
    return new_image

# 페이지 기본 설정
st.set_page_config(page_title="위드멤버 결과 보고 및 솔루션 제안", layout="wide")

if 'expected_rev' not in st.session_state:
    st.session_state.expected_rev = random.randint(1500, 2000) * 10000

st.title("📊 1주 무료체험 결과 및 솔루션 제안")
st.markdown("---")

# 1. 플레이스 Before & After 및 관리 항목 설정
st.header("1. 네이버 플레이스 개선 Before & After & 관리 항목 세팅")

col_set1, col_set2 = st.columns(2)
with col_set1:
    before_img = st.file_uploader("Before 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if before_img is not None:
        st.image(before_img, use_container_width=True)

with col_set2:
    after_img = st.file_uploader("After 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if after_img is not None:
        st.image(after_img, use_container_width=True)

st.markdown("### 🛠️ 플레이스 최적화 관리 항목 선택")
use_booking = st.checkbox("네이버 예약 연동 및 세팅 (고객 유입 편의성 증대)", value=True)
use_talk = st.checkbox("네이버 톡톡 세팅 및 응대 배너 적용 (소통 지수 상승)", value=True)
use_call = st.checkbox("안심번호 등록 및 키워드 최적화 (검색 알고리즘 반영)", value=True)

# 항목별 점수 산정
base_score = 30
score_booking = 12 if use_booking else 0
score_talk = 10 if use_talk else 0
score_call = 11 if use_call else 0
total_seo_score = base_score + score_booking + score_talk + score_call

st.info(f"💡 **현재 적용된 총 최적화 상승 점수:** **{total_seo_score}점** 상승 (기본 {base_score}점" +
         (f" + 예약 {score_booking}점" if use_booking else "") +
         (f" + 톡톡 {score_talk}점" if use_talk else "") +
         (f" + 안심번호 {score_call}점" if use_call else "") + ")")

st.markdown("---")

# 2. 위드멤버 1년 마케팅 솔루션
st.header("2. 위드멤버 1년 마케팅 솔루션")
st.markdown("""
* **네이버 플레이스 세팅 및 관리 (SEO최적화):** 단순 세팅을 넘어선 알고리즘 맞춤형 순위 최적화 및 지속 관리
* **맞춤형 블로그 체험단 운영:** 매장 타겟층 정밀 분석을 통한 최적화 블로그 후보 검수 및 고품질 리뷰 배포
* **숏폼 영상 콘텐츠 기획 및 제작:** 트렌디한 인스타그램 릴스 및 유튜브 쇼츠 배포를 통한 바이럴 확산
* **평점 및 리뷰 매니지먼트:** 카카오맵 및 구글 맵스 고품질 리뷰 30건 구축으로 매장 신뢰도 극대화
""")
st.markdown("---")

# 3. 예상 매출 상승
st.header("3. 3개월 뒤 예상 상승 매출액")
st.write(f"예상 상승 매출액: **{st.session_state.expected_rev:,}원**")

# 이미지 생성 함수 1: 체험 결과 (삽입 이미지 더욱 확대 및 관리 내역 반영)
def generate_result_image(before_upload, after_upload, use_b, use_t, use_c, total_score):
    font_path = load_font()
    img = Image.new('RGB', (1000, 1300), color="#F8F9FA")
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
        font_body = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()
        font_bold = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    except:
        font_title = font_sub = font_body = font_bold = ImageFont.load_default()

    draw.rectangle([0, 0, 1000, 110], fill="#1E3A8A")
    draw.text((50, 32), "위드멤버 1주 무료체험 결과 요약 보고서", font=font_title, fill="white")
    
    draw.text((50, 135), "[네이버 플레이스 개선 Before & After]", font=font_sub, fill="#212529")
    
    if before_upload and after_upload:
        try:
            before_upload.seek(0)
            after_upload.seek(0)
            img_b = Image.open(before_upload).convert("RGB")
            img_a = Image.open(after_upload).convert("RGB")
            
            # 플레이스 이미지 크기 대폭 확대 (440x580)
            img_b = resize_with_aspect_ratio(img_b, 440, 580)
            img_a = resize_with_aspect_ratio(img_a, 440, 580)
            
            img.paste(img_b, (50, 185))
            img.paste(img_a, (510, 185))
            
            draw.text((235, 780), "Before", font=font_bold, fill="#495057")
            draw.text((695, 780), "After", font=font_bold, fill="#495057")
        except Exception:
            pass
            
    # 플레이스 관리 세부 내역 영역
    draw.rectangle([50, 830, 950, 1180], fill="white", outline="#CED4DA", width=2)
    draw.text((75, 850), "📌 위드멤버 플레이스 중점 관리 및 상승 내역", font=font_bold, fill="#1E3A8A")
    
    y_pos = 900
    details = [("기본 플레이스 SEO 최적화 및 정보 정비", "+30점", True)]
    if use_b:
        details.append(("네이버 예약 연동 (고객 편의성 및 체류 시간 증대)", "+12점", True))
    if use_t:
        details.append(("네이버 톡톡 응대 배너 적용 (실시간 소통 지수 반영)", "+10점", True))
    if use_c:
        details.append(("안심번호 등록 및 검색 노출 알고리즘 최적화", "+11점", True))
        
    for text, score, active in details:
        draw.text((80, y_pos), f"• {text}", font=font_body, fill="#333333" if active else "#ADB5BD")
        draw.text((820, y_pos), score, font=font_body, fill="#0D6EFD" if active else "#ADB5BD")
        y_pos += 40
        
    draw.line([(75, y_pos + 10), (925, y_pos + 10)], fill="#DEE2E6", width=2)
    draw.text((75, y_pos + 30), f"✅ 확보된 플레이스 최적화 점수 총합: {total_score}점 상승", font=font_title, fill="#DC3545")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# 이미지 생성 함수 2: 마케팅 솔루션 & 매출 그래프 (완전 중앙 정렬)
def generate_solution_image(expected_revenue):
    font_path = load_font()
    img = Image.new('RGB', (1000, 1350), color="#F8F9FA")
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(font_path, 40) if font_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(font_path, 30) if font_path else ImageFont.load_default()
        font_body = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()
    except:
        font_title = font_sub = font_body = ImageFont.load_default()

    draw.rectangle([0, 0, 1000, 110], fill="#1E3A8A")
    draw.text((50, 32), "위드멤버 1년 마케팅 솔루션 제안서", font=font_title, fill="white")
    
    draw.text((50, 135), "[전문적인 마케팅 관리 솔루션]", font=font_sub, fill="#212529")
    
    services = [
        ("1. 네이버 플레이스 세팅 및 관리 (SEO최적화)", "단순 세팅을 넘어선 알고리즘 맞춤형 순위 최적화 및 지속 관리"),
        ("2. 맞춤형 블로그 체험단 운영", "매장 타겟층 정밀 분석을 통한 최적화 블로그 후보 검수 및 추천 배포"),
        ("3. 숏폼 영상 콘텐츠 기획 및 제작", "트렌디한 홍보 영상 제작 후 인스타그램 릴스 및 유튜브 쇼츠 배포"),
        ("4. 평점 및 리뷰 매니지먼트", "카카오맵 및 구글 맵스 고품질 리뷰 30건 구축으로 매장 신뢰도 극대화")
    ]
    
    y = 210
    for title, desc in services:
        draw.text((50, y), title, font=font_sub, fill="#0D6EFD")
        draw.text((75, y + 42), f"- {desc}", font=font_body, fill="#495057")
        y += 95
        
    draw.line([(50, y + 10), (950, y + 10)], fill="#DEE2E6", width=2)
    y += 45
    
    draw.text((50, y), "[3개월 뒤 예상 상승 매출액 및 추이]", font=font_sub, fill="#212529")
    y += 65
    
    # 매출 강조 박스 (정가운데 배치)
    draw.rectangle([50, y, 950, y + 90], fill="#FFF5F5", outline="#FFC9C9", width=2)
    rev_text = f"💰 총 예상 상승액: {expected_revenue:,} 원"
    draw.text((230, y + 25), rev_text, font=font_title, fill="#DC3545")
    
    y += 145
    
    # === 꺾은선 그래프 완벽 중앙 정렬 ===
    graph_x, graph_y = 120, y
    graph_w, graph_h = 760, 240
    
    draw.line([(graph_x, graph_y + graph_h), (graph_x + graph_w, graph_y + graph_h)], fill="#ADB5BD", width=3)
    
    labels = ["관리 시작", "1개월 차", "2개월 차", "3개월 차"]
    values = [0, expected_revenue * 0.25, expected_revenue * 0.60, expected_revenue]
    
    points = []
    x_step = graph_w / 3
    for i in range(4):
        px = graph_x + (i * x_step)
        py = (graph_y + graph_h) - (graph_h * (values[i] / expected_revenue))
        points.append((px, py))
        
        # X축 라벨 중앙 정렬 오프셋 적용
        draw.text((px - 35, graph_y + graph_h + 15), labels[i], font=font_body, fill="#495057")
        
        if i > 0:
            val_text = f"{int(values[i]/10000):,}만"
            draw.text((px - 30, py - 35), val_text, font=font_body, fill="#0D6EFD")

    draw.line(points, fill="#0D6EFD", width=4)
    for p in points:
        draw.ellipse([p[0]-7, p[1]-7, p[0]+7, p[1]+7], fill="#DC3545", outline="white", width=2)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

st.header("📥 분석 리포트 다운로드 (2종)")
st.write("이미지가 업로드되면 다운로드 버튼이 활성화됩니다.")

if before_img and after_img:
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        img1_bytes = generate_result_image(before_img, after_img, use_booking, use_talk, use_call, total_seo_score)
        st.download_button(
            label="1️⃣ 체험 결과 (Before/After) 이미지 다운로드",
            data=img1_bytes,
            file_name="1_위드멤버_결과보고.png",
            mime="image/png"
        )
        
    with col_btn2:
        img2_bytes = generate_solution_image(st.session_state.expected_rev)
        st.download_button(
            label="2️⃣ 마케팅 솔루션 및 매출 그래프 다운로드",
            data=img2_bytes,
            file_name="2_위드멤버_솔루션제안.png",
            mime="image/png"
        )
else:
    st.warning("Before와 After 이미지를 모두 업로드해야 보고서를 다운로드할 수 있습니다.")

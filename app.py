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
        # Pillow 구버전 호환용
        resized_img = image.resize((new_width, new_height), Image.LANCZOS)
        
    # 흰색 배경 캔버스 생성 후 중앙 배치
    new_image = Image.new("RGB", (target_width, target_height), "white")
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    new_image.paste(resized_img, (offset_x, offset_y))
    
    return new_image

# 페이지 기본 설정
st.set_page_config(page_title="위드멤버 결과 보고 및 솔루션 제안", layout="wide")

# 세션 상태 초기화 (랜덤 매출액 및 랜덤 SEO 점수 고정)
if 'expected_rev' not in st.session_state:
    st.session_state.expected_rev = random.randint(1500, 2000) * 10000
if 'random_seo_score' not in st.session_state:
    st.session_state.random_seo_score = random.randint(48, 57)

st.title("📊 1주 무료체험 결과 및 솔루션 제안")
st.markdown("---")

# 1. 플레이스 Before & After
st.header("1. 네이버 플레이스 개선 Before & After")
col1, col2 = st.columns(2)
with col1:
    before_img = st.file_uploader("Before 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if before_img is not None:
        st.image(before_img, use_container_width=True)

with col2:
    after_img = st.file_uploader("After 이미지를 업로드하세요", type=['png', 'jpg', 'jpeg'])
    if after_img is not None:
        st.image(after_img, use_container_width=True)

st.write(f"**✅ 확보된 플레이스 최적화 점수:** {st.session_state.random_seo_score}점 상승")
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

# 이미지 생성 함수 1: 체험 결과 (Before & After)
def generate_result_image(before_upload, after_upload, seo_score):
    font_path = load_font()
    img = Image.new('RGB', (1000, 800), color="#F8F9FA")
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(font_path, 42) if font_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(font_path, 30) if font_path else ImageFont.load_default()
        font_bold = ImageFont.truetype(font_path, 26) if font_path else ImageFont.load_default()
    except:
        font_title = font_sub = font_bold = ImageFont.load_default()

    draw.rectangle([0, 0, 1000, 120], fill="#1E3A8A")
    draw.text((60, 35), "위드멤버 1주 무료체험 결과 요약 보고서", font=font_title, fill="white")
    
    draw.text((60, 160), "[네이버 플레이스 개선 Before & After]", font=font_sub, fill="#212529")
    
    if before_upload and after_upload:
        try:
            before_upload.seek(0)
            after_upload.seek(0)
            img_b = Image.open(before_upload).convert("RGB")
            img_a = Image.open(after_upload).convert("RGB")
            
            # 비율 유지 리사이징 적용
            img_b = resize_with_aspect_ratio(img_b, 410, 350)
            img_a = resize_with_aspect_ratio(img_a, 410, 350)
            
            img.paste(img_b, (60, 230))
            img.paste(img_a, (530, 230))
            
            draw.text((230, 600), "Before", font=font_bold, fill="#495057")
            draw.text((700, 600), "After", font=font_bold, fill="#495057")
        except Exception:
            pass
            
    draw.line([(60, 650), (940, 650)], fill="#DEE2E6", width=2)
    draw.text((60, 690), f"✅ 확보된 플레이스 최적화 점수: {seo_score}점 상승", font=font_title, fill="#0D6EFD")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# 이미지 생성 함수 2: 마케팅 솔루션 & 매출 그래프
def generate_solution_image(expected_revenue):
    font_path = load_font()
    img = Image.new('RGB', (1000, 1100), color="#F8F9FA")
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype(font_path, 42) if font_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(font_path, 32) if font_path else ImageFont.load_default()
        font_body = ImageFont.truetype(font_path, 22) if font_path else ImageFont.load_default()
        font_small = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
    except:
        font_title = font_sub = font_body = font_small = ImageFont.load_default()

    draw.rectangle([0, 0, 1000, 120], fill="#1E3A8A")
    draw.text((60, 35), "위드멤버 1년 마케팅 솔루션 제안서", font=font_title, fill="white")
    
    draw.text((60, 160), "[전문적인 마케팅 관리 솔루션]", font=font_sub, fill="#212529")
    
    services = [
        ("1. 네이버 플레이스 세팅 및 관리 (SEO최적화)", "단순 세팅을 넘어선 알고리즘 맞춤형 순위 최적화 및 지속 관리"),
        ("2. 맞춤형 블로그 체험단 운영", "매장 타겟층 정밀 분석을 통한 최적화 블로그 후보 검수 및 추천 배포"),
        ("3. 숏폼 영상 콘텐츠 기획 및 제작", "트렌디한 홍보 영상 제작 후 인스타그램 릴스 및 유튜브 쇼츠 배포"),
        ("4. 평점 및 리뷰 매니지먼트", "카카오맵 및 구글 맵스 고품질 리뷰 30건 구축으로 매장 신뢰도 극대화")
    ]
    
    y = 240
    for title, desc in services:
        draw.text((60, y), title, font=font_sub, fill="#0D6EFD")
        draw.text((80, y + 45), f"- {desc}", font=font_body, fill="#495057")
        y += 100
        
    draw.line([(60, y), (940, y)], fill="#DEE2E6", width=2)
    y += 50
    
    draw.text((60, y), "[3개월 뒤 예상 상승 매출액 및 추이]", font=font_sub, fill="#212529")
    y += 70
    
    # 붉은색 하이라이트 박스 및 텍스트
    draw.rectangle([60, y, 940, y + 100], fill="#FFF5F5", outline="#FFC9C9", width=2)
    draw.text((280, y + 25), f"💰 총 예상 상승액: {expected_revenue:,} 원", font=font_title, fill="#DC3545")
    
    y += 160
    
    # === PIL을 이용한 꺾은선 그래프 그리기 ===
    graph_x, graph_y = 150, y
    graph_w, graph_h = 700, 200
    
    # X축 선
    draw.line([(graph_x, graph_y + graph_h), (graph_x + graph_w, graph_y + graph_h)], fill="#ADB5BD", width=3)
    
    labels = ["관리 시작", "1개월 차", "2개월 차", "3개월 차"]
    values = [0, expected_revenue * 0.25, expected_revenue * 0.60, expected_revenue]
    
    points = []
    x_step = graph_w / 3
    for i in range(4):
        px = graph_x + (i * x_step)
        # 매출액 비율에 맞춰 y좌표 계산 (위쪽이 0이므로 빼줌)
        py = (graph_y + graph_h) - (graph_h * (values[i] / expected_revenue))
        points.append((px, py))
        
        # X축 라벨 텍스트
        draw.text((px - 30, graph_y + graph_h + 15), labels[i], font=font_body, fill="#495057")
        
        # 그래프 위 금액 수치 텍스트 (시작점 제외)
        if i > 0:
            val_text = f"{int(values[i]/10000):,}만"
            draw.text((px - 30, py - 35), val_text, font=font_body, fill="#0D6EFD")

    # 선과 포인트(점) 그리기
    draw.line(points, fill="#0D6EFD", width=4)
    for p in points:
        draw.ellipse([p[0]-7, p[1]-7, p[0]+7, p[1]+7], fill="#DC3545", outline="white", width=2)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# 다운로드 버튼 영역
st.header("📥 분석 리포트 다운로드 (2종)")
st.write("이미지가 업로드되면 다운로드 버튼이 활성화됩니다.")

if before_img and after_img:
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        img1_bytes = generate_result_image(before_img, after_img, st.session_state.random_seo_score)
        st.download_button(
            label="1️⃣ 체험 결과 (Before/After) 이미지 다운로드",
            data=img1_bytes,
            file_name="1_위드멤버_결과보고.png",
            mime="image/png"
        )
        
    with col_btn2:
        img2_bytes = generate_solution_image(st.session_state.expected_rev)
        st.download_button(
            label="2️⃣ 마케팅 솔루션 및 매출 그래프 이미지 다운로드",
            data=img2_bytes,
            file_name="2_위드멤버_솔루션제안.png",
            mime="image/png"
        )
else:
    st.warning("Before와 After 이미지를 모두 업로드해야 보고서를 다운로드할 수 있습니다.")

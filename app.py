import streamlit as st
import random
import base64

st.set_page_config(page_title="위드멤버 마케팅 보고서 & 솔루션 시스템", layout="wide")

if 'expected_rev' not in st.session_state:
    st.session_state.expected_rev = random.randint(1500, 2000) * 10000

# 새로고침이나 체크박스 토글 시 점수가 매번 자연스럽게 갱신되도록 세션 상태 활용
if 'score_booking' not in st.session_state:
    st.session_state.score_booking = random.randint(10, 15)
if 'score_talk' not in st.session_state:
    st.session_state.score_talk = random.randint(8, 12)
if 'score_call' not in st.session_state:
    st.session_state.score_call = random.randint(9, 14)
if 'score_news' not in st.session_state:
    st.session_state.score_news = random.randint(10, 15)
if 'score_keyword' not in st.session_state:
    st.session_state.score_keyword = random.randint(12, 18)

st.title("📊 위드멤버 마케팅 보고서 & 1년 솔루션 분리 출력 시스템")
st.markdown("---")

st.sidebar.header("⚙️ 리포트 설정 및 이미지 입력")
before_file = st.sidebar.file_uploader("Before 이미지 업로드", type=['png', 'jpg', 'jpeg'])
after_file = st.sidebar.file_uploader("After 이미지 업로드", type=['png', 'jpg', 'jpeg'])

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ 플레이스 최적화 관리 항목")

# 요청하신 5가지 항목 체크박스 배치
use_booking = st.sidebar.checkbox(f"네이버 예약 연동 및 세팅 (+{st.session_state.score_booking}점)", value=True)
use_talk = st.sidebar.checkbox(f"네이버 톡톡 응대 배너 적용 (+{st.session_state.score_talk}점)", value=True)
use_call = st.sidebar.checkbox(f"안심번호 등록 및 키워드 최적화 (+{st.session_state.score_call}점)", value=True)
use_news = st.sidebar.checkbox(f"플레이스 새소식 업데이트 (+{st.session_state.score_news}점)", value=True)
use_keyword = st.sidebar.checkbox(f"플레이스 메인키워드 수정 (+{st.session_state.score_keyword}점)", value=True)

# 체크 여부에 따른 최종 종합 점수 계산
score_booking_val = st.session_state.score_booking if use_booking else 0
score_talk_val = st.session_state.score_talk if use_talk else 0
score_call_val = st.session_state.score_call if use_call else 0
score_news_val = st.session_state.score_news if use_news else 0
score_keyword_val = st.session_state.score_keyword if use_keyword else 0

total_seo_score = score_booking_val + score_talk_val + score_call_val + score_news_val + score_keyword_val

def get_image_base64(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        encoded = base64.b64encode(bytes_data).decode()
        return f"data:image/png;base64,{encoded}"
    return None

before_b64 = get_image_base64(before_file)
after_b64 = get_image_base64(after_file)

before_img_tag = f'<img src="{before_b64}" style="width: 100%; height: 100%; object-fit: cover; object-position: top; border-radius: 6px;" />' if before_b64 else '<span style="color: #94A3B8; font-size: 14px;">Before 이미지 미등록</span>'
after_img_tag = f'<img src="{after_b64}" style="width: 100%; height: 100%; object-fit: cover; object-position: top; border-radius: 6px;" />' if after_b64 else '<span style="color: #94A3B8; font-size: 14px;">After 이미지 미등록</span>'

details_html = ""
if use_booking:
    details_html += f'<div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;"><span style="color: #334155;">• 네이버 예약 연동 (고객 편의성 및 체류 시간 증대)</span><span style="color: #2563EB; font-weight: bold;">+{score_booking_val}점</span></div>'
if use_talk:
    details_html += f'<div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;"><span style="color: #334155;">• 네이버 톡톡 응대 배너 적용 (실시간 소통 지수 반영)</span><span style="color: #2563EB; font-weight: bold;">+{score_talk_val}점</span></div>'
if use_call:
    details_html += f'<div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;"><span style="color: #334155;">• 안심번호 등록 및 키워드 최적화</span><span style="color: #2563EB; font-weight: bold;">+{score_call_val}점</span></div>'
if use_news:
    details_html += f'<div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;"><span style="color: #334155;">• 플레이스 새소식 업데이트 (활성화 지수 및 최신성 확보)</span><span style="color: #2563EB; font-weight: bold;">+{score_news_val}점</span></div>'
if use_keyword:
    details_html += f'<div style="display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 14px;"><span style="color: #334155;">• 플레이스 메인키워드 수정 (타겟 검색 유입 극대화)</span><span style="color: #2563EB; font-weight: bold;">+{score_keyword_val}점</span></div>'

rev = st.session_state.expected_rev
rev_formatted = f"{rev:,}"

m1 = int(rev * 0.15 / 10000)
m2 = int(rev * 0.45 / 10000)
m3 = int(rev / 10000)

separate_reports_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
    body {{ font-family: 'Nanum Gothic', sans-serif; background: #F1F5F9; margin: 0; padding: 20px; }}
    .main-wrapper {{ max-width: 900px; margin: 0 auto; }}
    .report-card {{ background: #FFFFFF; padding: 35px; border-radius: 12px; border: 1px solid #CBD5E1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 40px; position: relative; }}
    .download-bar {{ text-align: right; margin-bottom: 12px; }}
    .download-btn {{ background: #2563EB; color: white; border: none; padding: 10px 20px; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    .download-btn:hover {{ background: #1D4ED8; }}
    .header-banner {{ background: #0F172A; color: white; padding: 20px 25px; border-radius: 8px; font-size: 20px; font-weight: bold; margin-bottom: 25px; }}
    .section-title {{ color: #1E293B; font-size: 16px; font-weight: bold; margin-bottom: 15px; border-left: 4px solid #2563EB; padding-left: 10px; }}
</style>
</head>
<body>

<div class="main-wrapper">

    <!-- [보고서 1] 1주 무료체험 결과 요약 보고서 -->
    <div class="download-bar">
        <button class="download-btn" onclick="downloadReport('report-1', '위드멤버_1주무료체험_결과보고서.png')">📥 1주 무료체험 보고서 저장</button>
    </div>
    
    <div id="report-1" class="report-card">
        <div class="header-banner">
            위드멤버 1주 무료체험 결과 요약 보고서
        </div>
        
        <div class="section-title">[ 네이버 플레이스 개선 Before & After ]</div>
        <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 25px;">
            <div style="flex: 1; text-align: center; background: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
                <div style="width: 100%; height: 580px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; overflow: hidden; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px;">
                    {before_img_tag}
                </div>
                <div style="display: inline-block; background: #F1F5F9; padding: 4px 16px; border-radius: 4px; font-weight: bold; color: #475569; font-size: 13px; margin-top: 5px;">Before</div>
            </div>
            <div style="flex: 1; text-align: center; background: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0;">
                <div style="width: 100%; height: 580px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px; overflow: hidden; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px;">
                    {after_img_tag}
                </div>
                <div style="display: inline-block; background: #EFF6FF; padding: 4px 16px; border-radius: 4px; font-weight: bold; color: #2563EB; font-size: 13px; margin-top: 5px;">After</div>
            </div>
        </div>

        <div style="background: #FAFAFA; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px;">
            <div style="font-weight: bold; color: #0F172A; margin-bottom: 15px; font-size: 14px;">📌 위드멤버 플레이스 중점 관리 및 상승 내역</div>
            {details_html}
            <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 15px 0;">
            <div style="background: #FEF2F2; border: 1px solid #FECACA; padding: 12px; border-radius: 6px; color: #DC2626; font-weight: bold; text-align: center; font-size: 15px;">
                ✅ 확보된 플레이스 최적화 점수 총합: {total_seo_score}점 상승
            </div>
        </div>
    </div>


    <!-- [보고서 2] 1년 마케팅 솔루션 제안서 -->
    <div class="download-bar">
        <button class="download-btn" onclick="downloadReport('report-2', '위드멤버_1년마케팅솔루션_제안서.png')">📥 1년 마케팅 솔루션 제안서 저장</button>
    </div>

    <div id="report-2" class="report-card">
        
        <div class="section-title" style="margin-top: 0;">[ 전문적인 마케팅 관리 솔루션 ]</div>
        <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 25px;">
            <div style="background: #F8FAFC; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 6px; border-left: 5px solid #2563EB;">
                <div style="font-weight: bold; color: #2563EB; margin-bottom: 4px; font-size: 14px;">1. 네이버 플레이스 세팅 및 관리 (SEO최적화)</div>
                <div style="font-size: 13px; color: #475569;">- 단순 세팅을 넘어선 알고리즘 맞춤형 순위 최적화 및 지속 관리</div>
            </div>
            <div style="background: #F8FAFC; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 6px; border-left: 5px solid #2563EB;">
                <div style="font-weight: bold; color: #2563EB; margin-bottom: 4px; font-size: 14px;">2. 맞춤형 블로그 체험단 운영</div>
                <div style="font-size: 13px; color: #475569;">- 매장 타겟층 정밀 분석을 통한 최적화 블로그 후보 검수 및 추천 배포</div>
            </div>
            <div style="background: #F8FAFC; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 6px; border-left: 5px solid #2563EB;">
                <div style="font-weight: bold; color: #2563EB; margin-bottom: 4px; font-size: 14px;">3. 숏폼 영상 콘텐츠 기획 및 제작</div>
                <div style="font-size: 13px; color: #475569;">- 트렌디한 홍보 영상 제작 후 인스타그램 릴스 및 유튜브 쇼츠 배포</div>
            </div>
            <div style="background: #F8FAFC; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 6px; border-left: 5px solid #2563EB;">
                <div style="font-weight: bold; color: #2563EB; margin-bottom: 4px; font-size: 14px;">4. 평점 및 리뷰 매니지먼트</div>
                <div style="font-size: 13px; color: #475569;">- 카카오맵 및 구글 맵스 고품질 리뷰 30건 구축으로 매장 신뢰도 극대화</div>
            </div>
            <div style="background: #F8FAFC; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 6px; border-left: 5px solid #2563EB;">
                <div style="font-weight: bold; color: #2563EB; margin-bottom: 4px; font-size: 14px;">5. 트래픽 작업을 통한 플레이스 순위 상승</div>
                <div style="font-size: 13px; color: #475569;">- 실사용자 패턴 기반 맞춤형 유입 트래픽 제어로 네이버 알고리즘 상위 노출 극대화</div>
            </div>
        </div>

        <div class="section-title">[ 3개월 뒤 예상 상승 매출액 및 추이 ]</div>
        
        <div style="background: #FEF2F2; border: 1px solid #FECACA; padding: 14px 18px; border-radius: 6px; text-align: center; color: #DC2626; font-size: 18px; font-weight: bold; margin-bottom: 15px; width: 100%; box-sizing: border-box;">
            💰 총 예상 상승액: {rev_formatted} 원
        </div>
        
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px 25px 15px 25px; border-radius: 6px; text-align: center; width: 100%; box-sizing: border-box;">
            <svg viewBox="0 0 800 220" width="100%" height="100%" style="overflow: visible;">
                <path d="M 100,175 Q 400,165 730,35" fill="none" stroke="#DC2626" stroke-width="4" />
                
                <circle cx="100" cy="175" r="6" fill="#DC2626" stroke="white" stroke-width="2"/>
                <text x="100" y="205" font-size="13" fill="#475569" text-anchor="middle" font-weight="bold">관리 시작</text>
                
                <circle cx="310" cy="160" r="6" fill="#DC2626" stroke="white" stroke-width="2"/>
                <text x="310" y="142" font-size="14" fill="#DC2626" text-anchor="middle" font-weight="bold">{m1:,}만</text>
                <text x="310" y="205" font-size="13" fill="#475569" text-anchor="middle" font-weight="bold">1개월 차</text>
                
                <circle cx="525" cy="115" r="6" fill="#DC2626" stroke="white" stroke-width="2"/>
                <text x="525" y="97" font-size="14" fill="#DC2626" text-anchor="middle" font-weight="bold">{m2:,}만</text>
                <text x="525" y="205" font-size="13" fill="#475569" text-anchor="middle" font-weight="bold">2개월 차</text>
                
                <circle cx="730" cy="35" r="6" fill="#DC2626" stroke="white" stroke-width="2"/>
                <text x="730" y="17" font-size="14" fill="#DC2626" text-anchor="middle" font-weight="bold">{m3:,}만</text>
                <text x="730" y="205" font-size="13" fill="#475569" text-anchor="middle" font-weight="bold">3개월 차</text>
            </svg>
        </div>
    </div>

</div>

<script>
function downloadReport(elementId, filename) {{
    const target = document.getElementById(elementId);
    html2canvas(target, {{ scale: 2, useCORS: true }}).then(canvas => {{
        const link = document.createElement('a');
        link.download = filename;
        link.href = canvas.toDataURL('image/png');
        link.click();
    }});
}}
</script>

</body>
</html>
"""

st.components.v1.html(separate_reports_html, height=2050, scrolling=True)

import os
import random

import streamlit as st
import anthropic
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
CHARACTER_IMG = os.path.join(BASE_DIR, "character_small.png")
AVATAR = os.path.join(BASE_DIR, "avatar.png")  # 말풍선 옆 얼굴 프사

# 메이저 아르카나 22장: (표시명, 이미지 파일명)
MAJOR_ARCANA = [
    ("0. 바보 (The Fool)", "RWS_Tarot_00_Fool.jpg"),
    ("1. 마법사 (The Magician)", "RWS_Tarot_01_Magician.jpg"),
    ("2. 여사제 (The High Priestess)", "RWS_Tarot_02_High_Priestess.jpg"),
    ("3. 여황제 (The Empress)", "RWS_Tarot_03_Empress.jpg"),
    ("4. 황제 (The Emperor)", "RWS_Tarot_04_Emperor.jpg"),
    ("5. 교황 (The Hierophant)", "RWS_Tarot_05_Hierophant.jpg"),
    ("6. 연인 (The Lovers)", "RWS_Tarot_06_Lovers.jpg"),
    ("7. 전차 (The Chariot)", "RWS_Tarot_07_Chariot.jpg"),
    ("8. 힘 (Strength)", "RWS_Tarot_08_Strength.jpg"),
    ("9. 은둔자 (The Hermit)", "RWS_Tarot_09_Hermit.jpg"),
    ("10. 운명의 수레바퀴 (Wheel of Fortune)", "RWS_Tarot_10_Wheel_of_Fortune.jpg"),
    ("11. 정의 (Justice)", "RWS_Tarot_11_Justice.jpg"),
    ("12. 매달린 사람 (The Hanged Man)", "RWS_Tarot_12_Hanged_Man.jpg"),
    ("13. 죽음 (Death)", "RWS_Tarot_13_Death.jpg"),
    ("14. 절제 (Temperance)", "RWS_Tarot_14_Temperance.jpg"),
    ("15. 악마 (The Devil)", "RWS_Tarot_15_Devil.jpg"),
    ("16. 탑 (The Tower)", "RWS_Tarot_16_Tower.jpg"),
    ("17. 별 (The Star)", "RWS_Tarot_17_Star.jpg"),
    ("18. 달 (The Moon)", "RWS_Tarot_18_Moon.jpg"),
    ("19. 태양 (The Sun)", "RWS_Tarot_19_Sun.jpg"),
    ("20. 심판 (Judgement)", "RWS_Tarot_20_Judgement.jpg"),
    ("21. 세계 (The World)", "RWS_Tarot_21_World.jpg"),
]

MODEL = "claude-haiku-4-5-20251001"  # 타로 해석은 가벼워서 haiku로 충분


def get_api_key():
    """환경변수 우선, 없으면 Streamlit secrets. 둘 다 없으면 None."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None


def read_card(concern: str, card: str, orientation: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        "당신은 신비롭고 다정한 20대 타로술사 캐릭터입니다. "
        "사용자에게 직접 말을 거는 1인칭 말투로, 차분하지만 따뜻하게 이야기하세요. "
        "아래 다섯 항목을 각각 굵은 소제목으로 달되, 번호나 글머리 기호(-, •, 1. 등)는 절대 붙이지 마세요. "
        "각 소제목 아래 내용은 캐릭터가 말 거는 1인칭 말투로 1~2문장 씁니다. "
        "소제목+내용 묶음 사이는 반드시 빈 줄로 띄웁니다. "
        "일반론이 아니라 이 고민에 맞춘 구체적인 메시지를 주세요.\n\n"
        "**당신의 상황**\n"
        "**그 밑에 깔린 마음**\n"
        "**이 카드의 의미** (정방향/역방향 포함)\n"
        "**카드와 당신의 연결**\n"
        "**오늘 해볼 행동**\n\n"
        f"고민: {concern}\n"
        f"뽑힌 카드: {card} ({orientation})\n\n"
    )
    msg = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


st.set_page_config(page_title="타로 한 장", page_icon="🔮")

st.title("🔮 타로 한 장")

intro_col1, intro_col2 = st.columns([1, 2])
with intro_col1:
    st.image(CHARACTER_IMG, width=150)
with intro_col2:
    st.markdown(
        "**신비로운 타로술사**가 당신의 고민을 들어드립니다.\n\n"
        "고민을 한 줄 적고 카드를 뽑아보세요. 메이저 아르카나 22장 중 한 장이 나옵니다."
    )

concern = st.text_input(
    "오늘의 고민",
    placeholder="예: 지금 벌인 일을 계속 끌고 가도 될까?",
)

if st.button("카드 뽑기", type="primary"):
    if not concern.strip():
        st.warning("고민을 한 줄 적어주세요.")
        st.stop()

    name, filename = random.choice(MAJOR_ARCANA)
    orientation = random.choice(["정방향", "역방향"])

    card_img = Image.open(os.path.join(IMG_DIR, filename))
    if orientation == "역방향":
        card_img = card_img.rotate(180)

    api_key = get_api_key()
    if not api_key:
        # 키가 없으면 조용히 더미를 주지 않고 명확히 멈춘다
        st.error(
            "ANTHROPIC_API_KEY가 설정되지 않았습니다.\n\n"
            "- 로컬: 터미널에서 `export ANTHROPIC_API_KEY=sk-...` 후 다시 실행\n"
            "- 배포: Streamlit Cloud의 Secrets에 `ANTHROPIC_API_KEY` 추가"
        )
        st.stop()

    intro_l, intro_r = st.columns([1, 6])
    with intro_l:
        st.image(AVATAR)
    with intro_r:
        st.markdown("당신의 고민, 잘 들었어요.\n\n카드를 한 장 펼쳐볼게요...")

    st.image(card_img, width=200)
    st.markdown(f"**{name} · {orientation}**")

    with st.spinner("카드를 읽는 중..."):
        reading = read_card(concern, name, orientation, api_key)

    read_l, read_r = st.columns([1, 6])
    with read_l:
        st.image(AVATAR)
    with read_r:
        st.markdown(reading)

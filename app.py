import os
import random

import streamlit as st
import anthropic

# 메이저 아르카나 22장 (MVP는 메이저만)
MAJOR_ARCANA = [
    "0. 바보 (The Fool)",
    "1. 마법사 (The Magician)",
    "2. 여사제 (The High Priestess)",
    "3. 여황제 (The Empress)",
    "4. 황제 (The Emperor)",
    "5. 교황 (The Hierophant)",
    "6. 연인 (The Lovers)",
    "7. 전차 (The Chariot)",
    "8. 힘 (Strength)",
    "9. 은둔자 (The Hermit)",
    "10. 운명의 수레바퀴 (Wheel of Fortune)",
    "11. 정의 (Justice)",
    "12. 매달린 사람 (The Hanged Man)",
    "13. 죽음 (Death)",
    "14. 절제 (Temperance)",
    "15. 악마 (The Devil)",
    "16. 탑 (The Tower)",
    "17. 별 (The Star)",
    "18. 달 (The Moon)",
    "19. 태양 (The Sun)",
    "20. 심판 (Judgement)",
    "21. 세계 (The World)",
]

MODEL = "claude-haiku-4-5-20251001"  # 타로 해석은 가벼워서 haiku로 충분


def get_api_key():
    """환경변수 우선, 없으면 Streamlit secrets. 둘 다 없으면 None."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    # st.secrets는 secrets 파일이 없으면 접근 시 예외를 던지므로 감싼다
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None


def read_card(concern: str, card: str, orientation: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        "당신은 따뜻하지만 막연하지 않은 타로 리더입니다. "
        "사용자의 고민과 뽑힌 카드를 연결해 5~7문장으로 해석해 주세요. "
        "일반론이 아니라 이 고민에 맞춘 구체적인 메시지를 주고, 마지막 한 문장은 행동 제안으로 끝내세요.\n\n"
        f"고민: {concern}\n"
        f"뽑힌 카드: {card} ({orientation})\n\n"
        "해석:"
    )
    msg = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


st.title("🔮 타로 한 장")
st.caption("고민을 한 줄 적고 카드를 뽑으세요. 메이저 아르카나 22장 중 한 장이 나옵니다.")

concern = st.text_input(
    "오늘의 고민",
    placeholder="예: 지금 벌인 일을 계속 끌고 가도 될까?",
)

if st.button("카드 뽑기", type="primary"):
    if not concern.strip():
        st.warning("고민을 한 줄 적어주세요.")
        st.stop()

    card = random.choice(MAJOR_ARCANA)
    orientation = random.choice(["정방향", "역방향"])
    st.markdown(f"### 뽑힌 카드 — {card} · {orientation}")

    api_key = get_api_key()
    if not api_key:
        # 키가 없으면 조용히 더미를 주지 않고 명확히 멈춘다
        st.error(
            "ANTHROPIC_API_KEY가 설정되지 않았습니다.\n\n"
            "- 로컬: 터미널에서 `export ANTHROPIC_API_KEY=sk-...` 후 다시 실행\n"
            "- 배포: Streamlit Cloud의 Secrets에 `ANTHROPIC_API_KEY` 추가"
        )
        st.stop()

    with st.spinner("카드를 읽는 중..."):
        reading = read_card(concern, card, orientation, api_key)

    st.write(reading)

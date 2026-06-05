# 타로 한 장

고민을 한 줄 적으면 메이저 아르카나 22장 중 한 장을 뽑아 Claude가 해석해주는 작은 웹 앱.

## 로컬 실행

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # 또는 .streamlit/secrets.toml 에 저장
streamlit run app.py
```

## 배포 (Streamlit Community Cloud)

1. 이 repo를 GitHub에 push
2. share.streamlit.io 에서 repo 연결
3. App settings → Secrets 에 `ANTHROPIC_API_KEY` 추가

## 구조

- `app.py` — 전체 앱 (입력 → 카드 뽑기 → LLM 해석)
- 카드: 메이저 아르카나 22장, 정/역방향 랜덤
- 모델: claude-haiku-4-5

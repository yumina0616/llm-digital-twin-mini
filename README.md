# 🏗️ LLM-based Structural Digital Twin

자연어로 된 구조 문제를 해석하여 물리 기반 시뮬레이션을 수행하고 결과를 시각화합니다.

---

## 📌 프로젝트 배경

현재 디지털 트윈, LLM 에이전트, 물리정보 기반 AI에 관심을 가지고 있습니다.

사용자가 자연어로 구조 문제를 입력하면 이를 공학 파라미터로 변환하고 간단한 물리 시뮬레이션을 수행한 뒤 결과를 시각화하는 미니 프로젝트를 진행했습니다.

- 소프트웨어가 자연어 입력을 공학적 파라미터로 해석하고 시뮬레이션 할 수 있도록,
- 물리 기반 계산을 자동화된 시스템을 이용하여 쉽게 해결할 수 있도록,
- 사람이 직접 수식을 넣지 않아도 기본적인 공학 시뮬레이션이 돌아가도록,
만든 것이 이번 프로젝트의 핵심 목표입니다.

---

## 🖥️ 데모

![demo1](examples/demo1.png)
![demo2](examples/demo2.png)

---

## ⚙️ 시스템 구조
```
자연어 입력
→ 규칙 기반 파서 (1차)
→ LLM 파서 (2차, 규칙 기반 실패 시)
→ 파라미터 추출 (길이 / 하중 / 재료 / 하중 조건)
→ Beam 시뮬레이션
→ 그래프 + 수치 출력
```

---

## 🔧 주요 기능

- 자연어 입력 해석 (한국어 / 영어 지원)
- 규칙 기반 파서 + LLM 파서 이중 구조
- 재료 데이터베이스 (강철 / 알루미늄 / 탄소섬유 / 콘크리트)
- 하중 조건 선택 (중앙 집중하중 / 분포하중 / 외팔보)
- 변위 그래프 및 최대 변위 수치 출력
- 재료별 변위 비교 그래프
- Streamlit 웹 인터페이스

---

## 🧱 기술 스택

- Python
- NumPy, Matplotlib
- OpenAI API (gpt-4o-mini)
- python-dotenv
- Streamlit

---

## 🚀 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

프로젝트 루트에 `.env` 파일 생성:
```
OPENAI_API_KEY=your_api_key_here
```

### 3. 웹 인터페이스 실행
```bash
streamlit run app.py
```

### 4. 터미널 실행
```bash
python main.py
```

---

## 💬 입력 예시
```
길이 1m 강철 보에 1000N 중앙 하중을 가하면?
2m 알루미늄 외팔보에 500N을 가했을 때
3m 콘크리트 보에 200N 분포하중
2미터짜리 보에 5 킬로뉴턴을 가했을 때  ← LLM 파서 처리
```

---

## 📁 프로젝트 구조
```
llm-digital-twin-mini/
│
├── app.py               # Streamlit 웹 인터페이스
├── main.py              # 터미널 실행 진입점
├── requirements.txt
│
├── src/
│   ├── beam.py          # 물리 시뮬레이션 (중앙하중 / 분포하중 / 외팔보)
│   ├── materials.py     # 재료 데이터베이스
│   ├── parser.py        # 규칙 기반 파서
│   └── llm_parser.py    # LLM 기반 파서
│
└── examples/
    └── demo.png         # 실행 결과 스크린샷
```

---

## 🔮 향후 확장 방향

- Spring-mass 진동 모델 추가
- 단면 조건 입력 지원 (원형 / 사각형)
- Surrogate model 및 virtual sensing 연구로 확장
- 3D 시각화 추가
- Multi-agent 구조로 확장
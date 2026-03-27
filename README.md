# LLM-based Physics-informed Digital Twin Mini Project

자연어로 입력된 구조 문제를 해석하여 물리 기반 시뮬레이션을 수행하고 결과를 시각화하는 프로젝트입니다.

---

## 프로젝트 배경

디지털 트윈, LLM 에이전트, 물리정보 기반 AI에 관심을 가지고,  
이를 축소된 형태의 개인 프로젝트로 직접 구현해보는 것을 목표로 합니다.

사용자가 자연어로 구조 문제를 입력하면,  
시스템은 이를 공학 파라미터로 변환하고 간단한 물리 시뮬레이션을 수행한 뒤 결과를 시각화합니다.

---

## 시스템 구조
```
자연어 입력
→ 규칙 기반 파서 (1차)
→ LLM 파서 (2차, 규칙 기반 실패 시)
→ Beam 시뮬레이션
→ 그래프 + 수치 출력
```

---

## 주요 기능

- 자연어 입력 해석 (한국어 지원)
- 규칙 기반 파서와 LLM 파서 이중 구조
- Simply supported beam 변위 계산
- 변위 그래프 및 최대 변위 수치 출력

---

## 기술 스택

- Python
- NumPy, Matplotlib
- OpenAI API (gpt-4o-mini)
- python-dotenv

---

## 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

프로젝트 루트에 `.env` 파일 생성:
```
OPENAI_API_KEY=your_api_key_here
```

### 3. 실행
```bash
python main.py
```

---

## 입력 예시
```
길이 1m 보에 1000N 하중을 가하면 어떻게 돼?
2미터짜리 보에 5 킬로뉴턴을 가했을 때
length 1.5m force 800N
```

---

## 출력 예시

- 변위 그래프 (mm 단위)
- 최대 변위 수치 출력

---

## 향후 확장 방향

- Spring-mass 진동 모델 추가
- 재료 및 단면 조건 입력 지원
- Streamlit UI 추가
- Surrogate model 및 virtual sensing 연구로 확장
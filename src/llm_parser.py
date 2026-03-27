import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_input_llm(text):
    """
    LLM을 사용해 자연어에서 length, force 추출

    Returns:
        dict: {"length": float, "force": float}
        또는 None (추출 실패 시)
    """
    prompt = f"""
다음 문장에서 보(beam)의 길이와 하중을 추출해줘.
반드시 아래 JSON 형식으로만 답해. 다른 말은 하지 마.

{{"length": 길이(m, float), "force": 하중(N, float)}}

추출할 수 없으면 이렇게 답해:
{{"error": "추출 실패 이유"}}

문장: {text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
        if "error" in result:
            print(f"추출 실패: {result['error']}")
            return None
        return result
    except json.JSONDecodeError:
        print(f"JSON 파싱 실패: {content}")
        return None


if __name__ == "__main__":
    tests = [
        "길이 1m 보에 1000N 하중을 가하면 어떻게 돼?",
        "2미터짜리 보에 5 킬로뉴턴을 가했을 때",
        "보에 하중을 가하면?",
    ]

    for t in tests:
        print(f"\n입력: {t}")
        print(f"결과: {parse_input_llm(t)}")
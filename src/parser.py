import re


def parse_input(text):
    """
    자연어 문장에서 length, force 추출
    
    Examples:
        "길이 1m 보에 1000N 하중을 가하면"
        "2m 길이의 보에 500N을 가했을 때"
        "length 1.5m force 800N"
    
    Returns:
        dict: {"length": float, "force": float}
        또는 None (추출 실패 시)
    """
    result = {}

    # 길이 추출: 숫자 + m
    length_match = re.search(r'(\d+\.?\d*)\s*m', text)
    if length_match:
        result["length"] = float(length_match.group(1))

    # 하중 추출: 숫자 + N
    force_match = re.search(r'(\d+\.?\d*)\s*[nN]', text)
    if force_match:
        result["force"] = float(force_match.group(1))

    # 둘 다 추출됐는지 확인
    if "length" in result and "force" in result:
        return result
    
    # 실패 시 어떤 값이 빠졌는지 알려줌
    missing = []
    if "length" not in result:
        missing.append("길이")
    if "force" not in result:
        missing.append("하중")
    
    print(f"다음 정보를 찾을 수 없었어요: {', '.join(missing)}")
    return None


if __name__ == "__main__":
    tests = [
        "길이 1m 보에 1000N 하중을 가하면 어떻게 돼?",
        "2m 길이의 보에 500N을 가했을 때",
        "length 1.5m force 800N",
        "보에 하중을 가하면?",  # 실패 케이스
    ]

    for t in tests:
        print(f"\n입력: {t}")
        print(f"결과: {parse_input(t)}")
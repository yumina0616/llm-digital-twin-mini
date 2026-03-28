import re
from src.materials import MATERIALS, MATERIAL_ALIASES


def parse_input(text):
    """
    자연어 문장에서 length, force, material 추출

    Examples:
        "길이 1m 강철 보에 1000N 하중을 가하면"
        "2m 알루미늄 보에 500N을 가했을 때"

    Returns:
        dict: {"length": float, "force": float, "material": str(optional)}
        또는 None (추출 실패 시)
    """
    result = {}

    # 길이 추출
    length_match = re.search(r'(\d+\.?\d*)\s*m', text)
    if length_match:
        result["length"] = float(length_match.group(1))

    # 하중 추출
    force_match = re.search(r'(\d+\.?\d*)\s*[nN]', text)
    if force_match:
        result["force"] = float(force_match.group(1))

    # 재료 추출 (한국어)
    for name in MATERIALS:
        if name in text:
            result["material"] = name
            break

    # 재료 추출 (영어)
    if "material" not in result:
        for alias in MATERIAL_ALIASES:
            if alias in text.lower():
                result["material"] = MATERIAL_ALIASES[alias]
                break

    # 필수값 확인
    missing = []
    if "length" not in result:
        missing.append("길이")
    if "force" not in result:
        missing.append("하중")

    if missing:
        print(f"다음 정보를 찾을 수 없었어요: {', '.join(missing)}")
        return None

    return result


if __name__ == "__main__":
    tests = [
        "길이 1m 강철 보에 1000N 하중을 가하면?",
        "2m 알루미늄 보에 500N을 가했을 때",
        "length 1.5m force 800N",  # 재료 없는 경우
        "보에 하중을 가하면?",     # 실패 케이스
    ]

    for t in tests:
        print(f"\n입력: {t}")
        print(f"결과: {parse_input(t)}")
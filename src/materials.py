# 재료별 탄성계수 데이터베이스 (단위: Pa)
MATERIALS = {
    "강철": {
        "E": 200e9,
        "density": 7850,
        "description": "Steel"
    },
    "알루미늄": {
        "E": 69e9,
        "density": 2700,
        "description": "Aluminum"
    },
    "탄소섬유": {
        "E": 150e9,
        "density": 1600,
        "description": "Carbon Fiber"
    },
    "콘크리트": {
        "E": 30e9,
        "density": 2400,
        "description": "Concrete"
    },
}

# 영어 키워드 매핑
MATERIAL_ALIASES = {
    "steel": "강철",
    "aluminum": "알루미늄",
    "aluminium": "알루미늄",
    "carbon fiber": "탄소섬유",
    "concrete": "콘크리트",
}


def get_material(name):
    """
    재료 이름으로 탄성계수 반환
    
    Returns:
        dict: 재료 정보
        또는 None (없는 재료)
    """
    # 한국어 직접 검색
    if name in MATERIALS:
        return MATERIALS[name]
    
    # 영어 aliases 검색
    english_key = MATERIAL_ALIASES.get(name.lower())
    if english_key:
        return MATERIALS[english_key]
    
    return None


def list_materials():
    """사용 가능한 재료 목록 출력"""
    print("사용 가능한 재료:")
    for name, props in MATERIALS.items():
        print(f"  - {name} ({props['description']}): E = {props['E']:.2e} Pa")


if __name__ == "__main__":
    list_materials()
    print()
    print(get_material("강철"))
    print(get_material("aluminum"))
    print(get_material("티타늄"))  # 없는 재료
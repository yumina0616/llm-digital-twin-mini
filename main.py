from src.beam import calculate_beam_deflection, plot_deflection
from src.parser import parse_input
from src.llm_parser import parse_input_llm
from src.materials import get_material


def run(params, I=8.33e-6):
    length = params["length"]
    force = params["force"]

    # 재료 설정
    material_name = params.get("material", "강철")  # 기본값 강철
    material = get_material(material_name)

    if material is None:
        print(f"'{material_name}' 재료를 찾을 수 없어요. 강철로 대체합니다.")
        material = get_material("강철")

    E = material["E"]
    print(f"재료: {material_name} (E = {E:.2e} Pa)")

    x, y = calculate_beam_deflection(length, force, E, I)
    plot_deflection(x, y, length, force, save_path="examples/output.png")
    print(f"최대 변위: {min(y) * 1000:.4f} mm")


if __name__ == "__main__":
    user_input = input("문제를 입력하세요: ")

    # 1차: 규칙 기반 파서
    params = parse_input(user_input)

    # 2차: 규칙 기반 실패 시 LLM 파서
    if params is None:
        print("규칙 기반 파서 실패 → LLM 파서 시도 중...")
        params = parse_input_llm(user_input)

    if params:
        run(params)
    else:
        print("입력을 다시 확인해주세요.")

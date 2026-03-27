from src.beam import calculate_beam_deflection, plot_deflection
from src.parser import parse_input


def run(params, E=200e9, I=8.33e-6):
    length = params["length"]
    force = params["force"]
    x, y = calculate_beam_deflection(length, force, E, I)
    plot_deflection(x, y, length, force)
    print(f"최대 변위: {min(y) * 1000:.4f} mm")


if __name__ == "__main__":
    user_input = input("문제를 입력하세요: ")
    
    params = parse_input(user_input)
    
    if params:
        run(params)
    else:
        print("입력을 다시 확인해주세요.")
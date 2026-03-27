import numpy as np
import matplotlib.pyplot as plt


def calculate_beam_deflection(length, force, E, I, num_points=100):
    """
    Simply supported beam, 중앙 집중하중 조건에서 변위 계산
    
    Parameters:
        length  : 보의 길이 (m)
        force   : 중앙 집중하중 (N)
        E       : 탄성계수 (Pa)
        I       : 단면 2차 모멘트 (m^4)
        num_points : 계산할 점의 수
    
    Returns:
        x : 위치 배열
        y : 변위 배열 (아래 방향이 음수)
    """
    x = np.linspace(0, length, num_points)
    L = length
    P = force
    y = np.zeros_like(x)

    for i, xi in enumerate(x):
        if xi <= L / 2:
            y[i] = (P * xi) / (48 * E * I) * (3 * L**2 - 4 * xi**2)
        else:
            y[i] = (P * (L - xi)) / (48 * E * I) * (3 * L**2 - 4 * (L - xi)**2)

    return x, -y  # 아래 방향을 음수로 표현


def plot_deflection(x, y, length, force):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y * 1000, color='steelblue', linewidth=2)  # mm 단위로 변환
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title(f'Beam Deflection (L={length}m, F={force}N)')
    plt.xlabel('Position (m)')
    plt.ylabel('Deflection (mm)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 테스트용 기본값
    length = 1.0       # 1m
    force = 1000       # 1000N
    E = 200e9          # 강철 탄성계수 (Pa)
    I = 8.33e-6        # 단면 2차 모멘트 (m^4)

    x, y = calculate_beam_deflection(length, force, E, I)
    plot_deflection(x, y, length, force)

    max_deflection = min(y)
    print(f"최대 변위: {max_deflection * 1000:.4f} mm")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False


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


def plot_deflection(x, y, length, force, save_path=None):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y * 1000, color='steelblue', linewidth=2)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title(f'Beam Deflection (L={length}m, F={force}N)')
    plt.xlabel('Position (m)')
    plt.ylabel('Deflection (mm)')
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"그래프 저장됨: {save_path}")

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

def plot_comparison(length, force, I=8.33e-6, save_path=None):
    """
    재료별 변위 비교 그래프
    """
    from src.materials import MATERIALS

    plt.figure(figsize=(10, 5))

    for name, props in MATERIALS.items():
        E = props["E"]
        x, y = calculate_beam_deflection(length, force, E, I)
        plt.plot(x, y * 1000, linewidth=2, label=f"{name} (E={E:.2e})")

    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title(f'재료별 변위 비교 (L={length}m, F={force}N)')
    plt.xlabel('Position (m)')
    plt.ylabel('Deflection (mm)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        print(f"그래프 저장됨: {save_path}")

    plt.show()

def calculate_distributed_load(length, w, E, I, num_points=100):
    """
    Simply supported beam, 균일 분포하중
    
    Parameters:
        w : 단위길이당 하중 (N/m)
    """
    x = np.linspace(0, length, num_points)
    L = length
    y = (w * x) / (24 * E * I) * (L**3 - 2 * L * x**2 + x**3)
    return x, -y


def calculate_cantilever(length, force, E, I, num_points=100):
    """
    외팔보(cantilever), 자유단 집중하중
    """
    x = np.linspace(0, length, num_points)
    L = length
    P = force
    y = (P * x**2) / (6 * E * I) * (3 * L - x)
    return x, -y
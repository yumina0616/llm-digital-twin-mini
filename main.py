from src.beam import calculate_beam_deflection, plot_deflection


def run(length, force, E=200e9, I=8.33e-6):
    x, y = calculate_beam_deflection(length, force, E, I)
    plot_deflection(x, y, length, force)
    print(f"최대 변위: {min(y) * 1000:.4f} mm")


if __name__ == "__main__":
    run(length=1.0, force=1000)
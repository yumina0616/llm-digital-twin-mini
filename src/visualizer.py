import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import platform
import plotly.graph_objects as go

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def draw_beam_diagram(x, y, length, force, load_type, material_name, max_deflection):
    """
    보 변형 다이어그램 그리기
    - 원래 보 위치 (점선)
    - 변형된 보 (실선, 색상)
    - 지지점, 하중 화살표
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 7))

    # ── 상단: 보 다이어그램 ──
    ax1 = axes[0]

    # 원래 보 (점선)
    ax1.plot([0, length], [0, 0], 'k--', linewidth=1.5, label='원래 위치', alpha=0.5)

    # 변형된 보 (색상)
    ax1.plot(x, y * 1000, color='steelblue', linewidth=3, label='변형된 보')

    # 변형 영역 채우기
    ax1.fill_between(x, y * 1000, 0, alpha=0.1, color='steelblue')

    # 하중 화살표
    if load_type == "center":
        ax1.annotate('', xy=(length/2, min(y)*1000*0.3),
                    xytext=(length/2, max(abs(min(y)*1000))*1.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax1.text(length/2, max(abs(min(y)*1000))*1.7, f'{force}N',
                ha='center', color='red', fontsize=10, fontweight='bold')

    elif load_type == "distributed":
        for xi in np.linspace(0.1, length-0.1, 8):
            ax1.annotate('', xy=(xi, min(y)*1000*0.3),
                        xytext=(xi, max(abs(min(y)*1000))*1.2),
                        arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
        ax1.text(length/2, max(abs(min(y)*1000))*1.5, f'분포하중 {force}N/m',
                ha='center', color='red', fontsize=10, fontweight='bold')

    elif load_type == "cantilever":
        y_max = float(max(abs(y * 1000)))
        ax1.annotate('', xy=(length, float(min(y * 1000)) * 0.3),
                    xytext=(length, y_max * 1.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax1.text(length, y_max * 1.7, f'{force}N',
                ha='center', color='red', fontsize=10, fontweight='bold')

    # 지지점 표시
    y_max = float(max(abs(y * 1000)))
    if load_type == "cantilever":
        ax1.add_patch(plt.Rectangle((-length*0.03, -y_max*0.5),
                                   length*0.03, y_max*1.0,
                                   color='gray', zorder=5))
        ax1.text(-length*0.05, 0, '고정단', ha='right', va='center',
                fontsize=9, color='gray')
    else:
        triangle_l = plt.Polygon([[0, 0], [-length*0.03, -y_max*0.4],
                                  [length*0.03, -y_max*0.4]],
                                 color='gray', zorder=5)
        triangle_r = plt.Polygon([[length, 0],
                                  [length-length*0.03, -y_max*0.4],
                                  [length+length*0.03, -y_max*0.4]],
                                 color='gray', zorder=5)
        ax1.add_patch(triangle_l)
        ax1.add_patch(triangle_r)

    ax1.set_title(f'보 변형 다이어그램 | {material_name} | {load_type}', fontsize=13)
    ax1.set_xlabel('위치 (m)')
    ax1.set_ylabel('변위 (mm)')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # ── 하단: 변위 분포 heatmap ──
    ax2 = axes[1]
    deflection_2d = np.tile(y * 1000, (20, 1))
    im = ax2.imshow(deflection_2d, aspect='auto', cmap='RdYlBu_r',
                   extent=[0, length, 0, 1])
    plt.colorbar(im, ax=ax2, label='변위 (mm)')
    ax2.set_title('변위 분포 Heatmap')
    ax2.set_xlabel('위치 (m)')
    ax2.set_yticks([])

    plt.tight_layout()
    return fig


def draw_safety_gauge(max_deflection, length, allowable_ratio=1/300):
    """
    안전성 게이지
    허용 변위 = L/300 (일반적인 구조 기준)
    """
    allowable = length / allowable_ratio / 1000 * 1000  # mm
    allowable_mm = length * 1000 / 300  # mm

    ratio = abs(max_deflection) / allowable_mm

    if ratio < 0.7:
        status = "✅ 안전"
        color = "green"
    elif ratio < 1.0:
        status = "⚠️ 주의"
        color = "orange"
    else:
        status = "❌ 위험"
        color = "red"

    return status, color, allowable_mm, ratio


def draw_3d_beam(x, y, length, force, load_type, material_name):
    """
    Plotly 3D 보 변형 시각화
    """
    # 보의 두께 표현을 위한 y축 확장
    width = np.linspace(-0.05, 0.05, 10)
    X, W = np.meshgrid(x, width)
    Z = np.tile(y * 1000, (10, 1))  # 변위 (mm)
    Y = np.zeros_like(X)  # 보의 높이

    fig = go.Figure()

    # 변형된 보 surface
    fig.add_trace(go.Surface(
        x=X,
        y=W,
        z=Z,
        colorscale='RdYlBu_r',
        showscale=True,
        colorbar=dict(title='변위 (mm)'),
        opacity=0.9,
        name='변형된 보'
    ))

    # 원래 보 위치 (투명한 회색)
    Z_original = np.zeros_like(Z)
    fig.add_trace(go.Surface(
        x=X,
        y=W,
        z=Z_original,
        colorscale=[[0, 'gray'], [1, 'gray']],
        showscale=False,
        opacity=0.2,
        name='원래 위치'
    ))

    # 하중 화살표
    if load_type == "center":
        arrow_x = length / 2
    elif load_type == "cantilever":
        arrow_x = length
    else:
        arrow_x = length / 2

    fig.add_trace(go.Scatter3d(
        x=[arrow_x, arrow_x],
        y=[0, 0],
        z=[max(abs(y * 1000)) * 2, max(abs(y * 1000)) * 0.5],
        mode='lines+text',
        line=dict(color='red', width=6),
        text=[f'{force}N', ''],
        textposition='top center',
        name='하중'
    ))

    fig.update_layout(
        title=f'3D 보 변형 시각화 | {material_name} | {load_type}',
        scene=dict(
            xaxis_title='위치 (m)',
            yaxis_title='폭 (m)',
            zaxis_title='변위 (mm)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.0)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        height=550,
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig
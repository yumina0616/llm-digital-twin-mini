import streamlit as st
import matplotlib.pyplot as plt
from src.beam import (
    calculate_beam_deflection,
    calculate_distributed_load,
    calculate_cantilever,
    plot_comparison
)
from src.parser import parse_input
from src.llm_parser import parse_input_llm
from src.materials import get_material, list_materials, MATERIALS

st.set_page_config(page_title="Digital Twin Mini", layout="wide")
st.title("🏗️ LLM-based Structural Digital Twin")
st.markdown("자연어로 구조 문제를 입력하면 시뮬레이션 결과를 보여줍니다.")

# 사이드바
st.sidebar.header("⚙️ 설정")
I = st.sidebar.number_input("단면 2차 모멘트 I (m⁴)", value=8.33e-6, format="%.2e")
show_comparison = st.sidebar.checkbox("재료별 비교 그래프 보기", value=False)

st.markdown("---")

# 입력
user_input = st.text_input(
    "문제를 입력하세요",
    placeholder="예: 2m 알루미늄 외팔보에 500N을 가했을 때"
)

if st.button("시뮬레이션 실행") and user_input:
    with st.spinner("분석 중..."):
        # 파서
        params = parse_input(user_input)
        if params is None:
            st.info("규칙 기반 파서 실패 → LLM 파서 시도 중...")
            params = parse_input_llm(user_input)

    if params is None:
        st.error("입력에서 필요한 정보를 찾을 수 없어요. 길이와 하중을 포함해 입력해주세요.")
    else:
        length = params["length"]
        force = params["force"]
        load_type = params.get("load_type", "center")
        material_name = params.get("material", "강철")

        material = get_material(material_name)
        if material is None:
            st.warning(f"'{material_name}' 재료를 찾을 수 없어요. 강철로 대체합니다.")
            material_name = "강철"
            material = get_material("강철")

        E = material["E"]

        # 파라미터 요약
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("길이", f"{length} m")
        col2.metric("하중", f"{force} N")
        col3.metric("재료", material_name)
        col4.metric("하중 조건", load_type)

        st.markdown("---")

        # 계산
        if load_type == "center":
            x, y = calculate_beam_deflection(length, force, E, I)
        elif load_type == "distributed":
            x, y = calculate_distributed_load(length, force, E, I)
        elif load_type == "cantilever":
            x, y = calculate_cantilever(length, force, E, I)
        else:
            x, y = calculate_beam_deflection(length, force, E, I)

        max_deflection = min(y) * 1000

        # 결과 그래프
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("변위 그래프")
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(x, y * 1000, color='steelblue', linewidth=2)
            ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            ax.set_title(f'Beam Deflection (L={length}m, F={force}N)')
            ax.set_xlabel('Position (m)')
            ax.set_ylabel('Deflection (mm)')
            ax.grid(True)
            st.pyplot(fig)

        with col_right:
            st.subheader("결과 요약")
            st.metric("최대 변위", f"{max_deflection:.4f} mm")
            st.metric("탄성계수 E", f"{E:.2e} Pa")
            st.metric("단면 2차 모멘트 I", f"{I:.2e} m⁴")

        # 재료 비교 그래프
        if show_comparison:
            st.markdown("---")
            st.subheader("재료별 변위 비교")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            for name, props in MATERIALS.items():
                E_comp = props["E"]
                if load_type == "center":
                    xc, yc = calculate_beam_deflection(length, force, E_comp, I)
                elif load_type == "distributed":
                    xc, yc = calculate_distributed_load(length, force, E_comp, I)
                elif load_type == "cantilever":
                    xc, yc = calculate_cantilever(length, force, E_comp, I)
                else:
                    xc, yc = calculate_beam_deflection(length, force, E_comp, I)
                ax2.plot(xc, yc * 1000, linewidth=2, label=f"{name} (E={E_comp:.2e})")
            ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
            ax2.set_title(f'재료별 변위 비교 (L={length}m, F={force}N)')
            ax2.set_xlabel('Position (m)')
            ax2.set_ylabel('Deflection (mm)')
            ax2.legend()
            ax2.grid(True)
            st.pyplot(fig2)
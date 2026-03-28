import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from src.beam import (
    calculate_beam_deflection,
    calculate_distributed_load,
    calculate_cantilever,
)
from src.parser import parse_input
from src.llm_parser import parse_input_llm
from src.materials import get_material, MATERIALS
from src.visualizer import draw_beam_diagram, draw_safety_gauge, draw_3d_beam

st.set_page_config(page_title="Structural Digital Twin", layout="wide")

# 헤더
st.title("🏗️ Structural Digital Twin")
st.markdown("자연어로 구조 문제를 입력하면 시뮬레이션 결과를 보여줍니다.")
st.markdown("---")

# 사이드바
st.sidebar.header("⚙️ 고급 설정")
I = st.sidebar.number_input("단면 2차 모멘트 I (m⁴)", value=8.33e-6, format="%.2e")
show_comparison = st.sidebar.checkbox("재료별 비교 그래프", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("**입력 예시**")
st.sidebar.code("2m 알루미늄 외팔보에 500N")
st.sidebar.code("길이 1m 강철 보에 1000N 중앙 하중")
st.sidebar.code("3m 콘크리트 보에 200N 분포하중")

# 입력
user_input = st.text_input(
    "🔍 문제를 입력하세요",
    placeholder="예: 2m 알루미늄 외팔보에 500N을 가했을 때"
)

run_button = st.button("⚡ 시뮬레이션 실행", use_container_width=True)

if run_button and user_input:
    with st.spinner("분석 중..."):
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
        status, color, allowable_mm, ratio = draw_safety_gauge(
            max_deflection, length
        )

        st.markdown("---")

        # 파라미터 요약
        st.subheader("📋 입력 파라미터")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("길이", f"{length} m")
        col2.metric("하중", f"{force} N")
        col3.metric("재료", material_name)
        col4.metric("하중 조건", load_type)

        st.markdown("---")

        # 결과 요약
        st.subheader("📊 결과 요약")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("최대 변위", f"{abs(max_deflection):.4f} mm")
        col_b.metric("허용 변위 (L/300)", f"{allowable_mm:.4f} mm")
        col_c.metric("안전성", status)

        # 안전성 프로그레스 바
        st.markdown(f"**안전성 비율: {ratio*100:.1f}%** (100% 초과 시 위험)")
        st.progress(min(ratio, 1.0))

        # 결과 해석 텍스트
        st.markdown("---")
        st.subheader("🔍 결과 해석")
        if ratio < 0.7:
            st.success(f"""
            현재 최대 변위는 **{abs(max_deflection):.4f} mm**로,
            허용 변위 기준({allowable_mm:.4f} mm)의 **{ratio*100:.1f}%** 수준입니다.
            구조적으로 **안전한 범위**에 있습니다.
            """)
        elif ratio < 1.0:
            st.warning(f"""
            현재 최대 변위는 **{abs(max_deflection):.4f} mm**로,
            허용 변위 기준({allowable_mm:.4f} mm)의 **{ratio*100:.1f}%** 수준입니다.
            허용 기준에 근접하고 있습니다. **재료 또는 단면 변경을 검토하세요.**
            """)
        else:
            st.error(f"""
            현재 최대 변위는 **{abs(max_deflection):.4f} mm**로,
            허용 변위 기준({allowable_mm:.4f} mm)을 **초과**했습니다.
            **구조 설계를 재검토해야 합니다.**
            """)

        st.markdown("---")

        # 보 다이어그램
        st.subheader("📐 보 변형 다이어그램")
        fig = draw_beam_diagram(x, y, length, force, load_type, material_name, max_deflection)
        st.pyplot(fig)

        # 재료 비교
        if show_comparison:
            st.markdown("---")
            st.subheader("🔬 재료별 변위 비교")
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
            ax2.set_xlabel('위치 (m)')
            ax2.set_ylabel('변위 (mm)')
            ax2.legend()
            ax2.grid(True)
            st.pyplot(fig2)

        # 3D 시각화 (항상 표시)
        st.markdown("---")
        st.subheader("🌐 3D 보 변형 시각화")
        fig3d = draw_3d_beam(x, y, length, force, load_type, material_name)
        st.plotly_chart(fig3d, use_container_width=True)
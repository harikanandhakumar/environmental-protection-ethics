import streamlit as st

import assessment_dashboard
import biodiversity_map
import corridor_designer
import design_studio
import ethics_challenge
import ethics_lab
import impact_simulator
from data_models import SECTIONS
from styles import get_asset_path, inject_custom_css

PROJECT_TITLE = (
    "Environmental Protection Ethics in Future-Proof Engineering "
    "for Biodiversity, Climate and Pollution Prevention"
)

SECTION_RENDERERS = {
    SECTIONS[0]: biodiversity_map.render,
    SECTIONS[1]: impact_simulator.render,
    SECTIONS[2]: ethics_lab.render,
    SECTIONS[3]: corridor_designer.render,
    SECTIONS[4]: assessment_dashboard.render,
    SECTIONS[5]: design_studio.render,
    SECTIONS[6]: ethics_challenge.render,
}


def _go_prev() -> None:
    idx = SECTIONS.index(st.session_state["nav_radio"])
    if idx > 0:
        st.session_state["nav_radio"] = SECTIONS[idx - 1]


def _go_next() -> None:
    idx = SECTIONS.index(st.session_state["nav_radio"])
    if idx < len(SECTIONS) - 1:
        st.session_state["nav_radio"] = SECTIONS[idx + 1]


def main() -> None:
    st.set_page_config(
        page_title="Environmental Protection Ethics | Future-Proof Engineering",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_custom_css()

    if "nav_radio" not in st.session_state:
        st.session_state["nav_radio"] = SECTIONS[0]
    if "visited_sections" not in st.session_state:
        st.session_state["visited_sections"] = set()

    with st.sidebar:
        st.markdown("### 🌿 Engineering Ethics Hub")
        st.caption("Interactive Simulation & Stewardship Workbench")

        selected = st.radio(
            "Navigate Simulation Sections",
            SECTIONS,
            key="nav_radio",
        )
        st.session_state["visited_sections"].add(selected)

        visited_count = len(st.session_state["visited_sections"])
        st.markdown("---")
        st.markdown(f"**Exploration Progress:** {visited_count} / {len(SECTIONS)} sections")
        st.progress(visited_count / len(SECTIONS))

        st.markdown("#### Quick Section Jump")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.button(
                "← Previous",
                width="stretch",
                disabled=(SECTIONS.index(selected) == 0),
                on_click=_go_prev,
                key="btn_prev_sec",
            )
        with b_col2:
            st.button(
                "Next →",
                width="stretch",
                disabled=(SECTIONS.index(selected) == len(SECTIONS) - 1),
                on_click=_go_next,
                key="btn_next_sec",
            )

        st.markdown("---")
        st.markdown(
            "**Core Ethical Pillars**\n"
            "- Precautionary Pollution Prevention\n"
            "- Biodiversity Mitigation Hierarchy\n"
            "- Climate Non-Stationarity Resilience\n"
            "- Intergenerational & Community Equity"
        )

    # Top Hero Header with integrated visual showcase
    hero_text_col, hero_img_col = st.columns([1.45, 1.0], gap="medium")
    with hero_text_col:
        st.markdown(
            f"""
            <div class="hero-card" style="height:100%;">
                <div class="hero-kicker">Interactive Environmental Engineering Simulation Platform</div>
                <div class="hero-title">{PROJECT_TITLE}</div>
                <p class="hero-sub">
                    Simulate ecological trade-offs, design wildlife corridors, audit engineering ethics dilemmas,
                    and configure net-positive sustainable infrastructure across seven interactive modules.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hero_img_col:
        st.image(
            get_asset_path("hero_banner.png"),
            caption="Future-proof infrastructure: wildlife eco-duct, clean rail, solar microgrid & wetlands",
            width="stretch",
        )

    with st.expander("Section Directory & Exploration Status", expanded=False):
        cols = st.columns(2)
        for idx, sec in enumerate(SECTIONS):
            marker = "✅" if sec in st.session_state["visited_sections"] else "▫️"
            cols[idx % 2].markdown(f"{marker} **{sec}**")

    # Render selected section
    SECTION_RENDERERS[selected]()

    st.markdown("---")
    st.caption(
        "Environmental Protection Ethics in Future-Proof Engineering for Biodiversity, Climate and Pollution Prevention "
        "| Built with Python, Streamlit & Plotly."
    )


if __name__ == "__main__":
    main()

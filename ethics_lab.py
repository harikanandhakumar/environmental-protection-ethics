import plotly.graph_objects as go
import streamlit as st

from data_models import ETHICAL_DILEMMAS
from styles import (
    apply_plotly_theme,
    get_asset_path,
    render_kpi_card,
    render_section_header,
)


def render() -> None:
    render_section_header(
        "Section 3 — Ethical Decision-Making Lab",
        "Evaluate real-world civil and environmental engineering dilemmas across normative ethics lenses, stakeholder priorities, and ecological outcomes.",
        badge_text="Normative Ethics & Stakeholder Analysis",
    )

    top_img, top_intro = st.columns([1.15, 1.85], gap="large")
    with top_img:
        st.image(
            get_asset_path("ethics_compass.png"),
            caption="Environmental engineering ethical compass balancing biosphere, climate, and equity",
            width="stretch",
        )
    with top_intro:
        dilemma_titles = [d["title"] for d in ETHICAL_DILEMMAS]
        chosen_title = st.selectbox("Select Engineering Dilemma Scenario", dilemma_titles, key="eth_case")
        dilemma = next(d for d in ETHICAL_DILEMMAS if d["title"] == chosen_title)
        st.markdown(
            f"""
            <div class="info-panel">
                <h4 style="margin:0 0 0.4rem 0; color:#064E3B;">Scenario Brief</h4>
                <p style="margin:0; line-height:1.55;">{dilemma['context']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Step 1: Set Ethical Priority Weights & Choose Design Alternative")
    w_col, opt_col = st.columns([1.1, 1.4], gap="large")

    with w_col:
        w_prec = st.slider("Precautionary Principle Weight", 1, 5, 4, key="eth_w_prec")
        w_inter = st.slider("Intergenerational Climate Justice Weight", 1, 5, 4, key="eth_w_inter")
        w_eco = st.slider("Ecological Integrity & Non-Human Life Weight", 1, 5, 5, key="eth_w_eco")
        w_just = st.slider("Community & Environmental Justice Weight", 1, 5, 4, key="eth_w_just")
        w_int = st.slider("Professional & Scientific Integrity Weight", 1, 5, 5, key="eth_w_int")

    with opt_col:
        option_names = list(dilemma["options"].keys())
        selected_opt = st.radio(
            "Select Proposed Engineering Course of Action",
            option_names,
            index=1,
            key="eth_opt",
        )
        opt = dilemma["options"][selected_opt]

        weights = [w_prec, w_inter, w_eco, w_just, w_int]
        scores = [
            opt["precautionary"],
            opt["intergenerational"],
            opt["ecological"],
            opt["justice"],
            opt["integrity"],
        ]
        weighted_index = sum(w * s for w, s in zip(weights, scores)) / sum(weights)

        if weighted_index >= 82:
            tier = "Exemplary Ethical Stewardship"
            badge_cls = "badge-green"
        elif weighted_index >= 60:
            tier = "Acceptable with Residual Risks"
            badge_cls = "badge-amber"
        else:
            tier = "Ethically Non-Compliant"
            badge_cls = "badge-red"

        st.markdown(
            f"""
            <div class="info-panel">
                <span class="badge-pill {badge_cls}">{tier}</span>
                <span class="badge-pill badge-blue">Cost Premium: +{opt['cost_premium_pct']}%</span>
                <h4 style="margin:0.45rem 0 0.25rem 0;">Audit Assessment</h4>
                <p style="margin:0;">{opt['verdict']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Weighted Ethics Score", f"{weighted_index:.1f}/100", tier, "#0F766E")
    with k2:
        render_kpi_card("Biodiversity Outcome", f"{opt['biodiversity_delta']:+d}%", "Net ecosystem trajectory", "#064E3B")
    with k3:
        render_kpi_card("Pollution Load Change", f"{opt['pollution_delta']:+d}%", "Positive = cleaner", "#0284C7")
    with k4:
        render_kpi_card("Lifecycle Carbon Delta", f"{opt['co2_delta']:+d} kt", "Negative = abatement", "#D97706")

    c_left, c_right = st.columns(2, gap="large")
    with c_left:
        lenses = [
            "Precautionary Principle",
            "Intergenerational Justice",
            "Ecological Integrity",
            "Environmental Justice",
            "Professional Integrity",
        ]
        radar = go.Figure(
            go.Scatterpolar(
                r=scores + [scores[0]],
                theta=lenses + [lenses[0]],
                fill="toself",
                fillcolor="rgba(20, 184, 166, 0.25)",
                line=dict(color="#0F766E", width=2.6),
                name="Selected Option",
            )
        )
        radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        apply_plotly_theme(radar, height=380, title="Five-Lens Ethical Alignment Profile")
        st.plotly_chart(radar, width="stretch")

    with c_right:
        comp_fig = go.Figure()
        for idx, name in enumerate(option_names):
            o = dilemma["options"][name]
            o_avg = sum(w * s for w, s in zip(weights, [o["precautionary"], o["intergenerational"], o["ecological"], o["justice"], o["integrity"]])) / sum(weights)
            comp_fig.add_trace(
                go.Bar(
                    x=[f"Option {idx + 1}"],
                    y=[o_avg],
                    name=name[:42] + ("..." if len(name) > 42 else ""),
                    marker_color="#0F766E" if name == selected_opt else "#94A3B8",
                    text=[f"{o_avg:.1f}"],
                    textposition="outside",
                )
            )
        comp_fig.update_yaxes(range=[0, 110], title="Weighted Ethics Score")
        apply_plotly_theme(comp_fig, height=380, title="Alternative Comparison Under Your Value Weights")
        st.plotly_chart(comp_fig, width="stretch")

    with st.expander("Generate Formal Ethical Engineering Justification Note"):
        rationale_note = st.text_area(
            "Document your engineering rationale (avoidance, mitigation, and stakeholder consent steps):",
            value=(
                f"Selected '{selected_opt}' for '{dilemma['title']}'. "
                f"Under weighted ethical priorities, this option achieved {weighted_index:.1f}/100, "
                f"with {opt['biodiversity_delta']:+d}% biodiversity outcome and +{opt['cost_premium_pct']}% capital premium."
            ),
            height=100,
            key="eth_note",
        )
        st.download_button(
            "Download Ethical Audit Memo (.txt)",
            data=rationale_note.encode("utf-8"),
            file_name="ethical_engineering_audit.txt",
            mime="text/plain",
        )

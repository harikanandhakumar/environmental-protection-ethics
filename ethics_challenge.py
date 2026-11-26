import plotly.graph_objects as go
import streamlit as st

from data_models import CHALLENGE_QUESTIONS
from styles import apply_plotly_theme, render_kpi_card, render_section_header


def render() -> None:
    render_section_header(
        "Section 7 — Engineering Ethics Challenge",
        "Test your applied judgment on real-world environmental ethics, pollution prevention, climate non-stationarity, and biodiversity protection dilemmas.",
        badge_text="Interactive Applied Ethics Assessment",
    )

    if "challenge_answers" not in st.session_state:
        st.session_state["challenge_answers"] = {}

    f1, f2 = st.columns([1.2, 2.2])
    with f1:
        diff_filter = st.selectbox(
            "Filter Challenge Difficulty",
            ["All Levels", "Foundation", "Intermediate", "Advanced"],
            key="chg_diff",
        )
    with f2:
        if st.button("Reset Challenge Responses", key="chg_reset"):
            st.session_state["challenge_answers"] = {}
            st.rerun()

    questions = (
        CHALLENGE_QUESTIONS
        if diff_filter == "All Levels"
        else [q for q in CHALLENGE_QUESTIONS if q["difficulty"] == diff_filter]
    )

    answered_count = 0
    correct_count = 0
    domain_totals = {}
    domain_correct = {}

    for q in CHALLENGE_QUESTIONS:
        dom = q["domain"]
        domain_totals[dom] = domain_totals.get(dom, 0) + 1
        domain_correct.setdefault(dom, 0)

    for q in questions:
        qid = q["id"]
        with st.container(border=True):
            st.markdown(
                f"<span class='badge-pill badge-blue'>{q['domain']}</span>"
                f"<span class='badge-pill badge-amber'>{q['difficulty']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Scenario {qid}:** {q['scenario']}")
            st.markdown(f"**{q['question']}**")

            prev_idx = st.session_state["challenge_answers"].get(qid, None)
            selected_text = st.radio(
                "Select your engineering response:",
                q["options"],
                index=prev_idx,
                key=f"chg_q_{qid}",
            )

            col_btn, col_status = st.columns([1, 3])
            with col_btn:
                if st.button(f"Verify Response #{qid}", key=f"chg_btn_{qid}"):
                    if selected_text is not None:
                        st.session_state["challenge_answers"][qid] = q["options"].index(selected_text)
            saved_idx = st.session_state["challenge_answers"].get(qid, None)
            if saved_idx is not None:
                with col_status:
                    if saved_idx == q["correct_idx"]:
                        st.success(f"Correct — {q['rationale']}")
                    else:
                        st.error(f"Needs revision — {q['rationale']}")

    # Aggregate full bank stats
    for q in CHALLENGE_QUESTIONS:
        saved = st.session_state["challenge_answers"].get(q["id"])
        if saved is not None:
            answered_count += 1
            if saved == q["correct_idx"]:
                correct_count += 1
                domain_correct[q["domain"]] += 1

    accuracy_pct = (correct_count / len(CHALLENGE_QUESTIONS)) * 100.0
    completion_pct = (answered_count / len(CHALLENGE_QUESTIONS)) * 100.0

    st.markdown("---")
    st.markdown("#### Stewardship Mastery Summary")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Challenges Verified", f"{answered_count}/{len(CHALLENGE_QUESTIONS)}", f"{completion_pct:.0f}% completed", "#0284C7")
    with k2:
        render_kpi_card("Correct Ethical Decisions", f"{correct_count}/{len(CHALLENGE_QUESTIONS)}", f"{accuracy_pct:.0f}% overall mastery", "#0F766E")
    with k3:
        tier = "Stewardship Leader" if accuracy_pct >= 75 else ("Practitioner" if answered_count >= 4 else "In Progress")
        render_kpi_card("Readiness Standing", tier, "Anonymous benchmark", "#064E3B")
    with k4:
        render_kpi_card("Active Filter Set", f"{len(questions)} cases", diff_filter, "#D97706")

    domains = list(domain_totals.keys())
    dom_scores = [round((domain_correct[d] / domain_totals[d]) * 100.0, 1) for d in domains]

    radar = go.Figure(
        go.Scatterpolar(
            r=dom_scores + [dom_scores[0]],
            theta=domains + [domains[0]],
            fill="toself",
            fillcolor="rgba(15, 118, 110, 0.25)",
            line=dict(color="#0F766E", width=2.5),
        )
    )
    radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    apply_plotly_theme(radar, height=370, title="Competency Profile Across Environmental Ethics Domains")
    st.plotly_chart(radar, width="stretch")

    if answered_count == len(CHALLENGE_QUESTIONS) and accuracy_pct >= 75:
        st.balloons()
        st.success(
            "All 8 Engineering Ethics Challenges completed with high mastery. "
            "Your decisions consistently prioritized avoidance, pollution prevention, climate resilience, and public welfare."
        )

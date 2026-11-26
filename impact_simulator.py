import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data_models import INFRASTRUCTURE_PROJECTS
from styles import apply_plotly_theme, render_kpi_card, render_section_header


def render() -> None:
    render_section_header(
        "Section 2 — Infrastructure Impact Simulator",
        "Model 25-year habitat integrity, net greenhouse emissions, stormwater pollution loads, and mitigation ROI for major civil infrastructure.",
        badge_text="25-Year Environmental Lifecycle Engine",
    )

    ctrl_col, viz_col = st.columns([1.05, 1.95], gap="large")

    with ctrl_col:
        st.markdown("#### Engineering & Mitigation Controls")
        project_name = st.selectbox(
            "Infrastructure Archetype",
            list(INFRASTRUCTURE_PROJECTS.keys()),
            key="sim_project",
        )
        proj = INFRASTRUCTURE_PROJECTS[project_name]
        st.caption(proj["summary"])

        scale_factor = st.slider("Project Footprint Scale (x)", 0.5, 2.0, 1.0, 0.1, key="sim_scale")
        mitigation_pct = st.slider("Ecological Mitigation Budget (% of CapEx)", 0, 30, 14, 1, key="sim_mit")
        wildlife_crossings = st.slider("Wildlife Crossing Density (per 10 km)", 0, 8, 4, 1, key="sim_cross")
        clean_fleet_pct = st.slider("Electric / Low-Carbon Construction Fleet (%)", 0, 100, 65, 5, key="sim_fleet")
        zld_bioswales = st.toggle("Zero-Liquid-Discharge & Bio-Retention Swales", value=True, key="sim_zld")
        dark_acoustic = st.toggle("Full-Cutoff Dark-Sky & Acoustic Barriers", value=True, key="sim_dark")

        if st.button("Apply Maximum Future-Proof Preset", width="stretch", key="sim_preset_btn"):
            st.info("Try setting Mitigation >= 18%, Crossings >= 5, Clean Fleet >= 85%, and keeping both ecological toggles enabled for net-positive alignment.")

    # Compute baseline vs. engineered metrics
    years = np.arange(2026, 2051)
    t_norm = np.linspace(0, 1, len(years))

    mit_eff = min(0.92, (mitigation_pct / 30.0) * 0.55 + (wildlife_crossings / 8.0) * 0.25 + (0.12 if dark_acoustic else 0.0))
    pollution_ctrl = (0.48 if zld_bioswales else 0.0) + (mitigation_pct / 30.0) * 0.28 + (clean_fleet_pct / 100.0) * 0.14
    carbon_ctrl = (clean_fleet_pct / 100.0) * 0.38 + (mitigation_pct / 30.0) * 0.22 + (0.10 if zld_bioswales else 0.0)

    # Habitat Integrity (100 = pristine baseline)
    unmitigated_loss = min(65.0, proj["base_habitat_loss"] * scale_factor)
    unmitigated_habitat = 100.0 - unmitigated_loss * (1 - np.exp(-3.5 * t_norm))

    engineered_initial_drop = unmitigated_loss * (1.0 - 0.72 * mit_eff)
    # Recovery curve via restoration & corridors
    recovery_gain = (mitigation_pct * 0.65 + wildlife_crossings * 1.8) * (t_norm ** 1.15)
    engineered_habitat = np.clip(100.0 - engineered_initial_drop * (1 - np.exp(-4.0 * t_norm)) + recovery_gain * 0.45, 20.0, 108.0)

    # Annual Net CO2e (kt/yr)
    base_co2 = proj["base_carbon_kt_yr"] * scale_factor
    unmitigated_co2 = base_co2 * (1.0 - 0.05 * t_norm)
    if base_co2 >= 0:
        engineered_co2 = base_co2 * (1.0 - carbon_ctrl) - (mitigation_pct * 0.9 * scale_factor) * t_norm
    else:
        engineered_co2 = base_co2 * (1.0 + 0.35 * carbon_ctrl) - (mitigation_pct * 0.5) * t_norm

    # Runoff & chemical pollution index
    base_runoff = proj["base_runoff_load"] * scale_factor
    unmitigated_runoff = np.full_like(years, base_runoff, dtype=float)
    engineered_runoff = base_runoff * (1.0 - pollution_ctrl) - (12.0 if zld_bioswales else 0.0)

    # Fragmentation & Capital cost
    unmit_frag = min(98.0, proj["base_fragmentation"] * scale_factor)
    eng_frag = max(5.0, unmit_frag * (1.0 - 0.68 * (wildlife_crossings / 8.0) - (0.15 if dark_acoustic else 0.0)))
    capex_musd = proj["base_cost_musd"] * scale_factor * (1.0 + mitigation_pct / 100.0)
    avoided_damage_musd = (unmitigated_loss - (100.0 - engineered_habitat[-1])) * 4.8 + max(0.0, unmitigated_co2.sum() - engineered_co2.sum()) * 0.085
    sustainability_roi = avoided_damage_musd / max(1.0, capex_musd * (mitigation_pct / 100.0 + 0.05))

    with viz_col:
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi_card(
                "2050 Habitat Integrity",
                f"{engineered_habitat[-1]:.1f}%",
                f"{engineered_habitat[-1] - unmitigated_habitat[-1]:+.1f} pts vs. baseline",
                "#0F766E",
            )
        with k2:
            cum_saved = float(unmitigated_co2.sum() - engineered_co2.sum())
            render_kpi_card(
                "25-Yr Carbon Avoided",
                f"{cum_saved:,.0f} kt",
                "CO₂e vs. unmitigated",
                "#0284C7",
            )
        with k3:
            render_kpi_card(
                "Fragmentation Risk",
                f"{eng_frag:.1f}/100",
                f"-{unmit_frag - eng_frag:.1f} barrier drop",
                "#D97706",
            )
        with k4:
            render_kpi_card(
                "Mitigation ROI Ratio",
                f"{sustainability_roi:.2f}x",
                f"CapEx: ${capex_musd:,.0f}M",
                "#064E3B",
            )

        tab1, tab2, tab3 = st.tabs(
            ["25-Year Habitat & Carbon Trajectories", "Pollution & Stressor Breakdown", "Multi-Dimensional Trade-Off Radar"]
        )

        with tab1:
            traj_fig = go.Figure()
            traj_fig.add_trace(
                go.Scatter(
                    x=years,
                    y=unmitigated_habitat,
                    name="Unmitigated Habitat Integrity (%)",
                    line=dict(color="#DC2626", width=2.5, dash="dash"),
                )
            )
            traj_fig.add_trace(
                go.Scatter(
                    x=years,
                    y=engineered_habitat,
                    name="Future-Proof Engineered Habitat (%)",
                    line=dict(color="#0F766E", width=3.2),
                    fill="tonexty",
                    fillcolor="rgba(15, 118, 110, 0.14)",
                )
            )
            traj_fig.add_hline(y=100, line_dash="dot", line_color="#64748B", annotation_text="Pre-Project Baseline (100%)")
            traj_fig.update_yaxes(title="Habitat Integrity Index (%)", range=[25, 112])
            traj_fig.update_xaxes(title="Simulation Year")
            apply_plotly_theme(traj_fig, height=370, title="2026–2050 Habitat Integrity & Ecological Recovery")
            st.plotly_chart(traj_fig, width="stretch")

        with tab2:
            stressors = ["Runoff & Chemical Load", "Habitat Fragmentation", "Annual Net Carbon (kt)", "Thermal/Acoustic Stress"]
            unmit_vals = [
                max(0.0, float(unmitigated_runoff[0])),
                float(unmit_frag),
                max(0.0, float(unmitigated_co2[0])),
                float(68.0 * scale_factor),
            ]
            eng_vals = [
                max(0.0, float(engineered_runoff[0])),
                float(eng_frag),
                max(0.0, float(engineered_co2[0])),
                float(68.0 * scale_factor * (0.35 if dark_acoustic else 0.82)),
            ]
            bar_fig = go.Figure(
                data=[
                    go.Bar(name="Conventional Unmitigated", x=stressors, y=unmit_vals, marker_color="#EF4444"),
                    go.Bar(name="Future-Proof Engineered", x=stressors, y=eng_vals, marker_color="#0F766E"),
                ]
            )
            bar_fig.update_layout(barmode="group")
            apply_plotly_theme(bar_fig, height=370, title="Environmental Stressor Comparison (Lower is Better)")
            st.plotly_chart(bar_fig, width="stretch")

        with tab3:
            dims = ["Biodiversity Protection", "Climate Decarbonization", "Pollution Prevention", "Corridor Permeability", "Cost Discipline"]
            score_eng = [
                min(100, engineered_habitat[-1]),
                min(100, max(10, 70 - engineered_co2[-1] * 0.45)),
                min(100, max(15, 85 - engineered_runoff[-1] * 0.85)),
                max(10, 100 - eng_frag),
                max(30, 100 - mitigation_pct * 1.4),
            ]
            score_unmit = [
                max(10, unmitigated_habitat[-1]),
                max(10, 55 - unmitigated_co2[-1] * 0.45),
                max(10, 65 - unmitigated_runoff[-1] * 0.85),
                max(5, 100 - unmit_frag),
                92,
            ]
            rad = go.Figure()
            rad.add_trace(go.Scatterpolar(r=score_unmit + [score_unmit[0]], theta=dims + [dims[0]], fill="toself", name="Conventional", line_color="#DC2626", fillcolor="rgba(220,38,38,0.14)"))
            rad.add_trace(go.Scatterpolar(r=score_eng + [score_eng[0]], theta=dims + [dims[0]], fill="toself", name="Future-Proof", line_color="#0F766E", fillcolor="rgba(15,118,110,0.24)"))
            rad.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
            apply_plotly_theme(rad, height=370, title="Engineering Sustainability Trade-Off Radar")
            st.plotly_chart(rad, width="stretch")

    # Export report
    export_df = pd.DataFrame(
        {
            "Year": years,
            "Unmitigated_Habitat_Index": np.round(unmitigated_habitat, 2),
            "Engineered_Habitat_Index": np.round(engineered_habitat, 2),
            "Unmitigated_CO2_kt": np.round(unmitigated_co2, 2),
            "Engineered_CO2_kt": np.round(engineered_co2, 2),
            "Unmitigated_Runoff_Load": np.round(unmitigated_runoff, 2),
            "Engineered_Runoff_Load": np.round(engineered_runoff, 2),
        }
    )
    d1, d2 = st.columns([3, 1])
    with d1:
        summary_payload = json.dumps(
            {
                "project": project_name,
                "scale_factor": scale_factor,
                "mitigation_budget_pct": mitigation_pct,
                "wildlife_crossings_per_10km": wildlife_crossings,
                "habitat_2050_pct": round(float(engineered_habitat[-1]), 2),
                "cumulative_co2_saved_kt": round(cum_saved, 2),
                "sustainability_roi": round(float(sustainability_roi), 2),
            },
            indent=2,
        )
        st.download_button(
            "Download Simulation CSV Projection",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="infrastructure_impact_projection.csv",
            mime="text/csv",
        )
    with d2:
        st.download_button(
            "Download JSON Summary",
            data=summary_payload.encode("utf-8"),
            file_name="impact_summary.json",
            mime="application/json",
        )

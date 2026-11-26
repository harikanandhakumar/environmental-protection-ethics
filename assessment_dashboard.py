import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_models import get_biodiversity_hotspots
from styles import apply_plotly_theme, render_kpi_card, render_section_header


def render() -> None:
    render_section_header(
        "Section 5 — Biodiversity Assessment Dashboard",
        "Monitor ecosystem integrity across taxa, climate stress scenarios, water quality, and pollution attenuation indices.",
        badge_text="Ecological KPI & Pressure-State-Response Telemetry",
    )

    hotspots = get_biodiversity_hotspots()

    c1, c2, c3 = st.columns([1.4, 1.2, 1.0])
    with c1:
        selected_regions = st.multiselect(
            "Regional Portfolio Scope",
            options=sorted(hotspots["region"].unique()),
            default=sorted(hotspots["region"].unique()),
            key="dash_regions",
        )
    with c2:
        climate_scenario = st.selectbox(
            "Climate & Policy Scenario",
            [
                "Current Trajectory (+2.4°C)",
                "Delayed Mitigation (+2.9°C High Stress)",
                "Future-Proof Engineering + 30x30 Rewilding (+1.5°C)",
            ],
            index=2,
            key="dash_scenario",
        )
    with c3:
        horizon_year = st.slider("Assessment Target Year", 2026, 2050, 2035, 1, key="dash_year")

    df = hotspots[hotspots["region"].isin(selected_regions)].copy()
    if df.empty:
        st.warning("Select at least one region to populate the Biodiversity Assessment Dashboard.")
        return

    # Scenario modifiers
    t_frac = (horizon_year - 2026) / 24.0
    if "Future-Proof" in climate_scenario:
        msa_shift = +11.5 * t_frac
        wqi_shift = +14.0 * t_frac
        shannon_shift = +0.28 * t_frac
        stress_mult = 0.72
    elif "Delayed" in climate_scenario:
        msa_shift = -16.0 * t_frac
        wqi_shift = -14.5 * t_frac
        shannon_shift = -0.34 * t_frac
        stress_mult = 1.25
    else:
        msa_shift = -6.5 * t_frac
        wqi_shift = -4.0 * t_frac
        shannon_shift = -0.10 * t_frac
        stress_mult = 1.02

    df["MSA_Index"] = np.clip(100 - df["fragmentation_risk"] * 0.42 * stress_mult + msa_shift, 15, 98)
    df["Water_Quality_Index"] = np.clip(100 - df["pollution_pressure"] * 0.55 * stress_mult + wqi_shift, 18, 99)
    df["Shannon_H"] = np.clip(2.4 + (df["species_richness"] / 12500.0) * 1.45 + shannon_shift, 1.2, 4.3)
    df["Carbon_CoBenefit_Mt"] = np.round(df["carbon_density_t_ha"] * (df["protected_pct"] / 100.0) * 0.45, 1)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Mean Species Abundance", f"{df['MSA_Index'].mean():.1f}%", f"Target year {horizon_year}", "#0F766E")
    with k2:
        render_kpi_card("Shannon Diversity (H')", f"{df['Shannon_H'].mean():.2f}", "Multi-taxa richness index", "#064E3B")
    with k3:
        render_kpi_card("Watershed WQI", f"{df['Water_Quality_Index'].mean():.1f}/100", "Bio-chemical runoff index", "#0284C7")
    with k4:
        render_kpi_card("Protected Carbon Pool", f"{df['Carbon_CoBenefit_Mt'].sum():.1f} Mt", "Ecosystem co-benefit", "#D97706")

    col_left, col_right = st.columns([1.15, 1.15], gap="large")
    with col_left:
        years = np.arange(2026, horizon_year + 1)
        if len(years) < 2:
            years = np.array([2026, 2027])
        tf = np.linspace(0, 1, len(years))

        base_amp = 74.0
        base_pol = 79.0
        base_aqu = 76.0
        base_mam = 72.0

        delta_end = msa_shift
        taxa_df = pd.DataFrame(
            {
                "Year": years,
                "Amphibians & Reptiles": np.clip(base_amp + delta_end * 1.15 * tf, 20, 99),
                "Pollinators & Insects": np.clip(base_pol + delta_end * 1.05 * tf, 20, 99),
                "Freshwater Fish Guild": np.clip(base_aqu + wqi_shift * 0.9 * tf, 20, 99),
                "Large Mammals & Raptors": np.clip(base_mam + delta_end * 0.95 * tf, 20, 99),
            }
        )
        trend_fig = px.line(
            taxa_df,
            x="Year",
            y=["Amphibians & Reptiles", "Pollinators & Insects", "Freshwater Fish Guild", "Large Mammals & Raptors"],
            markers=True,
            color_discrete_sequence=["#0F766E", "#D97706", "#0284C7", "#064E3B"],
        )
        trend_fig.update_yaxes(title="Population Viability Index (%)", range=[20, 102])
        apply_plotly_theme(trend_fig, height=390, title="Guild Population Trajectory Under Selected Scenario")
        st.plotly_chart(trend_fig, width="stretch")

    with col_right:
        heat_cols = ["MSA_Index", "Water_Quality_Index", "climate_vulnerability", "pollution_pressure", "protected_pct"]
        heat_labels = ["MSA (%)", "Water Quality", "Climate Risk", "Pollution Load", "Protected (%)"]
        z_data = df[heat_cols].round(1).values
        heat_fig = go.Figure(
            data=go.Heatmap(
                z=z_data,
                x=heat_labels,
                y=df["name"].tolist(),
                colorscale="Tealgrn",
                text=z_data,
                texttemplate="%{text}",
                hovertemplate="%{y}<br>%{x}: %{z}<extra></extra>",
            )
        )
        apply_plotly_theme(heat_fig, height=390, title="Ecoregion Ecosystem Health Matrix")
        st.plotly_chart(heat_fig, width="stretch")

    # Bubble scatter: Climate Risk vs Pollution vs Carbon Stock
    st.markdown("#### Biodiversity Risk vs. Pollution Exposure & Carbon Co-Benefits")
    scat_fig = px.scatter(
        df,
        x="pollution_pressure",
        y="MSA_Index",
        size="carbon_density_t_ha",
        color="biome",
        hover_name="name",
        labels={
            "pollution_pressure": "Baseline Pollution Pressure (0-100)",
            "MSA_Index": "Projected Mean Species Abundance (%)",
        },
        size_max=40,
    )
    apply_plotly_theme(scat_fig, height=370, title="Hotspot Resilience Bubble Matrix (Size = Carbon Density tC/ha)")
    st.plotly_chart(scat_fig, width="stretch")

    st.download_button(
        "Export Portfolio Assessment CSV",
        data=df[["name", "region", "biome", "MSA_Index", "Water_Quality_Index", "Shannon_H", "Carbon_CoBenefit_Mt"]]
        .round(2)
        .to_csv(index=False)
        .encode("utf-8"),
        file_name="biodiversity_assessment_report.csv",
        mime="text/csv",
    )

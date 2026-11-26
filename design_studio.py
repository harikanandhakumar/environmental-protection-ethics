import json
import plotly.graph_objects as go
import streamlit as st

from styles import (
    apply_plotly_theme,
    get_asset_path,
    render_kpi_card,
    render_section_header,
)

MATERIALS = {
    "Conventional OPC Concrete + Virgin Steel": {"embodied_drop": 0, "circularity": 18, "cost_mult": 1.00},
    "Slag / Calcined-Clay Geopolymer + Recycled Steel": {"embodied_drop": 46, "circularity": 72, "cost_mult": 1.07},
    "Mass Timber (FSC CLT) + Bio-Aggregate Hybrid": {"embodied_drop": 68, "circularity": 86, "cost_mult": 1.12},
}

STORMWATER = {
    "Standard Curb & Pipe Culverts": {"retention": 18, "pollution_removal": 15, "bng": -4, "cooling": 0.1},
    "Permeable Pavements + Vegetated Bioswales": {"retention": 68, "pollution_removal": 74, "bng": 12, "cooling": 1.3},
    "Constructed Bio-Filtration Wetland + Sponge Terrace": {"retention": 92, "pollution_removal": 91, "bng": 26, "cooling": 2.4},
}

ENERGY = {
    "Grid Baseline Only": {"clean_pct": 25, "op_carbon_drop": 10},
    "Rooftop Solar + Battery Storage": {"clean_pct": 72, "op_carbon_drop": 64},
    "Bifacial Agrivoltaic + Geothermal Heat Loop": {"clean_pct": 96, "op_carbon_drop": 91},
}


def render() -> None:
    render_section_header(
        "Section 6 — Sustainable Infrastructure Design Studio",
        "Assemble a net-zero, biodiversity-positive civil engineering blueprint and evaluate embodied carbon, circularity, urban cooling, and 30-year lifecycle cost.",
        badge_text="Future-Proof Civil Blueprint Configurator",
    )

    top_img, top_cfg = st.columns([1.2, 1.8], gap="large")
    with top_img:
        st.image(
            get_asset_path("sustainable_infra.png"),
            caption="Integrated green-roof transit hub, bioswale retention ponds, and clean energy arrays",
            width="stretch",
        )
    with top_cfg:
        st.markdown("#### Configure Future-Proof Engineering Specifications")
        s1, s2 = st.columns(2)
        with s1:
            mat_choice = st.selectbox("Primary Structural Material System", list(MATERIALS.keys()), index=1, key="studio_mat")
            storm_choice = st.selectbox("Stormwater & Pollution Control", list(STORMWATER.keys()), index=2, key="studio_storm")
            energy_choice = st.selectbox("Site Energy Architecture", list(ENERGY.keys()), index=2, key="studio_energy")
        with s2:
            green_roof_pct = st.slider("Native Living Roof & Pollinator Canopy (%)", 0, 100, 75, 5, key="studio_roof")
            waste_diversion_pct = st.slider("Construction Waste Circular Reuse (%)", 10, 98, 85, 2, key="studio_waste")
            dark_sky_wildlife = st.toggle("Dark-Sky Shielded Lighting & Bird-Safe Glazing", value=True, key="studio_dark")

    mat = MATERIALS[mat_choice]
    storm = STORMWATER[storm_choice]
    eng = ENERGY[energy_choice]

    embodied_reduction = min(85.0, mat["embodied_drop"] + waste_diversion_pct * 0.14)
    circularity_score = min(98.0, mat["circularity"] * 0.55 + waste_diversion_pct * 0.45)
    net_bng_pct = storm["bng"] + green_roof_pct * 0.18 + (6.0 if dark_sky_wildlife else -4.0)
    cooling_c = storm["cooling"] + (green_roof_pct / 100.0) * 1.4
    storm_retention = min(98.0, storm["retention"] + (green_roof_pct / 100.0) * 8.0)

    # 30-year Total Cost of Ownership (index: 100 = Conventional Baseline)
    capex_idx = 100.0 * mat["cost_mult"] + (green_roof_pct * 0.08) + (5.0 if "Wetland" in storm_choice else 2.0)
    opex_30yr_conv = 85.0  # energy + flood damage + carbon penalty
    opex_30yr_green = opex_30yr_conv * (1.0 - eng["op_carbon_drop"] / 145.0) - (storm_retention * 0.16)
    tco_conv = 100.0 + opex_30yr_conv
    tco_green = capex_idx + max(18.0, opex_30yr_green)

    overall_grade_score = (
        embodied_reduction * 0.25
        + circularity_score * 0.20
        + storm_retention * 0.20
        + min(100, max(0, 60 + net_bng_pct * 1.2)) * 0.20
        + eng["clean_pct"] * 0.15
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Design Sustainability Score", f"{overall_grade_score:.1f}/100", "Future-proof readiness", "#0F766E")
    with k2:
        render_kpi_card("Embodied Carbon Cut", f"-{embodied_reduction:.1f}%", "vs. OPC concrete baseline", "#064E3B")
    with k3:
        render_kpi_card("Biodiversity Net Gain", f"{net_bng_pct:+.1f}%", f"Stormwater capture: {storm_retention:.0f}%", "#0284C7")
    with k4:
        render_kpi_card("30-Yr Lifecycle Cost", f"{tco_green:.1f} idx", f"{tco_green - tco_conv:+.1f} vs. conventional (185)", "#D97706")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=overall_grade_score,
                delta={"reference": 70, "increasing": {"color": "#0F766E"}},
                title={"text": "Future-Proof Engineering Readiness"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#0F766E"},
                    "steps": [
                        {"range": [0, 50], "color": "#FEE2E2"},
                        {"range": [50, 75], "color": "#FEF3C7"},
                        {"range": [75, 100], "color": "#D1FAE5"},
                    ],
                    "threshold": {"line": {"color": "#064E3B", "width": 3}, "value": 80},
                },
            )
        )
        apply_plotly_theme(gauge, height=350)
        st.plotly_chart(gauge, width="stretch")

    with c2:
        cost_fig = go.Figure(
            data=[
                go.Bar(name="Upfront CapEx Index", x=["Conventional Design", "Your Green Studio Design"], y=[100.0, capex_idx], marker_color="#64748B"),
                go.Bar(name="30-Yr Energy, Flood & Carbon OpEx", x=["Conventional Design", "Your Green Studio Design"], y=[opex_30yr_conv, max(18.0, opex_30yr_green)], marker_color="#0F766E"),
            ]
        )
        cost_fig.update_layout(barmode="stack")
        cost_fig.update_yaxes(title="Normalized Lifecycle Cost Index")
        apply_plotly_theme(cost_fig, height=350, title="30-Year Total Cost of Ownership Comparison")
        st.plotly_chart(cost_fig, width="stretch")

    spec_summary = {
        "structural_material": mat_choice,
        "stormwater_system": storm_choice,
        "energy_architecture": energy_choice,
        "living_roof_pct": green_roof_pct,
        "waste_circularity_pct": waste_diversion_pct,
        "dark_sky_and_bird_safe": dark_sky_wildlife,
        "metrics": {
            "sustainability_score": round(overall_grade_score, 2),
            "embodied_carbon_cut_pct": round(embodied_reduction, 2),
            "circularity_score": round(circularity_score, 2),
            "biodiversity_net_gain_pct": round(net_bng_pct, 2),
            "urban_cooling_c": round(cooling_c, 2),
            "tco_index_30yr": round(tco_green, 2),
        },
    }
    st.download_button(
        "Export Design Blueprint Specification (JSON)",
        data=json.dumps(spec_summary, indent=2).encode("utf-8"),
        file_name="sustainable_design_blueprint.json",
        mime="application/json",
    )

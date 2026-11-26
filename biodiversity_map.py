import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_models import get_biodiversity_hotspots
from styles import (
    apply_plotly_theme,
    get_asset_path,
    render_kpi_card,
    render_section_header,
)


def render() -> None:
    render_section_header(
        "Section 1 — Interactive Biodiversity Map",
        "Explore global ecological hotspots, endemic richness, climate-pollution stressors, and site-specific ethical engineering directives.",
        badge_text="Geospatial Ecology & Siting Intelligence",
    )

    df = get_biodiversity_hotspots()

    banner_col, intro_col = st.columns([1.3, 1.7], gap="large")
    with banner_col:
        st.image(
            get_asset_path("biodiversity_biome.png"),
            caption="Interconnected terrestrial, riparian, and coastal mangrove biodiversity zones",
            width="stretch",
        )
    with intro_col:
        st.markdown("#### Geospatial Screening Filters")
        f1, f2 = st.columns(2)
        with f1:
            selected_biomes = st.multiselect(
                "Filter Biomes",
                options=sorted(df["biome"].unique()),
                default=sorted(df["biome"].unique()),
                key="bio_map_biomes",
            )
            min_endemic = st.slider(
                "Minimum Endemic Species",
                min_value=0,
                max_value=3500,
                value=200,
                step=100,
                key="bio_map_endemic",
            )
        with f2:
            threat_filter = st.multiselect(
                "Threat Severity",
                options=["Critical", "High", "Moderate"],
                default=["Critical", "High", "Moderate"],
                key="bio_map_threat",
            )
            map_mode = st.radio(
                "Map Projection Mode",
                ["Natural Earth Vector (Offline-Safe)", "OpenStreetMap Interactive Tiles"],
                horizontal=False,
                key="bio_map_mode",
            )

    filtered = df[
        df["biome"].isin(selected_biomes)
        & df["threat_level"].isin(threat_filter)
        & (df["endemic_species"] >= min_endemic)
    ].copy()

    if filtered.empty:
        st.warning("No biodiversity hotspots match your active filter criteria. Widen the filters above.")
        return

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Active Hotspots", f"{len(filtered)}", f"of {len(df)} monitored regions", "#0F766E")
    with k2:
        render_kpi_card(
            "Avg Conservation Priority",
            f"{filtered['conservation_priority'].mean():.1f}/100",
            "IUCN & carbon weighted",
            "#0284C7",
        )
    with k3:
        render_kpi_card(
            "Peak Endemic Richness",
            f"{filtered['endemic_species'].max():,}",
            filtered.loc[filtered["endemic_species"].idxmax(), "name"],
            "#D97706",
        )
    with k4:
        render_kpi_card(
            "Mean Protected Coverage",
            f"{filtered['protected_pct'].mean():.1f}%",
            "Target >= 30% by 2030",
            "#064E3B",
        )

    color_map = {"Critical": "#DC2626", "High": "#D97706", "Moderate": "#0F766E"}

    if map_mode.startswith("Natural Earth"):
        fig = px.scatter_geo(
            filtered,
            lat="lat",
            lon="lon",
            size="species_richness",
            color="threat_level",
            color_discrete_map=color_map,
            hover_name="name",
            hover_data={
                "region": True,
                "biome": True,
                "species_richness": ":,",
                "endemic_species": ":,",
                "conservation_priority": True,
                "lat": False,
                "lon": False,
            },
            projection="natural earth",
            size_max=34,
        )
        fig.update_geos(
            showcoastlines=True,
            coastlinecolor="#64748B",
            showland=True,
            landcolor="#ECFDF5",
            showocean=True,
            oceancolor="#E0F2FE",
            showcountries=True,
            countrycolor="#CBD5E1",
            lataxis_showgrid=True,
            lonaxis_showgrid=True,
            gridcolor="rgba(148,163,184,0.25)",
        )
    else:
        fig = px.scatter_map(
            filtered,
            lat="lat",
            lon="lon",
            size="species_richness",
            color="threat_level",
            color_discrete_map=color_map,
            hover_name="name",
            hover_data={
                "region": True,
                "biome": True,
                "species_richness": ":,",
                "endemic_species": ":,",
                "conservation_priority": True,
                "lat": False,
                "lon": False,
            },
            zoom=1.15,
            size_max=32,
            map_style="open-street-map",
        )

    apply_plotly_theme(fig, height=460, title="Global Biodiversity Hotspots & Engineering Sensitivity")
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### Hotspot Deep-Dive & Engineering Siting Directive")
    selected_name = st.selectbox(
        "Select a Hotspot to Inspect Environmental Risk Profile",
        options=filtered["name"].tolist(),
        key="bio_map_inspect",
    )
    spot = filtered[filtered["name"] == selected_name].iloc[0]

    left_col, right_col = st.columns([1.1, 1.2], gap="large")
    with left_col:
        st.markdown(
            f"""
            <div class="info-panel">
                <span class="badge-pill badge-blue">{spot['region']}</span>
                <span class="badge-pill badge-green">{spot['biome']}</span>
                <span class="badge-pill badge-amber">Threat: {spot['threat_level']}</span>
                <h4 style="margin:0.5rem 0 0.35rem 0; color:#064E3B;">{spot['name']}</h4>
                <p style="margin:0 0 0.45rem 0;"><b>Key Taxa:</b> {spot['key_taxa']}</p>
                <p style="margin:0 0 0.45rem 0;"><b>Ecosystem Carbon Stock:</b> {spot['carbon_density_t_ha']} tC/ha &nbsp;|&nbsp; <b>Protected Area:</b> {spot['protected_pct']}%</p>
                <p style="margin:0; color:#0F172A;"><b>Mandatory Engineering Directive:</b> {spot['engineering_directive']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Comparison bar across filtered hotspots
        top_bars = filtered.sort_values("conservation_priority", ascending=True).tail(8)
        bar_fig = px.bar(
            top_bars,
            x="conservation_priority",
            y="name",
            orientation="h",
            color="threat_level",
            color_discrete_map=color_map,
            labels={"conservation_priority": "Conservation Priority Index", "name": ""},
        )
        apply_plotly_theme(bar_fig, height=280, title="Priority Ranking of Filtered Hotspots")
        st.plotly_chart(bar_fig, width="stretch")

    with right_col:
        categories = [
            "Conservation Priority",
            "Climate Vulnerability",
            "Pollution Pressure",
            "Fragmentation Risk",
            "Unprotected Gap",
        ]
        values = [
            float(spot["conservation_priority"]),
            float(spot["climate_vulnerability"]),
            float(spot["pollution_pressure"]),
            float(spot["fragmentation_risk"]),
            float(100 - spot["protected_pct"]),
        ]
        radar_fig = go.Figure(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(15, 118, 110, 0.25)",
                line=dict(color="#0F766E", width=2.5),
                name=spot["name"],
            )
        )
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
        )
        apply_plotly_theme(radar_fig, height=430, title=f"Multi-Stressor Vulnerability Profile — {spot['name']}")
        st.plotly_chart(radar_fig, width="stretch")

    with st.expander("View Complete Hotspot Ecological Dataset"):
        st.dataframe(
            filtered[
                [
                    "name",
                    "region",
                    "biome",
                    "threat_level",
                    "species_richness",
                    "endemic_species",
                    "climate_vulnerability",
                    "pollution_pressure",
                    "fragmentation_risk",
                    "protected_pct",
                ]
            ],
            width="stretch",
            hide_index=True,
        )

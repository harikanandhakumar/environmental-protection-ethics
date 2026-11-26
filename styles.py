from pathlib import Path
import streamlit as st

PALETTE = {
    "forest": "#064E3B",
    "emerald": "#0F766E",
    "teal": "#14B8A6",
    "mint": "#ECFDF5",
    "sky": "#0284C7",
    "amber": "#D97706",
    "coral": "#DC2626",
    "slate": "#0F172A",
    "muted": "#475569",
    "border": "#CBD5E1",
    "surface": "#FFFFFF",
}


def get_asset_path(filename: str) -> str:
    """Return a relative asset path compatible with local runs and Streamlit Cloud."""
    rel_path = Path("assets") / filename
    return rel_path.as_posix()


def inject_custom_css() -> None:
    """Inject responsive eco-engineering UI styling."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2.5rem;
            max-width: 1320px;
        }
        .hero-card {
            background: linear-gradient(135deg, #064E3B 0%, #0F766E 55%, #0284C7 100%);
            color: #F8FAFC;
            border-radius: 16px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1.15rem;
            box-shadow: 0 10px 28px rgba(6, 78, 59, 0.16);
        }
        .hero-kicker {
            font-size: 0.78rem;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            color: #A7F3D0;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .hero-title {
            font-size: clamp(1.35rem, 2.3vw, 2.05rem);
            font-weight: 800;
            line-height: 1.2;
            margin: 0 0 0.45rem 0;
            color: #FFFFFF;
        }
        .hero-sub {
            font-size: 0.96rem;
            color: #E2E8F0;
            line-height: 1.5;
            margin: 0;
        }
        .section-banner {
            background: linear-gradient(90deg, #ECFDF5 0%, #F0F9FF 100%);
            border-left: 5px solid #0F766E;
            border-radius: 10px;
            padding: 0.95rem 1.2rem;
            margin-bottom: 1rem;
        }
        .section-banner h3 {
            margin: 0 0 0.25rem 0;
            color: #064E3B;
            font-size: 1.18rem;
        }
        .section-banner p {
            margin: 0;
            color: #334155;
            font-size: 0.92rem;
        }
        .kpi-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 4px solid #0F766E;
            border-radius: 12px;
            padding: 0.9rem 1rem;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
            margin-bottom: 0.6rem;
        }
        .kpi-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            font-weight: 600;
        }
        .kpi-value {
            font-size: 1.55rem;
            font-weight: 800;
            color: #0F172A;
            margin: 0.15rem 0;
        }
        .kpi-delta {
            font-size: 0.82rem;
            font-weight: 600;
            color: #0F766E;
        }
        .badge-pill {
            display: inline-block;
            padding: 0.22rem 0.65rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            margin-right: 0.35rem;
            margin-bottom: 0.25rem;
        }
        .badge-green { background: #D1FAE5; color: #065F46; }
        .badge-amber { background: #FEF3C7; color: #92400E; }
        .badge-red { background: #FEE2E2; color: #991B1B; }
        .badge-blue { background: #E0F2FE; color: #075985; }
        .info-panel {
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.8rem;
        }
        @media (max-width: 768px) {
            .block-container {
                padding-left: 0.85rem;
                padding-right: 0.85rem;
            }
            .hero-card {
                padding: 1.1rem 1.1rem;
            }
            .kpi-value {
                font-size: 1.25rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str, badge_text: str = "") -> None:
    badge_html = f'<span class="badge-pill badge-green">{badge_text}</span><br>' if badge_text else ""
    st.markdown(
        f"""
        <div class="section-banner">
            {badge_html}
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, delta: str = "", accent: str = "#0F766E") -> None:
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top-color: {accent};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_plotly_theme(fig, height: int = 420, title: str = ""):
    """Apply clean, high-contrast styling to Plotly figures."""
    layout_kwargs = dict(
        height=height,
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0.95)",
        plot_bgcolor="rgba(248,250,252,0.75)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#0F172A", size=12),
        margin=dict(l=28, r=20, t=48 if title else 28, b=28),
        hoverlabel=dict(bgcolor="#0F172A", font_color="#F8FAFC", font_size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
    )
    if title:
        layout_kwargs["title"] = dict(text=title, font=dict(size=15, color="#064E3B"))
    fig.update_layout(**layout_kwargs)
    return fig

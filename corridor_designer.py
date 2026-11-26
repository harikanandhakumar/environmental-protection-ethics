import heapq
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from data_models import SPECIES_PROFILES
from styles import (
    apply_plotly_theme,
    get_asset_path,
    render_kpi_card,
    render_section_header,
)

# Landscape grid codes:
# 0 = Forest Reserve, 1 = Agricultural Buffer, 2 = River/Riparian, 3 = Highway Barrier,
# 4 = Urban Zone, 5 = Vegetated Eco-Duct Overpass, 6 = Riparian Culvert Underpass, 7 = Rewilded Stepping Stone
TILE_LABELS = {
    0: "Primary Forest",
    1: "Agri-Meadow Buffer",
    2: "River Channel",
    3: "Highway Corridor",
    4: "Urban Footprint",
    5: "Eco-Duct Overpass",
    6: "Riparian Underpass",
    7: "Rewilded Stepping Stone",
}


def build_base_landscape(rows: int = 12, cols: int = 18, add_second_highway: bool = False) -> np.ndarray:
    grid = np.ones((rows, cols), dtype=int)
    # West and East core forest reserves
    grid[:, :4] = 0
    grid[:, 14:] = 0
    grid[1:4, 4:6] = 0
    grid[7:11, 12:14] = 0

    # Winding river
    for c in range(cols):
        r = int(5 + round(1.4 * np.sin(c * 0.45)))
        if 0 <= r < rows:
            grid[r, c] = 2

    # Main north-south highway dividing the habitat
    grid[:, 9] = 3
    if add_second_highway:
        grid[:, 12] = 3

    # Urban settlements
    grid[0:3, 7:9] = 4
    grid[9:12, 10:12] = 4
    return grid


def compute_least_cost_path(grid: np.ndarray, profile: dict):
    rows, cols = grid.shape
    cost_map = np.zeros_like(grid, dtype=float)
    for r in range(rows):
        for c in range(cols):
            tile = grid[r, c]
            if tile == 0:
                cost_map[r, c] = profile["forest_cost"]
            elif tile == 1:
                cost_map[r, c] = profile["buffer_cost"]
            elif tile == 2:
                cost_map[r, c] = profile["river_penalty"]
            elif tile == 3:
                cost_map[r, c] = profile["road_penalty"]
            elif tile == 4:
                cost_map[r, c] = profile["urban_penalty"]
            elif tile == 5:
                cost_map[r, c] = profile["overpass_bonus_cost"]
            elif tile == 6:
                cost_map[r, c] = profile["underpass_bonus_cost"]
            elif tile == 7:
                cost_map[r, c] = 1.05

    start = (5, 1)
    goal = (6, cols - 2)
    pq = [(cost_map[start], start)]
    dist = {start: cost_map[start]}
    parent = {}

    dirs = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
            (-1, -1, 1.41), (-1, 1, 1.41), (1, -1, 1.41), (1, 1, 1.41)]

    while pq:
        d, (r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            break
        if d > dist.get((r, c), float("inf")):
            continue
        for dr, dc, step_mult in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = d + cost_map[nr, nc] * step_mult
                if nd < dist.get((nr, nc), float("inf")):
                    dist[(nr, nc)] = nd
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(pq, (nd, (nr, nc)))

    path = []
    cur = goal
    while cur in parent:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()
    return path, dist[goal], cost_map


def render() -> None:
    render_section_header(
        "Section 4 — Wildlife Corridor Designer",
        "Design wildlife eco-ducts, riparian underpasses, and rewilded stepping stones across fragmented landscapes using least-cost ecological pathfinding.",
        badge_text="Spatial Connectivity & Rewilding Engine",
    )

    c_img, c_ctrl = st.columns([1.15, 1.85], gap="large")
    with c_img:
        st.image(
            get_asset_path("corridor_overpass.png"),
            caption="Vegetated eco-duct overpass reconnecting divided forest reserves",
            width="stretch",
        )
    with c_ctrl:
        species_name = st.selectbox("Target Focal Species / Guild", list(SPECIES_PROFILES.keys()), key="cor_species")
        profile = SPECIES_PROFILES[species_name]
        st.info(profile["note"])

        m1, m2 = st.columns(2)
        with m1:
            overpass_rows = st.multiselect(
                "Place Eco-Duct Overpasses on Highway (Row)",
                options=list(range(12)),
                default=[3, 8],
                key="cor_overpasses",
            )
            underpass_river = st.toggle("Install Riparian Culvert Underpass at River Crossing", value=True, key="cor_underpass")
        with m2:
            rewilded_col6 = st.slider("Stepping-Stone Rewilding Density (%)", 0, 100, 60, 20, key="cor_rewild")
            second_highway = st.toggle("Simulate Secondary Freight Spur (High Stress)", value=False, key="cor_hwy2")

    # Build grid & apply user mitigations
    base_grid = build_base_landscape(add_second_highway=second_highway)
    unmitigated_path, unmitigated_cost, _ = compute_least_cost_path(base_grid, profile)

    eng_grid = base_grid.copy()
    for r in overpass_rows:
        eng_grid[r, 9] = 5
        if second_highway:
            eng_grid[r, 12] = 5

    if underpass_river:
        for r in range(12):
            if eng_grid[r, 9] == 2 or (r > 0 and eng_grid[r - 1, 9] == 2):
                eng_grid[r, 9] = 6
                if second_highway:
                    eng_grid[r, 12] = 6

    n_rewild = int(round((rewilded_col6 / 100.0) * 6))
    rewild_coords = [(4, 6), (5, 7), (6, 8), (5, 10), (6, 11), (4, 11)]
    for rr, cc in rewild_coords[:n_rewild]:
        if eng_grid[rr, cc] == 1:
            eng_grid[rr, cc] = 7

    eng_path, eng_cost, cost_map = compute_least_cost_path(eng_grid, profile)

    connectivity_score = max(8.0, min(99.0, 100.0 * (22.0 / max(18.0, eng_cost))))
    unmit_conn = max(5.0, min(95.0, 100.0 * (22.0 / max(18.0, unmitigated_cost))))
    mortality_drop = min(94.0, max(0.0, (unmitigated_cost - eng_cost) / max(1.0, unmitigated_cost) * 115.0))
    crossings_used = sum(1 for r, c in eng_path if eng_grid[r, c] in (5, 6))

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Habitat Connectivity", f"{connectivity_score:.1f}%", f"{connectivity_score - unmit_conn:+.1f} pts vs. unmitigated", "#0F766E")
    with k2:
        render_kpi_card("Road Mortality Reduction", f"{mortality_drop:.1f}%", f"Path resistance: {eng_cost:.1f}", "#064E3B")
    with k3:
        render_kpi_card("Eco-Structures Traversed", f"{crossings_used}", "Overpasses / culverts used", "#0284C7")
    with k4:
        render_kpi_card("Optimal Route Length", f"{len(eng_path)} cells", "West Reserve -> East Reserve", "#D97706")

    # Visualize interactive landscape heatmap + path overlay
    colorscale = [
        [0 / 7, "#065F46"],  # Primary Forest
        [1 / 7, "#A7F3D0"],  # Agri-Meadow
        [2 / 7, "#0284C7"],  # River
        [3 / 7, "#334155"],  # Highway
        [4 / 7, "#EF4444"],  # Urban
        [5 / 7, "#22C55E"],  # Eco-Duct Overpass
        [6 / 7, "#38BDF8"],  # Riparian Underpass
        [7 / 7, "#84CC16"],  # Rewilded Stepping Stone
    ]
    hover_text = [[TILE_LABELS[int(eng_grid[r, c])] + f" (Cost: {cost_map[r, c]:.1f})" for c in range(18)] for r in range(12)]

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=eng_grid,
            colorscale=colorscale,
            zmin=0,
            zmax=7,
            showscale=False,
            text=hover_text,
            hovertemplate="Row %{y}, Col %{x}<br>%{text}<extra></extra>",
        )
    )
    path_y = [p[0] for p in eng_path]
    path_x = [p[1] for p in eng_path]
    fig.add_trace(
        go.Scatter(
            x=path_x,
            y=path_y,
            mode="lines+markers",
            name="Optimal Wildlife Migration Path",
            line=dict(color="#FACC15", width=4),
            marker=dict(size=7, color="#FEF08A", line=dict(color="#0F172A", width=1)),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[1, 16],
            y=[5, 6],
            mode="markers+text",
            text=["West Reserve", "East Reserve"],
            textposition="top center",
            textfont=dict(color="#FFFFFF", size=12),
            marker=dict(size=13, color="#FFFFFF", symbol="star", line=dict(color="#064E3B", width=2)),
            name="Core Reserve Anchors",
        )
    )
    fig.update_yaxes(autorange="reversed", title="North-South Grid Row", dtick=1)
    fig.update_xaxes(title="West-East Landscape Column", dtick=1)
    apply_plotly_theme(fig, height=450, title=f"Landscape Permeability & Least-Cost Migration Corridor — {species_name}")
    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Legend: Dark Green = Primary Forest | Mint = Agri-Buffer | Blue = River | Charcoal = Highway | "
        "Red = Urban | Bright Green = Eco-Duct Overpass | Cyan = Riparian Underpass | Lime = Rewilded Stepping Stone | Yellow Line = Optimal Path."
    )

# Environmental Protection Ethics in Future-Proof Engineering for Biodiversity, Climate and Pollution Prevention

An interactive, multi-module Streamlit simulation platform for exploring ethical civil and environmental engineering decisions across biodiversity conservation, climate resilience, and pollution prevention.

## Interactive Sections

1. **Interactive Biodiversity Map** — Geospatial screening across global ecological hotspots with biome/threat filtering, multi-stressor vulnerability radars, and mandatory engineering directives.
2. **Infrastructure Impact Simulator** — 25-year (2026–2050) projection engine comparing unmitigated vs. future-proof infrastructure across habitat integrity, net CO₂e emissions, runoff pollution, fragmentation, and mitigation ROI, with CSV/JSON exports.
3. **Ethical Decision-Making Lab** — Normative ethics workbench evaluating real engineering dilemmas across Precautionary Principle, Intergenerational Justice, Ecological Integrity, Environmental Justice, and Professional Integrity with customizable value weights.
4. **Wildlife Corridor Designer** — Spatial landscape simulator running least-cost ecological pathfinding (Dijkstra over habitat resistance grids) with configurable eco-duct overpasses, riparian underpasses, and rewilded stepping stones.
5. **Biodiversity Assessment Dashboard** — Portfolio telemetry dashboard tracking Mean Species Abundance (MSA), Shannon Diversity ($H'$), Water Quality Index (WQI), taxa viability curves, and carbon co-benefits under climate scenarios.
6. **Sustainable Infrastructure Design Studio** — Green blueprint configurator comparing low-carbon structural materials, bio-filtration stormwater systems, clean energy integration, urban cooling, and 30-year total cost of ownership.
7. **Engineering Ethics Challenge** — Interactive scenario-based ethics assessment with domain competency profiling and immediate rationale feedback.

## Project Structure

All Python modules reside directly in the repository root for simple, consistent imports and zero-friction Streamlit Cloud deployment:

```text
Environmental_Ethics_Final/
├── app.py
├── styles.py
├── data_models.py
├── biodiversity_map.py
├── impact_simulator.py
├── ethics_lab.py
├── corridor_designer.py
├── assessment_dashboard.py
├── design_studio.py
├── ethics_challenge.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── assets/
    ├── hero_banner.png
    ├── biodiversity_biome.png
    ├── corridor_overpass.png
    ├── sustainable_infra.png
    └── ethics_compass.png
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push the contents of this repository directly to a GitHub repository.
2. Open Streamlit Community Cloud and create a new app pointing to that repository.
3. Set the main file path to `app.py`.
4. Deploy — all relative asset paths (`assets/...`) and root-level module imports resolve automatically.

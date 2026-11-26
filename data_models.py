import pandas as pd

SECTIONS = [
    "1. Interactive Biodiversity Map",
    "2. Infrastructure Impact Simulator",
    "3. Ethical Decision-Making Lab",
    "4. Wildlife Corridor Designer",
    "5. Biodiversity Assessment Dashboard",
    "6. Sustainable Infrastructure Design Studio",
    "7. Engineering Ethics Challenge",
]


def get_biodiversity_hotspots() -> pd.DataFrame:
    """Curated global ecological hotspots with climate, pollution, and engineering risk metrics."""
    rows = [
        {
            "id": "western_ghats",
            "name": "Western Ghats Escarpment",
            "region": "South Asia",
            "biome": "Tropical Montane Forest",
            "lat": 11.4,
            "lon": 76.5,
            "species_richness": 7402,
            "endemic_species": 1820,
            "threat_level": "Critical",
            "conservation_priority": 96,
            "climate_vulnerability": 84,
            "pollution_pressure": 68,
            "fragmentation_risk": 88,
            "protected_pct": 24,
            "carbon_density_t_ha": 245,
            "key_taxa": "Amphibians, Asian Elephant, Lion-tailed Macaque, Freshwater Fish",
            "engineering_directive": "Mandate elevated viaducts over valley corridors, slope bio-stabilization, and zero-discharge runoff basins.",
        },
        {
            "id": "amazon_tapajos",
            "name": "Tapajos Basin Ecotone",
            "region": "South America",
            "biome": "Tropical Rainforest & Riverine",
            "lat": -4.3,
            "lon": -56.2,
            "species_richness": 12450,
            "endemic_species": 3420,
            "threat_level": "High",
            "conservation_priority": 98,
            "climate_vulnerability": 89,
            "pollution_pressure": 74,
            "fragmentation_risk": 86,
            "protected_pct": 38,
            "carbon_density_t_ha": 310,
            "key_taxa": "River Dolphins, Jaguar, Harpy Eagle, Neotropical Primates",
            "engineering_directive": "Avoid instream hydro barriers; enforce mercury-free sediment containment and riparian buffer preservation.",
        },
        {
            "id": "sundarbans_delta",
            "name": "Sundarbans Mangrove Delta",
            "region": "South Asia",
            "biome": "Coastal Mangrove & Estuary",
            "lat": 21.9,
            "lon": 89.2,
            "species_richness": 3180,
            "endemic_species": 410,
            "threat_level": "Critical",
            "conservation_priority": 95,
            "climate_vulnerability": 95,
            "pollution_pressure": 82,
            "fragmentation_risk": 71,
            "protected_pct": 42,
            "carbon_density_t_ha": 420,
            "key_taxa": "Bengal Tiger, Estuarine Terrapin, Mangrove Flora, Irrawaddy Dolphin",
            "engineering_directive": "Replace rigid concrete seawalls with living mangrove breakwaters and zero-ballast-discharge shipping protocols.",
        },
        {
            "id": "coral_triangle",
            "name": "Raja Ampat & Coral Triangle",
            "region": "Southeast Asia",
            "biome": "Marine Reef & Archipelago",
            "lat": -0.5,
            "lon": 130.6,
            "species_richness": 9850,
            "endemic_species": 1540,
            "threat_level": "High",
            "conservation_priority": 97,
            "climate_vulnerability": 92,
            "pollution_pressure": 76,
            "fragmentation_risk": 54,
            "protected_pct": 31,
            "carbon_density_t_ha": 185,
            "key_taxa": "Scleractinian Corals, Reef Manta, Sea Turtles, Pelagic Fish",
            "engineering_directive": "Enforce turbidity curtains for coastal works, closed-loop desalination brine diffusion, and thermal effluent caps.",
        },
        {
            "id": "congo_cuvette",
            "name": "Cuvette Centrale Peatlands",
            "region": "Central Africa",
            "biome": "Tropical Peat Swamp Forest",
            "lat": 0.8,
            "lon": 17.6,
            "species_richness": 6910,
            "endemic_species": 1190,
            "threat_level": "High",
            "conservation_priority": 94,
            "climate_vulnerability": 79,
            "pollution_pressure": 52,
            "fragmentation_risk": 67,
            "protected_pct": 29,
            "carbon_density_t_ha": 680,
            "key_taxa": "Forest Elephant, Bonobo, Dwarf Crocodile, Peat Flora",
            "engineering_directive": "Prohibit peat drainage ditches; utilize pile-supported boardwalks and hydrological-continuity causeways.",
        },
        {
            "id": "mesoamerican_reef",
            "name": "Mesoamerican Barrier Lagoon",
            "region": "Central America",
            "biome": "Coastal Mangrove & Reef",
            "lat": 17.8,
            "lon": -87.9,
            "species_richness": 5420,
            "endemic_species": 680,
            "threat_level": "High",
            "conservation_priority": 89,
            "climate_vulnerability": 88,
            "pollution_pressure": 79,
            "fragmentation_risk": 64,
            "protected_pct": 35,
            "carbon_density_t_ha": 215,
            "key_taxa": "Elkhorn Coral, West Indian Manatee, Hawksbill Turtle",
            "engineering_directive": "Deploy nature-based dune nourishment, tertiary nutrient stripping for coastal wastewater, and dark-sky lighting.",
        },
        {
            "id": "serengeti_mara",
            "name": "Serengeti-Mara Savanna Corridor",
            "region": "East Africa",
            "biome": "Tropical Savanna & Grassland",
            "lat": -2.1,
            "lon": 34.8,
            "species_richness": 4680,
            "endemic_species": 510,
            "threat_level": "High",
            "conservation_priority": 92,
            "climate_vulnerability": 83,
            "pollution_pressure": 46,
            "fragmentation_risk": 91,
            "protected_pct": 48,
            "carbon_density_t_ha": 95,
            "key_taxa": "Wildebeest, African Wild Dog, Acacia Guild, Raptors",
            "engineering_directive": "Route regional rail outside seasonal migration paths; integrate 120m-wide wildlife overpasses every 6 km.",
        },
        {
            "id": "danube_floodplain",
            "name": "Lower Danube Wetland Corridor",
            "region": "Europe",
            "biome": "Temperate Floodplain Wetland",
            "lat": 45.1,
            "lon": 28.9,
            "species_richness": 3890,
            "endemic_species": 290,
            "threat_level": "Moderate",
            "conservation_priority": 84,
            "climate_vulnerability": 75,
            "pollution_pressure": 71,
            "fragmentation_risk": 76,
            "protected_pct": 52,
            "carbon_density_t_ha": 165,
            "key_taxa": "Beluga Sturgeon, Dalmatian Pelican, European Otter",
            "engineering_directive": "Restore dike setbacks for room-for-the-river flood attenuation and construct fish-passable bypass channels.",
        },
        {
            "id": "yellowstone_yukon",
            "name": "Northern Rockies Y2Y Spine",
            "region": "North America",
            "biome": "Temperate Conifer & Alpine",
            "lat": 51.2,
            "lon": -115.6,
            "species_richness": 2940,
            "endemic_species": 240,
            "threat_level": "Moderate",
            "conservation_priority": 86,
            "climate_vulnerability": 77,
            "pollution_pressure": 38,
            "fragmentation_risk": 82,
            "protected_pct": 44,
            "carbon_density_t_ha": 220,
            "key_taxa": "Grizzly Bear, Wolverine, Bull Trout, Whitebark Pine",
            "engineering_directive": "Construct vegetated highway eco-ducts with exclusionary fencing and de-icing salt runoff bio-swales.",
        },
        {
            "id": "cape_floristic",
            "name": "Cape Floristic Fynbos Belt",
            "region": "Southern Africa",
            "biome": "Mediterranean Shrubland",
            "lat": -33.9,
            "lon": 19.4,
            "species_richness": 9200,
            "endemic_species": 6210,
            "threat_level": "Critical",
            "conservation_priority": 95,
            "climate_vulnerability": 90,
            "pollution_pressure": 63,
            "fragmentation_risk": 85,
            "protected_pct": 21,
            "carbon_density_t_ha": 78,
            "key_taxa": "Protea Guild, Cape Sugarbird, Geometric Tortoise",
            "engineering_directive": "Enforce strict aquifer recharge protection, wildfire-resilient utility undergrounding, and invasive-clearing buffers.",
        },
        {
            "id": "great_bear_rainforest",
            "name": "Pacific Temperate Fjords",
            "region": "North America",
            "biome": "Temperate Coastal Rainforest",
            "lat": 52.5,
            "lon": -128.1,
            "species_richness": 3120,
            "endemic_species": 340,
            "threat_level": "Moderate",
            "conservation_priority": 85,
            "climate_vulnerability": 69,
            "pollution_pressure": 34,
            "fragmentation_risk": 62,
            "protected_pct": 57,
            "carbon_density_t_ha": 390,
            "key_taxa": "Kermode Bear, Pacific Salmon, Old-Growth Cedar",
            "engineering_directive": "Use full-span clear-water bridges over salmon spawning streams and electric marine port tug fleets.",
        },
        {
            "id": "mekong_tonle",
            "name": "Mekong-Tonle Sap Pulse Basin",
            "region": "Southeast Asia",
            "biome": "Tropical Freshwater Floodplain",
            "lat": 12.9,
            "lon": 104.1,
            "species_richness": 4760,
            "endemic_species": 790,
            "threat_level": "Critical",
            "conservation_priority": 93,
            "climate_vulnerability": 91,
            "pollution_pressure": 80,
            "fragmentation_risk": 89,
            "protected_pct": 26,
            "carbon_density_t_ha": 170,
            "key_taxa": "Mekong Giant Catfish, Sarus Crane, Flooded Forest",
            "engineering_directive": "Preserve natural flood-pulse hydrology; replace mainstream dams with floating solar + pumped-offstream storage.",
        },
    ]
    return pd.DataFrame(rows)


INFRASTRUCTURE_PROJECTS = {
    "High-Speed Electric Rail Corridor": {
        "base_habitat_loss": 18.0,
        "base_carbon_kt_yr": 42.0,
        "base_runoff_load": 26.0,
        "base_fragmentation": 54.0,
        "base_cost_musd": 480.0,
        "summary": "Inter-regional electrified rail replacing short-haul aviation and highway freight.",
    },
    "Regional Highway & Freight Expansion": {
        "base_habitat_loss": 34.0,
        "base_carbon_kt_yr": 128.0,
        "base_runoff_load": 62.0,
        "base_fragmentation": 78.0,
        "base_cost_musd": 360.0,
        "summary": "Multi-lane surface highway across peri-urban and forested catchments.",
    },
    "Riverine Hydroelectric & Storage Facility": {
        "base_habitat_loss": 41.0,
        "base_carbon_kt_yr": 55.0,
        "base_runoff_load": 48.0,
        "base_fragmentation": 84.0,
        "base_cost_musd": 620.0,
        "summary": "Impoundment dam and grid transmission corridor in a high-biodiversity watershed.",
    },
    "Utility Solar + Battery Microgrid Park": {
        "base_habitat_loss": 15.0,
        "base_carbon_kt_yr": -86.0,
        "base_runoff_load": 18.0,
        "base_fragmentation": 28.0,
        "base_cost_musd": 290.0,
        "summary": "Agrivoltaic & pollinator-compatible clean generation with BESS storage.",
    },
    "Coastal Port & Climate Seawall Upgrade": {
        "base_habitat_loss": 29.0,
        "base_carbon_kt_yr": 64.0,
        "base_runoff_load": 57.0,
        "base_fragmentation": 49.0,
        "base_cost_musd": 510.0,
        "summary": "Port resilience fortification exposed to storm surge and estuarine nursery habitats.",
    },
    "Circular Wastewater & Bio-Wetland Park": {
        "base_habitat_loss": 6.0,
        "base_carbon_kt_yr": -24.0,
        "base_runoff_load": -45.0,
        "base_fragmentation": 12.0,
        "base_cost_musd": 210.0,
        "summary": "Zero-liquid-discharge municipal treatment paired with constructed habitat wetlands.",
    },
}


ETHICAL_DILEMMAS = [
    {
        "id": "wetland_lithium",
        "title": "Case A: High-Voltage Clean Grid Line vs. Ramsar Wetland Sanctuary",
        "context": (
            "A 400 kV transmission corridor needed to deliver 1.8 GW of desert solar power cuts directly across "
            "a seasonal Ramsar wetland supporting 42 migratory waterbird species. Rerouting adds 18% capital cost "
            "and delays grid decarbonization by 14 months, while direct alignment risks electrocution and peat dewatering."
        ),
        "options": {
            "Direct Overhead Towers (Lowest Cost & Fastest Schedule)": {
                "precautionary": 22,
                "intergenerational": 48,
                "ecological": 18,
                "justice": 35,
                "integrity": 40,
                "co2_delta": -92,
                "biodiversity_delta": -38,
                "pollution_delta": -14,
                "cost_premium_pct": 0,
                "verdict": "Fails the mitigation hierarchy (avoidance skipped) and locks in avian mortality.",
            },
            "Perimeter Reroute + Elevated Monopoles + Avian Diverters": {
                "precautionary": 82,
                "intergenerational": 88,
                "ecological": 84,
                "justice": 80,
                "integrity": 90,
                "co2_delta": -84,
                "biodiversity_delta": 12,
                "pollution_delta": 8,
                "cost_premium_pct": 14,
                "verdict": "Strong ethical alignment: applies avoidance first while preserving net climate gains.",
            },
            "HDD Underground Cable Under Wetland + Peat Restoration Offset": {
                "precautionary": 94,
                "intergenerational": 92,
                "ecological": 91,
                "justice": 86,
                "integrity": 93,
                "co2_delta": -81,
                "biodiversity_delta": 24,
                "pollution_delta": 14,
                "cost_premium_pct": 24,
                "verdict": "Gold-standard precautionary engineering: eliminates collision risk and enhances wetland hydrology.",
            },
        },
    },
    {
        "id": "desal_coral",
        "title": "Case B: Drought-Relief Desalination Outfall Near Coral Nursery",
        "context": (
            "A coastal municipality faces severe freshwater scarcity under prolonged drought. The proposed reverse-osmosis "
            "desalination plant discharges hypersaline brine (70 ppt) and anti-scalant chemicals 600 m from a recovering "
            "coral reef nursery that sustains local artisanal fisheries."
        ),
        "options": {
            "Standard Nearshore Single-Pipe Outfall": {
                "precautionary": 18,
                "intergenerational": 36,
                "ecological": 15,
                "justice": 25,
                "integrity": 32,
                "co2_delta": 28,
                "biodiversity_delta": -45,
                "pollution_delta": -42,
                "cost_premium_pct": 0,
                "verdict": "Transfers municipal water stress onto marine ecosystems and fishing communities.",
            },
            "Deep-Diffuser Array + Solar Energy Recovery + Brine Dilution": {
                "precautionary": 76,
                "intergenerational": 80,
                "ecological": 74,
                "justice": 78,
                "integrity": 85,
                "co2_delta": -18,
                "biodiversity_delta": 4,
                "pollution_delta": 22,
                "cost_premium_pct": 16,
                "verdict": "Substantially reduces benthic salinity spikes and cuts fossil energy footprint.",
            },
            "Zero-Liquid-Discharge Mineral Recovery + Municipal Greywater Reuse First": {
                "precautionary": 95,
                "intergenerational": 96,
                "ecological": 94,
                "justice": 92,
                "integrity": 95,
                "co2_delta": -32,
                "biodiversity_delta": 28,
                "pollution_delta": 48,
                "cost_premium_pct": 27,
                "verdict": "Exemplifies circular pollution prevention and demand-side stewardship.",
            },
        },
    },
    {
        "id": "alpine_tunnel",
        "title": "Case C: Mountain Highway Cut vs. Endemic Amphibian Catchment",
        "context": (
            "An aging mountain pass suffers frequent landslides. A proposed open-cut highway widening exposes pyritic rock "
            "capable of acid rock drainage into headwater streams with endemic salamanders."
        ),
        "options": {
            "Open-Cut Rock Blasting + Roadside Settling Ponds": {
                "precautionary": 24,
                "intergenerational": 32,
                "ecological": 20,
                "justice": 42,
                "integrity": 38,
                "co2_delta": 19,
                "biodiversity_delta": -41,
                "pollution_delta": -39,
                "cost_premium_pct": 0,
                "verdict": "High risk of chronic heavy-metal leaching and irreversible stream acidification.",
            },
            "Bored Twin-Tube Tunnel + Wildlife Canopy Overpass Above Portal": {
                "precautionary": 91,
                "intergenerational": 93,
                "ecological": 90,
                "justice": 85,
                "integrity": 92,
                "co2_delta": -15,
                "biodiversity_delta": 22,
                "pollution_delta": 35,
                "cost_premium_pct": 22,
                "verdict": "Preserves surface catchment continuity, eliminates acid-rock exposure, and restores wildlife passage.",
            },
            "Geosynthetic Bio-Reinforced Viaduct + Neutralizing Wetland": {
                "precautionary": 80,
                "intergenerational": 84,
                "ecological": 79,
                "justice": 82,
                "integrity": 86,
                "co2_delta": -8,
                "biodiversity_delta": 14,
                "pollution_delta": 26,
                "cost_premium_pct": 13,
                "verdict": "Balanced landslide resilience with strong surface-flow and aquatic protection.",
            },
        },
    },
]


SPECIES_PROFILES = {
    "Asian Elephant (Wide-Ranging Herbivore)": {
        "road_penalty": 28.0,
        "urban_penalty": 45.0,
        "river_penalty": 3.5,
        "forest_cost": 1.0,
        "buffer_cost": 1.8,
        "overpass_bonus_cost": 1.4,
        "underpass_bonus_cost": 4.0,
        "edge_sensitivity": 0.72,
        "note": "Requires wide vegetated eco-ducts (>= 60 m width) and low-noise buffers away from settlements.",
    },
    "Grey Wolf / Large Carnivore": {
        "road_penalty": 22.0,
        "urban_penalty": 38.0,
        "river_penalty": 2.8,
        "forest_cost": 1.0,
        "buffer_cost": 1.5,
        "overpass_bonus_cost": 1.3,
        "underpass_bonus_cost": 2.2,
        "edge_sensitivity": 0.65,
        "note": "Uses both vegetated overpasses and broad box culverts when human disturbance is minimized.",
    },
    "Spotted Salamander / Riparian Amphibian": {
        "road_penalty": 35.0,
        "urban_penalty": 50.0,
        "river_penalty": 0.9,
        "forest_cost": 1.2,
        "buffer_cost": 1.6,
        "overpass_bonus_cost": 3.5,
        "underpass_bonus_cost": 1.1,
        "edge_sensitivity": 0.90,
        "note": "Highly sensitive to road desiccation and runoff; prefers shaded moist riparian underpasses.",
    },
    "Monarch & Native Pollinator Network": {
        "road_penalty": 8.0,
        "urban_penalty": 18.0,
        "river_penalty": 1.4,
        "forest_cost": 1.1,
        "buffer_cost": 1.0,
        "overpass_bonus_cost": 1.2,
        "underpass_bonus_cost": 5.5,
        "edge_sensitivity": 0.45,
        "note": "Thrives on connected meadow stepping-stones, pesticide-free verges, and sunlit vegetated bridges.",
    },
}


CHALLENGE_QUESTIONS = [
    {
        "id": 1,
        "domain": "Precautionary Principle",
        "difficulty": "Foundation",
        "scenario": (
            "An industrial park proposes releasing a newly formulated fluorinated surfactant into a municipal treatment "
            "plant. Chronic aquatic toxicity studies are incomplete, though persistence indicators resemble legacy PFAS."
        ),
        "question": "Which engineering action best upholds the Precautionary Principle?",
        "options": [
            "Approve discharge under existing legacy TSS/BOD permit limits until harm is proven.",
            "Require closed-loop pretreatment and thermal/membrane destruction before any discharge permit.",
            "Dilute effluent with river intake water during peak monsoon flow.",
            "Allow a 5-year trial discharge monitored only by downstream fish counts.",
        ],
        "correct_idx": 1,
        "rationale": (
            "When scientific evidence suggests plausible, irreversible environmental persistence, engineering ethics "
            "requires source-level prevention (closed-loop pretreatment) rather than dilution or waiting for ecological damage."
        ),
    },
    {
        "id": 2,
        "domain": "Biodiversity Hierarchy",
        "difficulty": "Intermediate",
        "scenario": (
            "A solar farm developer offers to fund planting 50 hectares of non-native monoculture eucalyptus elsewhere "
            "in exchange for clearing 12 hectares of primary old-growth grassland containing endemic orchids."
        ),
        "question": "Why does this proposal violate ethical biodiversity engineering standards?",
        "options": [
            "It skips the Avoidance step of the Mitigation Hierarchy and substitutes incomparable non-native habitat.",
            "Eucalyptus plantations sequester too much carbon to qualify for offsets.",
            "Solar farms always require at least a 10:1 tree planting ratio.",
            "Endemic orchids are only protected inside urban parks.",
        ],
        "correct_idx": 0,
        "rationale": (
            "The Mitigation Hierarchy mandates Avoid -> Minimize -> Restore -> Offset as a last resort, and 'like-for-like' "
            "ecological equivalence—monoculture trees cannot replace irreplaceable old-growth endemic grassland."
        ),
    },
    {
        "id": 3,
        "domain": "Professional Integrity",
        "difficulty": "Intermediate",
        "scenario": (
            "During commissioning of a landfill leachate liner, you discover a contractor welded seams below specification "
            "in a zone overlying a drinking-water aquifer. Project management urges sign-off to avoid a 3-week penalty."
        ),
        "question": "What is your primary ethical obligation under civil & environmental engineering codes?",
        "options": [
            "Sign off conditionally and note the defect in an internal private memo.",
            "Withhold sign-off, document the non-conformance transparently, and require full repair and re-testing.",
            "Install one extra downstream monitoring well and proceed with waste placement.",
            "Defer the technical judgment entirely to the project's financial sponsor.",
        ],
        "correct_idx": 1,
        "rationale": (
            "Engineers hold paramount public health, safety, and environmental welfare. Signing off on known containment "
            "defects endangers groundwater for decades and violates professional integrity."
        ),
    },
    {
        "id": 4,
        "domain": "Climate Resilience",
        "difficulty": "Foundation",
        "scenario": (
            "A coastal stormwater pump station is designed with a 50-year service life using only historical 1960-2000 "
            "rainfall intensity curves, ignoring projected sea-level rise and extreme precipitation intensification."
        ),
        "question": "What is the key future-proof engineering flaw in this design?",
        "options": [
            "Using historical stationarity assumes past climate extremes bound future risks, causing systemic failure.",
            "Pump stations should always be sized exclusively for 2-year storm events.",
            "Sea-level rise does not affect gravity stormwater outfalls.",
            "Concrete structures degrade slower in saltwater.",
        ],
        "correct_idx": 0,
        "rationale": (
            "Climate non-stationarity means future-proof infrastructure must incorporate downscaled climate projections, "
            "adaptive freeboard, and nature-based retention buffers."
        ),
    },
    {
        "id": 5,
        "domain": "Environmental Justice",
        "difficulty": "Advanced",
        "scenario": (
            "A city compares two sites for a regional biosolids incineration and transfer station: an affluent hillside "
            "with high land cost or an already pollution-burdened riverside neighborhood with lower land value."
        ),
        "question": "How should an ethical environmental siting assessment treat the riverside neighborhood?",
        "options": [
            "Select it solely because land acquisition minimizes municipal bond costs.",
            "Apply cumulative burden analysis, meaningful community consent, and zero-emission alternative evaluation.",
            "Ignore existing air-quality baselines because each facility is regulated separately.",
            "Offer a one-time park bench donation without changing stack emissions.",
        ],
        "correct_idx": 1,
        "rationale": (
            "Environmental justice requires evaluating cumulative pollution loads so vulnerable communities are not treated "
            "as sacrifice zones, prioritizing cleaner non-incineration/anaerobic digestion alternatives and FPIC."
        ),
    },
    {
        "id": 6,
        "domain": "Pollution Prevention",
        "difficulty": "Intermediate",
        "scenario": (
            "A highway widening project borders a salmon-bearing river. Heavy metals, microplastics from tire wear, "
            "and hydrocarbons will wash off the expanded pavement during storms."
        ),
        "question": "Which stormwater design delivers the strongest ecological protection?",
        "options": [
            "Direct concrete curb-and-gutter discharge pipes straight into the main river channel.",
            "Vegetated bio-retention swales with engineered biochar/sand media and sediment forebays.",
            "Painting road lanes white to reflect solar radiation.",
            "Increasing culvert velocity to flush pollutants rapidly downstream.",
        ],
        "correct_idx": 1,
        "rationale": (
            "Bio-retention swales with engineered sorptive media capture fine particulates, tire-wear toxins (e.g., 6PPD-quinone), "
            "and hydrocarbons before runoff reaches sensitive aquatic spawning habitats."
        ),
    },
    {
        "id": 7,
        "domain": "Biodiversity Hierarchy",
        "difficulty": "Advanced",
        "scenario": (
            "An elevated coastal highway includes bright unshielded 5000K white LED floodlights next to a sea-turtle "
            "nesting beach and nocturnal insect corridor."
        ),
        "question": "What engineering modification prevents ecological light pollution while keeping road safety?",
        "options": [
            "Double pole height so light spreads farther across the dunes.",
            "Install full-cutoff, warm amber (<2200K) adaptive shielded luminaires with motion dimming.",
            "Switch to unshielded ultraviolet-rich lamps.",
            "Leave floodlights on at 100% power all night for visibility.",
        ],
        "correct_idx": 1,
        "rationale": (
            "Full-cutoff warm amber (<2200K) shielded lighting preserves human roadway safety while avoiding disorientation "
            "of sea-turtle hatchlings and collapse of nocturnal pollinator populations."
        ),
    },
    {
        "id": 8,
        "domain": "Climate Resilience",
        "difficulty": "Advanced",
        "scenario": (
            "Comparing structural concrete options for a marine bridge deck: Portland cement mix vs. supplementary "
            "cementitious slag/calcined-clay geopolymer mix with recycled aggregate and carbon-cured rebar protection."
        ),
        "question": "Why does lifecycle embodied-carbon optimization matter alongside operational energy?",
        "options": [
            "Upfront embodied emissions occur immediately in the critical near-term warming window and drive resource extraction.",
            "Operational energy is never relevant for bridges.",
            "Higher embodied carbon automatically doubles structural durability.",
            "Recycled aggregates eliminate the need for structural load testing.",
        ],
        "correct_idx": 0,
        "rationale": (
            "Infrastructure materials create an immediate carbon pulse upon construction; low-carbon binders and circular "
            "aggregates cut near-term emissions while reducing mining pressure on quarry habitats."
        ),
    },
]

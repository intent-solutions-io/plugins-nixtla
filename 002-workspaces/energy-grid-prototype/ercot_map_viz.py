#!/usr/bin/env python3
"""
ERCOT Grid Map Visualization
============================
Interactive map showing ERCOT weather zones with forecast overlays.

Part of: 121-AA-REPT Energy Grid Forecasting Opportunity Research
"""

import json
from datetime import datetime

import folium
import pandas as pd
from folium import plugins

# ============================================================================
# ERCOT WEATHER ZONES (approximate center coordinates)
# ============================================================================

# ERCOT has 8 weather zones
ERCOT_ZONES = {
    "COAST": {
        "name": "Coast",
        "lat": 29.3013,
        "lon": -94.7977,
        "cities": ["Houston", "Galveston", "Beaumont"],
        "color": "#1f77b4",
    },
    "EAST": {
        "name": "East",
        "lat": 31.7619,
        "lon": -95.6308,
        "cities": ["Tyler", "Longview", "Nacogdoches"],
        "color": "#ff7f0e",
    },
    "FAR_WEST": {
        "name": "Far West",
        "lat": 31.1060,
        "lon": -104.0214,
        "cities": ["El Paso", "Midland", "Odessa"],
        "color": "#2ca02c",
    },
    "NORTH": {
        "name": "North",
        "lat": 33.0198,
        "lon": -96.6989,
        "cities": ["Dallas", "Fort Worth", "Denton"],
        "color": "#d62728",
    },
    "NORTH_CENTRAL": {
        "name": "North Central",
        "lat": 32.0853,
        "lon": -97.5672,
        "cities": ["Waco", "Killeen", "Temple"],
        "color": "#9467bd",
    },
    "SOUTH_CENTRAL": {
        "name": "South Central",
        "lat": 29.4241,
        "lon": -98.4936,
        "cities": ["San Antonio", "Austin", "New Braunfels"],
        "color": "#8c564b",
    },
    "SOUTHERN": {
        "name": "Southern",
        "lat": 26.2034,
        "lon": -98.2300,
        "cities": ["Corpus Christi", "McAllen", "Brownsville"],
        "color": "#e377c2",
    },
    "WEST": {
        "name": "West",
        "lat": 31.4638,
        "lon": -100.4370,
        "cities": ["Abilene", "San Angelo", "Lubbock"],
        "color": "#7f7f7f",
    },
}

# Major transmission corridors (simplified - approximate routes)
TRANSMISSION_CORRIDORS = [
    # North-South backbone
    {
        "start": (33.0198, -96.6989),
        "end": (29.4241, -98.4936),
        "voltage": "345kV",
        "name": "Dallas-SA Corridor",
    },
    {
        "start": (29.4241, -98.4936),
        "end": (29.3013, -94.7977),
        "voltage": "345kV",
        "name": "SA-Houston Corridor",
    },
    {
        "start": (33.0198, -96.6989),
        "end": (29.3013, -94.7977),
        "voltage": "345kV",
        "name": "Dallas-Houston Corridor",
    },
    # East-West ties
    {
        "start": (31.4638, -100.4370),
        "end": (33.0198, -96.6989),
        "voltage": "345kV",
        "name": "West-North Corridor",
    },
    {
        "start": (31.4638, -100.4370),
        "end": (29.4241, -98.4936),
        "voltage": "345kV",
        "name": "West-SC Corridor",
    },
    # Far West connection
    {
        "start": (31.1060, -104.0214),
        "end": (31.4638, -100.4370),
        "voltage": "345kV",
        "name": "Far West Tie",
    },
]


def create_base_map():
    """Create base folium map centered on Texas."""
    # Center on Texas
    texas_center = [31.0, -99.5]

    m = folium.Map(
        location=texas_center,
        zoom_start=6,
        tiles="cartodbpositron",  # Clean, light basemap
    )

    # Add fullscreen control
    plugins.Fullscreen().add_to(m)

    return m


def add_weather_zones(m, forecast_data=None):
    """Add ERCOT weather zones as circle markers."""

    for zone_id, zone in ERCOT_ZONES.items():
        # Default values
        load_mw = 0
        forecast_mw = 0
        change_pct = 0

        # If we have forecast data, use it
        if forecast_data is not None and zone_id in forecast_data:
            load_mw = forecast_data[zone_id].get("current_load", 0)
            forecast_mw = forecast_data[zone_id].get("forecast_load", 0)
            change_pct = forecast_data[zone_id].get("change_pct", 0)

        # Popup content
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0 0 10px 0; color: {zone['color']};">
                {zone['name']} Zone
            </h4>
            <p style="margin: 5px 0;"><b>Cities:</b> {', '.join(zone['cities'])}</p>
            <hr style="margin: 10px 0;">
            <p style="margin: 5px 0;"><b>Current Load:</b> {load_mw:,.0f} MW</p>
            <p style="margin: 5px 0;"><b>48h Forecast:</b> {forecast_mw:,.0f} MW</p>
            <p style="margin: 5px 0; color: {'green' if change_pct < 0 else 'red'};">
                <b>Change:</b> {change_pct:+.1f}%
            </p>
        </div>
        """

        # Circle size based on load (or fixed if no data)
        radius = 30000 if load_mw == 0 else max(15000, min(50000, load_mw * 0.5))

        folium.Circle(
            location=[zone["lat"], zone["lon"]],
            radius=radius,
            color=zone["color"],
            fill=True,
            fillColor=zone["color"],
            fillOpacity=0.4,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{zone['name']} Zone",
        ).add_to(m)

        # Add zone label
        folium.Marker(
            location=[zone["lat"], zone["lon"]],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 12px;
                    font-weight: bold;
                    color: {zone['color']};
                    text-shadow: 1px 1px 2px white, -1px -1px 2px white;
                    white-space: nowrap;
                ">
                    {zone['name']}
                </div>
                """,
                icon_size=(100, 20),
                icon_anchor=(50, 10),
            ),
        ).add_to(m)

    return m


def add_transmission_lines(m):
    """Add simplified transmission corridor lines."""

    for corridor in TRANSMISSION_CORRIDORS:
        folium.PolyLine(
            locations=[corridor["start"], corridor["end"]],
            color="#FFD700",  # Gold/yellow for transmission
            weight=3,
            opacity=0.7,
            tooltip=f"{corridor['name']} ({corridor['voltage']})",
        ).add_to(m)

    return m


def add_legend(m):
    """Add a legend to the map."""

    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        z-index: 1000;
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        border: 2px solid gray;
        font-family: Arial;
        font-size: 12px;
    ">
        <h4 style="margin: 0 0 10px 0;">ERCOT Grid Forecast</h4>
        <p style="margin: 5px 0;">
            <span style="color: #FFD700; font-weight: bold;">━━━</span> Transmission Corridor
        </p>
        <p style="margin: 5px 0;">
            <span style="display: inline-block; width: 15px; height: 15px;
                         background-color: #1f77b4; border-radius: 50%;
                         vertical-align: middle;"></span> Weather Zone
        </p>
        <hr style="margin: 10px 0;">
        <p style="margin: 5px 0; font-size: 10px; color: gray;">
            Circle size = Load magnitude<br>
            Click zones for forecast details
        </p>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    return m


def add_title(m, title="ERCOT Grid 48-Hour Load Forecast"):
    """Add a title to the map."""

    title_html = f"""
    <div style="
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background-color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: 2px solid #333;
        font-family: Arial;
        font-size: 18px;
        font-weight: bold;
    ">
        {title}
        <span style="font-size: 12px; font-weight: normal; color: gray;">
            | {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </span>
    </div>
    """

    m.get_root().html.add_child(folium.Element(title_html))
    return m


def generate_mock_forecast_data():
    """Generate mock forecast data for demonstration."""
    import random

    # Simulate realistic load values (MW) for each zone
    base_loads = {
        "COAST": 18000,  # Houston metro - highest
        "NORTH": 15000,  # Dallas-FW metro
        "SOUTH_CENTRAL": 12000,  # Austin-SA corridor
        "EAST": 5000,
        "NORTH_CENTRAL": 6000,
        "SOUTHERN": 4000,
        "WEST": 3000,
        "FAR_WEST": 2000,  # Lowest population
    }

    forecast_data = {}
    for zone_id, base in base_loads.items():
        current = base * random.uniform(0.9, 1.1)
        forecast = current * random.uniform(0.95, 1.15)
        change_pct = ((forecast - current) / current) * 100

        forecast_data[zone_id] = {
            "current_load": current,
            "forecast_load": forecast,
            "change_pct": change_pct,
        }

    return forecast_data


def create_ercot_forecast_map(forecast_data=None, output_path="ercot_forecast_map.html"):
    """Create complete ERCOT forecast map."""

    print("Creating ERCOT forecast map...")

    # Use mock data if none provided
    if forecast_data is None:
        print("  Using mock forecast data for demonstration")
        forecast_data = generate_mock_forecast_data()

    # Build map
    m = create_base_map()
    m = add_transmission_lines(m)
    m = add_weather_zones(m, forecast_data)
    m = add_legend(m)
    m = add_title(m)

    # Save
    m.save(output_path)
    print(f"  Saved to {output_path}")

    # Calculate totals
    total_current = sum(z["current_load"] for z in forecast_data.values())
    total_forecast = sum(z["forecast_load"] for z in forecast_data.values())
    total_change = ((total_forecast - total_current) / total_current) * 100

    print(f"\nERCOT System Summary:")
    print(f"  Current Load:  {total_current:,.0f} MW")
    print(f"  48h Forecast:  {total_forecast:,.0f} MW")
    print(f"  Change:        {total_change:+.1f}%")

    return m, forecast_data


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    m, data = create_ercot_forecast_map(output_path="ercot_forecast_map.html")
    print("\nOpen ercot_forecast_map.html in a browser to view!")

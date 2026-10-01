import asyncio
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.graph.travel_graph import travel_graph

async def main():
    initial_state = {
        "start_location": "Vijayawada",
        "destination": "Kerala",
        "budget": 25000,
        "start_date": "2026-09-25",
        "end_date": "2026-09-29",
        "duration_days": 5,
        "travelers": 2,
        "interests": ["Historical", "Food", "Nature"],
        "style": "Balanced",
        "transport_pref": "No preference",
        "hotel_pref": "Standard",
        "num_days": 5
    }

    res = await travel_graph.ainvoke(initial_state)

    print("=== DATES & PARAMS ===")
    print(f"Num Days: {res.get('num_days')}")
    print(f"Start Date: {res.get('start_date')}, End Date: {res.get('end_date')}")

    print("\n=== WEATHER FORECAST ===")
    print(f"Current: {res.get('current_weather')}")
    print(f"Daily forecast count: {len(res.get('weather_forecast', []))}")

    print("\n=== DAY-BY-DAY ITINERARY ===")
    for day in res.get("itinerary", []):
        print(f"\n--- {day.get('day_label')} ---")
        print(f"Theme: {day.get('theme')}")
        print(f"Weather: {day.get('weather_condition')} ({day.get('temp')})")
        for act in day.get("schedule", []):
            print(f"  [{act['time']}] {act['activity']}")
            print(f"    Details: {act['details']}")
            print(f"    Maps URL: {act['google_maps_url']}")

    print("\n=== ATTRACTIONS / PLACES TO VISIT ===")
    for attr in res.get("attractions", []):
        print(f"  - {attr['name']} ({attr['category']}) | Maps: {attr['google_maps_url']}")

    print("\n=== SELECTED HOTEL ===")
    hotel = res.get("selected_hotel", {})
    print(f"  {hotel.get('name')} | Rate: ₹{hotel.get('price_per_night')} | Maps: {hotel.get('google_maps_url')}")

    print("\n=== BUDGET BREAKDOWN ===")
    print(json.dumps(res.get("budget_breakdown", {}), indent=2))

if __name__ == "__main__":
    asyncio.run(main())

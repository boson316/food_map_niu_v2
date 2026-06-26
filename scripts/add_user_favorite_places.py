"""將 user_favorites 對應店家 merge 進 places 快取（缺欄位時補齊）。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_PLACES: list[dict] = [
    {
        "id": "ChIJ8_LTgunkZzRr-w6QFA_oqeQ",
        "name": "巧食坊宜大店",
        "lat": 24.7471575,
        "lon": 121.7486105,
        "rating": 3.8,
        "review_count": 184,
        "category": "chinese_noodle_restaurant",
        "price_level": 1,
        "food_groups": ["麵食類"],
        "business_status": "OPERATIONAL",
        "regular_opening_hours": {
            "periods": [
                *[
                    period
                    for day in range(1, 6)
                    for period in (
                        {
                            "open": {"day": day, "hour": 11, "minute": 0},
                            "close": {"day": day, "hour": 14, "minute": 30},
                        },
                        {
                            "open": {"day": day, "hour": 16, "minute": 0},
                            "close": {"day": day, "hour": 19, "minute": 30},
                        },
                    )
                ],
                {
                    "open": {"day": 6, "hour": 11, "minute": 0},
                    "close": {"day": 6, "hour": 14, "minute": 30},
                },
                {
                    "open": {"day": 6, "hour": 17, "minute": 0},
                    "close": {"day": 6, "hour": 19, "minute": 30},
                },
            ]
        },
    },
    {
        "id": "ChIJK0K7CenkZzTSkSZ5COxxV-Q",
        "name": "甜屋義大利麵",
        "lat": 24.7466374,
        "lon": 121.7499517,
        "rating": 4.1,
        "review_count": 137,
        "category": "italian_restaurant",
        "price_level": 1,
        "food_groups": ["義式披薩類"],
        "business_status": "OPERATIONAL",
        "regular_opening_hours": {
            "periods": [
                {
                    "open": {"day": day, "hour": 11, "minute": 0},
                    "close": {"day": day, "hour": 20, "minute": 30},
                }
                for day in range(7)
            ]
        },
    },
    {
        "id": "ChIJb05af7LlZzSx0ZNFYwc8fuQ",
        "name": "布麥加",
        "lat": 24.7466987,
        "lon": 121.7497404,
        "rating": 4.9,
        "review_count": 270,
        "category": "meal_takeaway",
        "price_level": 1,
        "food_groups": ["便當類"],
        "business_status": "OPERATIONAL",
    },
    {
        "id": "ChIJ1Q9EsVPlZzTSmgm6wnKi4uQ",
        "name": "鴨米港式燒臘便當",
        "lat": 24.7466276,
        "lon": 121.7510713,
        "rating": 4.6,
        "review_count": 88,
        "category": "chinese_restaurant",
        "price_level": 1,
        "food_groups": ["燒腊港式類"],
        "business_status": "OPERATIONAL",
        "regular_opening_hours": {
            "periods": [
                *[
                    period
                    for day in (0, 1, 2, 3, 4)
                    for period in (
                        {
                            "open": {"day": day, "hour": 10, "minute": 30},
                            "close": {"day": day, "hour": 13, "minute": 30},
                        },
                        {
                            "open": {"day": day, "hour": 16, "minute": 30},
                            "close": {"day": day, "hour": 19, "minute": 30},
                        },
                    )
                ],
                {
                    "open": {"day": 5, "hour": 10, "minute": 30},
                    "close": {"day": 5, "hour": 13, "minute": 30},
                },
            ]
        },
    },
]


def merge_into_cache(path: Path) -> tuple[int, int]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"{path} must be a JSON array")

    by_id = {str(row["id"]): row for row in rows if isinstance(row, dict) and row.get("id")}
    added = 0
    updated = 0
    for place in NEW_PLACES:
        existing = by_id.get(place["id"])
        if existing is None:
            rows.append(place)
            by_id[place["id"]] = place
            added += 1
            continue
        changed = False
        for key, value in place.items():
            if existing.get(key) != value:
                existing[key] = value
                changed = True
        if changed:
            updated += 1

    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return added, updated


def main() -> int:
    targets = [ROOT / "data" / "places_cache.public.json", ROOT / "data" / "places_cache.json"]
    for path in targets:
        if not path.is_file():
            print(f"skip missing: {path}")
            continue
        added, updated = merge_into_cache(path)
        print(f"{path.name}: +{added} new, ~{updated} updated, total {len(json.loads(path.read_text(encoding='utf-8')))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

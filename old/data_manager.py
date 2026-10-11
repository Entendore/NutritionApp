"""
NutriTrack — Local JSON data manager.
Handles all persistence: goals, food database, diary log, water tracking.
"""

import json, os
from datetime import date, timedelta

from constants import MEAL_CATS


class DataManager:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "nutritrack_data.json")
        self.data = self._load()

    # ── Load / Save ────────────────────────────────────────────────────────

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "goals": {
                "calories": 2000, "protein": 150, "carbs": 250,
                "fat": 65, "fiber": 30, "water": 8
            },
            "log": {},
            "foods": {}
        }

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    # ── Day ────────────────────────────────────────────────────────────────

    def today_key(self):
        return date.today().isoformat()

    def get_day(self, dk=None):
        if dk is None:
            dk = self.today_key()
        if dk not in self.data["log"]:
            self.data["log"][dk] = {"meals": {c: [] for c in MEAL_CATS}, "water": 0}
        return self.data["log"][dk]

    def get_totals(self, dk=None):
        day = self.get_day(dk)
        t = {"cal": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
        for cat in MEAL_CATS:
            for e in day["meals"][cat]:
                for k in t:
                    t[k] += e.get(k, 0)
        for k in t:
            t[k] = round(t[k], 1)
        return t

    # ── Food DB ────────────────────────────────────────────────────────────

    def get_foods(self):
        return self.data.get("foods", {})

    def get_food(self, name):
        return self.data.get("foods", {}).get(name)

    def add_food(self, name, cat, cal, pro, carb, fat, fib, srv, unit):
        self.data["foods"][name] = {
            "category": cat, "cal": float(cal),
            "protein": float(pro), "carbs": float(carb), "fat": float(fat),
            "fiber": float(fib), "serving": float(srv), "unit": unit
        }
        self.save()

    def update_food(self, old_name, name, cat, cal, pro, carb, fat, fib, srv, unit):
        if old_name in self.data["foods"]:
            del self.data["foods"][old_name]
        self.add_food(name, cat, cal, pro, carb, fat, fib, srv, unit)

    def delete_food(self, name):
        if name in self.data.get("foods", {}):
            del self.data["foods"][name]
            self.save()

    # ── Diary ──────────────────────────────────────────────────────────────

    def log_food(self, meal, name, servings, dk=None):
        fi = self.get_food(name)
        if not fi:
            return False
        entry = {
            "name": name, "servings": round(servings, 2),
            "cal":     round(fi["cal"]     * servings, 1),
            "protein": round(fi["protein"] * servings, 1),
            "carbs":   round(fi["carbs"]   * servings, 1),
            "fat":     round(fi["fat"]     * servings, 1),
            "fiber":   round(fi["fiber"]   * servings, 1),
            "unit":    fi["unit"]
        }
        self.get_day(dk)["meals"][meal].append(entry)
        self.save()
        return True

    def remove_entry(self, meal, idx, dk=None):
        day = self.get_day(dk)
        if 0 <= idx < len(day["meals"][meal]):
            day["meals"][meal].pop(idx)
            self.save()

    # ── Water ──────────────────────────────────────────────────────────────

    def add_water(self, dk=None):
        day = self.get_day(dk)
        day["water"] = min(day.get("water", 0) + 1, 20)
        self.save()

    def rem_water(self, dk=None):
        day = self.get_day(dk)
        day["water"] = max(day.get("water", 0) - 1, 0)
        self.save()

    def get_water(self, dk=None):
        return self.get_day(dk).get("water", 0)

    # ── Goals ──────────────────────────────────────────────────────────────

    def set_goals(self, **kw):
        self.data["goals"] = {k: int(v) for k, v in kw.items()}
        self.save()

    def get_goals(self):
        return self.data["goals"]

    # ── History ────────────────────────────────────────────────────────────

    def get_dates(self):
        return sorted(self.data["log"].keys(), reverse=True)[:60]

    def clear_day(self, dk=None):
        if dk is None:
            dk = self.today_key()
        self.data["log"][dk] = {"meals": {c: [] for c in MEAL_CATS}, "water": 0}
        self.save()
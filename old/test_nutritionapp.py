"""
NutriTrack — Pytest Test Suite
Tests all features: Data persistence, Food DB, Diary logging, Water tracking, 
Goals, History, Education content, and Constants.
"""

import sys
import os
import json
import pytest
from unittest.mock import MagicMock, patch

# ═══════════════════════════════════════════════════════════════════════════════
# CRITICAL: Mock Kivy Window before ANY Kivy modules are imported.
# This prevents "Unable to find any valuable Window provider" errors in pytest.
# ═══════════════════════════════════════════════════════════════════════════════

if 'kivy.core.window' not in sys.modules:
    sys.modules['kivy.core.window'] = MagicMock()

# Now we can safely import our app modules
from constants import C, MEAL_CATS, FOOD_CATS
from education_content import EDU_TOPICS
from data_manager import DataManager


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def dm(tmp_path):
    """Provides a DataManager instance that saves to a temporary directory."""
    file_path = tmp_path / "test_nutritrack_data.json"
    
    # Instantiate and override the path to use the temp directory
    manager = DataManager()
    manager.path = str(file_path)
    
    # Reset to default clean state for testing
    manager.data = {
        "goals": {"calories": 2000, "protein": 150, "carbs": 250,
                  "fat": 65, "fiber": 30, "water": 8},
        "log": {},
        "foods": {}
    }
    manager.save()
    return manager


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: CONSTANTS & EDUCATION CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

class TestConstants:
    def test_color_palette_exists(self):
        assert 'pri' in C
        assert 'bg' in C
        assert 'card' in C
        assert len(C['pri']) == 4  # RGBA format

    def test_meal_categories(self):
        assert len(MEAL_CATS) == 4
        assert 'Breakfast' in MEAL_CATS

    def test_food_categories(self):
        assert len(FOOD_CATS) == 12
        assert 'Proteins' in FOOD_CATS


class TestEducationContent:
    def test_topics_are_list(self):
        assert isinstance(EDU_TOPICS, list)
        assert len(EDU_TOPICS) > 0

    def test_topic_structure(self):
        for topic in EDU_TOPICS:
            assert 'title' in topic
            assert 'icon' in topic
            # Must have either sections or a calculator flag
            assert 'sections' in topic or topic.get('calculator') is True

    def test_calculator_topic_exists(self):
        calc_topics = [t for t in EDU_TOPICS if t.get('calculator')]
        assert len(calc_topics) == 1
        assert calc_topics[0]['title'] == 'BMI & TDEE Calculator'

    def test_sections_structure(self):
        for topic in EDU_TOPICS:
            if 'sections' in topic:
                for section in topic['sections']:
                    assert len(section) == 2  # (Title, Content)
                    assert isinstance(section[0], str)
                    assert isinstance(section[1], str)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: DATA MANAGER - CORE
# ═══════════════════════════════════════════════════════════════════════════════

class TestDataManagerCore:
    def test_default_goals(self, dm):
        goals = dm.get_goals()
        assert goals['calories'] == 2000
        assert goals['protein'] == 150

    def test_save_and_load(self, dm):
        dm.data['goals']['calories'] = 2500
        dm.save()
        
        # Create a new manager pointing to the same file
        dm2 = DataManager()
        dm2.path = dm.path
        dm2.data = dm2._load()
        
        assert dm2.get_goals()['calories'] == 2500


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: FOOD DATABASE (CRUD)
# ═══════════════════════════════════════════════════════════════════════════════

class TestFoodDatabase:
    def test_add_food(self, dm):
        dm.add_food("Chicken", "Proteins", 165, 31, 0, 3.6, 0, 100, "g")
        foods = dm.get_foods()
        assert "Chicken" in foods
        assert foods["Chicken"]["cal"] == 165

    def test_get_food(self, dm):
        dm.add_food("Apple", "Fruits", 95, 0.5, 25, 0.3, 4.4, 1, "piece")
        food = dm.get_food("Apple")
        assert food is not None
        assert food["category"] == "Fruits"
        assert food["fiber"] == 4.4

    def test_get_nonexistent_food(self, dm):
        assert dm.get_food("Mystery Meat") is None

    def test_update_food(self, dm):
        dm.add_food("Rice", "Grains", 130, 2.7, 28, 0.3, 0.4, 100, "g")
        # Update name and calories
        dm.update_food("Rice", "Brown Rice", "Grains", 112, 2.3, 24, 0.8, 1.8, 100, "g")
        
        assert dm.get_food("Rice") is None
        updated = dm.get_food("Brown Rice")
        assert updated is not None
        assert updated["cal"] == 112
        assert updated["fiber"] == 1.8

    def test_delete_food(self, dm):
        dm.add_food("Fish", "Proteins", 200, 20, 0, 10, 0, 100, "g")
        dm.delete_food("Fish")
        assert dm.get_food("Fish") is None
        
        # Deleting non-existent should not crash
        dm.delete_food("Air")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: DIARY & LOGGING
# ═══════════════════════════════════════════════════════════════════════════════

class TestDiary:
    def test_get_day(self, dm):
        today = dm.today_key()
        day = dm.get_day(today)
        assert "meals" in day
        assert "water" in day
        for cat in MEAL_CATS:
            assert cat in day["meals"]

    def test_log_food(self, dm):
        dm.add_food("Eggs", "Proteins", 155, 13, 1.1, 11, 0, 100, "g")
        success = dm.log_food("Breakfast", "Eggs", 2.0)  # 2 servings of 100g
        assert success is True
        
        day = dm.get_day()
        entry = day["meals"]["Breakfast"][0]
        assert entry["name"] == "Eggs"
        assert entry["cal"] == 310.0  # 155 * 2
        assert entry["protein"] == 26.0  # 13 * 2

    def test_log_nonexistent_food(self, dm):
        success = dm.log_food("Lunch", "Ghost Berry", 1)
        assert success is False

    def test_remove_entry(self, dm):
        dm.add_food("Bread", "Grains", 80, 4, 15, 1, 1, 1, "slice")
        dm.log_food("Breakfast", "Bread", 2)
        dm.log_food("Breakfast", "Bread", 1)
        
        dm.remove_entry("Breakfast", 0)
        day = dm.get_day()
        # Should be 1 entry left
        assert len(day["meals"]["Breakfast"]) == 1
        assert day["meals"]["Breakfast"][0]["servings"] == 1

    def test_get_totals(self, dm):
        dm.add_food("Steak", "Proteins", 271, 26, 0, 18, 0, 100, "g")
        dm.add_food("Potato", "Vegetables", 97, 2, 22, 0.1, 2.2, 1, "piece")
        
        dm.log_food("Dinner", "Steak", 1.5)
        dm.log_food("Dinner", "Potato", 2.0)
        
        totals = dm.get_totals()
        # 271*1.5 = 406.5
        # 97*2 = 194
        # Total = 600.5 -> rounded to 600.5
        assert totals["cal"] == 600.5
        assert totals["protein"] == 43.0  # 39 + 4


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: WATER TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

class TestWater:
    def test_add_water(self, dm):
        assert dm.get_water() == 0
        dm.add_water()
        assert dm.get_water() == 1
        dm.add_water()
        assert dm.get_water() == 2

    def test_rem_water(self, dm):
        dm.add_water()
        dm.add_water()
        dm.rem_water()
        assert dm.get_water() == 1

    def test_water_bounds(self, dm):
        # Cannot go below 0
        dm.rem_water()
        assert dm.get_water() == 0
        
        # Cannot go above 20
        for _ in range(25):
            dm.add_water()
        assert dm.get_water() == 20


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS: GOALS & HISTORY
# ═══════════════════════════════════════════════════════════════════════════════

class TestGoalsAndHistory:
    def test_set_goals(self, dm):
        dm.set_goals(calories=1800, protein=120, carbs=200, fat=60, fiber=25, water=10)
        goals = dm.get_goals()
        assert goals['calories'] == 1800
        assert goals['water'] == 10

    def test_clear_day(self, dm):
        dm.add_water()
        dm.add_food("Test", "Other", 100, 1, 1, 1, 1, 1, "g")
        dm.log_food("Lunch", "Test", 1)
        
        assert dm.get_water() == 1
        assert len(dm.get_day()["meals"]["Lunch"]) == 1
        
        dm.clear_day()
        assert dm.get_water() == 0
        assert len(dm.get_day()["meals"]["Lunch"]) == 0

    def test_get_dates(self, dm):
        dm.get_day("2023-01-01")
        dm.get_day("2023-01-02")
        dm.get_day("2023-01-03")
        
        dates = dm.get_dates()
        # Should be sorted reverse
        assert dates[0] == "2023-01-03"
        assert len(dates) == 3
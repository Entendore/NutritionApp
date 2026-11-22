"""
NutriTrack — Colors, constants, and category definitions.
"""

from kivy.metrics import dp, sp
from kivy.core.window import Window

# ── Colour Palette ──────────────────────────────────────────────────────────

C = {
    'pri':      [0.13, 0.59, 0.95, 1],
    'pri_dk':   [0.09, 0.44, 0.75, 1],
    'sec':      [0.30, 0.69, 0.31, 1],
    'acc':      [1.00, 0.60, 0.00, 1],
    'bg':       [0.95, 0.95, 0.96, 1],
    'card':     [1, 1, 1, 1],
    'txt':      [0.13, 0.13, 0.13, 1],
    'txt2':     [0.45, 0.45, 0.45, 1],
    'div':      [0.88, 0.88, 0.88, 1],
    'cal':      [0.91, 0.30, 0.24, 1],
    'pro':      [0.20, 0.60, 0.86, 1],
    'carb':     [0.95, 0.61, 0.07, 1],
    'fat_c':    [0.67, 0.28, 0.73, 1],
    'fib':      [0.30, 0.69, 0.31, 1],
    'water':    [0.00, 0.74, 0.83, 1],
    'danger':   [0.86, 0.20, 0.18, 1],
    'white':    [1, 1, 1, 1],
}

# ── Meal Categories ─────────────────────────────────────────────────────────

MEAL_CATS  = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
MEAL_ICON  = {'Breakfast': '🌅', 'Lunch': '☀️', 'Dinner': '🌙', 'Snacks': '🍿'}
MEAL_BG    = {
    'Breakfast': [1, .92, .78, 1],
    'Lunch':     [.80, .93, .80, 1],
    'Dinner':    [.78, .83, .93, 1],
    'Snacks':    [.93, .88, .93, 1],
}

# ── Food Categories ─────────────────────────────────────────────────────────

FOOD_CATS = [
    'Fruits', 'Vegetables', 'Proteins', 'Grains', 'Dairy',
    'Legumes', 'Nuts & Seeds', 'Beverages', 'Snacks',
    'Prepared Meals', 'Oils & Sauces', 'Other',
]

# ── Window Default ──────────────────────────────────────────────────────────

Window.clearcolor = C['bg']
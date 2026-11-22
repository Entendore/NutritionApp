#!/usr/bin/env python3
"""
NutriTrack — Local Nutrition Tracker
  • No APIs, No AI, All data in local JSON
  • Users build their own food database
  • Built-in nutrition education library
  • BMI & TDEE calculators
"""

import json, os, math
from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock

# ═══════════════════════════════════════════════════════════════════════════════
# COLOURS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

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

MEAL_CATS = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
MEAL_ICON = {'Breakfast': '🌅', 'Lunch': '☀️', 'Dinner': '🌙', 'Snacks': '🍿'}
MEAL_BG   = {'Breakfast': [1,.92,.78,1], 'Lunch': [.80,.93,.80,1],
              'Dinner': [.78,.83,.93,1], 'Snacks': [.93,.88,.93,1]}
FOOD_CATS = ['Fruits','Vegetables','Proteins','Grains','Dairy',
             'Legumes','Nuts & Seeds','Beverages','Snacks',
             'Prepared Meals','Oils & Sauces','Other']

Window.clearcolor = C['bg']

# ═══════════════════════════════════════════════════════════════════════════════
# EDUCATION CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

EDU_TOPICS = [
  {'title':'Understanding Calories','icon':'🔥','sections':[
    ('What Are Calories?',
     'Calories are units of energy that measure how much energy food and drink '
     'provide to your body. Your body needs this energy for every function — '
     'from breathing and pumping blood to walking and thinking.\n\n'
     '1 kilocalorie (kcal) = energy to heat 1 kg of water by 1°C.\n'
     'When we say "calories" on food labels, we actually mean kilocalories.'),
    ('Total Daily Energy Expenditure (TDEE)',
     'Your TDEE is the total calories you burn each day. It has three components:\n\n'
     '• Basal Metabolic Rate (BMR): 60-75% — energy to keep you alive at rest\n'
     '• Physical Activity: 15-30% — exercise + daily movement\n'
     '• Thermic Effect of Food (TEF): 5-10% — energy to digest and absorb food\n\n'
     'BMR is influenced by age, sex, body size, muscle mass, and genetics. '
     'Muscle tissue burns more calories at rest than fat tissue, so increasing '
     'muscle mass raises your BMR.'),
    ('Weight Management Basics',
     '• Maintain weight: Calories In ≈ TDEE\n'
     '• Lose weight: Eat 300-500 kcal below TDEE\n'
     '• Gain weight: Eat 300-500 kcal above TDEE\n\n'
     '1 kg of body fat ≈ 7,700 kcal\n'
     'A deficit of 500 kcal/day → ~0.5 kg loss per week\n\n'
     'Never eat below 1,200 kcal/day (women) or 1,500 kcal/day (men) '
     'without medical supervision. Severe restriction slows metabolism, '
     'causes nutrient deficiencies, and leads to muscle loss.'),
    ('Empty vs Nutrient-Dense Calories',
     'Empty calories provide energy but almost no vitamins, minerals, or fiber:\n'
     '  Soda, candy, pastries, alcohol, fried snacks\n\n'
     'Nutrient-dense calories pack vitamins and minerals per calorie:\n'
     '  Vegetables, lean proteins, whole grains, fruits, legumes\n\n'
     '200 kcal of soda ≠ 200 kcal of salmon in nutritional value.\n'
     'Focus on food quality, not just calorie quantity.'),
  ]},
  {'title':'Protein Guide','icon':'🥩','sections':[
    ('Why Protein Matters',
     'Protein is made of 20 amino acids — 9 are "essential" (your body cannot '
     'make them, you must eat them). Protein is responsible for:\n\n'
     '• Building and repairing muscle tissue\n'
     '• Producing enzymes and hormones\n'
     '• Supporting immune function (antibodies are proteins)\n'
     '• Maintaining skin, hair, nails, and bones\n'
     '• Providing satiety — protein keeps you full longer than carbs or fat'),
    ('How Much Protein Do You Need?',
     'RDA (minimum): 0.8 g per kg body weight\n'
     'Active / athletic: 1.2 - 2.0 g per kg\n'
     'Older adults (65+): 1.0 - 1.2 g per kg\n'
     'Weight loss (to preserve muscle): 1.6 - 2.4 g per kg\n\n'
     'Example: A 70 kg active person → 84-140 g protein per day\n\n'
     'Spread protein across meals: 20-40 g per meal for optimal muscle '
     'protein synthesis. Your body cannot store excess protein — it either '
     'uses it or excretes it.'),
    ('Complete vs Incomplete Proteins',
     'Complete proteins contain all 9 essential amino acids:\n'
     '  Meat, fish, poultry, eggs, dairy, soy, quinoa, buckwheat\n\n'
     'Incomplete proteins lack one or more essential amino acids:\n'
     '  Beans, lentils, nuts, seeds, most grains\n\n'
     'Complementary proteins: combine incomplete sources to get all amino acids:\n'
     '  Rice + beans, hummus + pita, peanut butter + whole wheat bread\n\n'
     'You do NOT need to eat complementary proteins at the same meal — '
     'just eat a variety across the day.'),
  ]},
  {'title':'Carbohydrates Guide','icon':'🍞','sections':[
    ('Types of Carbohydrates',
     'Carbohydrates are your body\'s preferred energy source, especially for '
     'the brain and during high-intensity exercise.\n\n'
     'Simple carbs (sugars): quick energy\n'
     '  Glucose, fructose, sucrose, lactose\n'
     '  Found in: fruit, milk, honey, table sugar, candy\n\n'
     'Complex carbs (starches): sustained energy\n'
     '  Long chains of sugar molecules\n'
     '  Found in: whole grains, potatoes, beans, oats\n\n'
     'Fiber: a type of carb the body cannot digest (covered in its own topic)'),
    ('Glycemic Index (GI)',
     'GI measures how quickly a carbohydrate food raises blood sugar on a '
     'scale of 0-100 (pure glucose = 100).\n\n'
     'Low GI (≤55): Oats, lentils, most fruits, sweet potato, beans\n'
     'Medium GI (56-69): Whole wheat bread, brown rice, honey\n'
     'High GI (≥70): White bread, white rice, potatoes, cornflakes\n\n'
     'Low GI foods provide steady energy and better blood sugar control.\n'
     'Glycemic Load (GL) accounts for portion size — a more practical measure.'),
    ('Daily Carb Recommendations',
     'Recommended: 45-65% of total daily calories\n\n'
     'For a 2,000 kcal diet: 225-325 g carbs per day\n\n'
     'Tips:\n'
     '• Prioritize whole grains over refined grains\n'
     '• Choose whole fruit over fruit juice\n'
     '• Limit added sugars to <10% of calories (<25 g/day for women, <36 g for men)\n'
     '• Carbs are NOT inherently fattening — excess calories from any source cause weight gain'),
  ]},
  {'title':'Fats Guide','icon':'🥑','sections':[
    ('Why Dietary Fat Is Essential',
     'Despite decades of "low-fat" messaging, fat is vital for health:\n\n'
     '• Energy: 9 kcal per gram (most energy-dense macronutrient)\n'
     '• Hormone production: testosterone, estrogen, cortisol\n'
     '• Absorption of fat-soluble vitamins: A, D, E, K\n'
     '• Cell membrane structure and function\n'
     '• Brain health: ~60% of the brain is fat\n'
     '• Insulation and organ protection'),
    ('Types of Dietary Fat',
     'Unsaturated fats (heart-healthy):\n'
     '  Monounsaturated: olive oil, avocado, almonds, cashews\n'
     '  Polyunsaturated: fatty fish, walnuts, flaxseed, sunflower oil\n'
     '    Omega-3: salmon, sardines, chia seeds, walnuts (anti-inflammatory)\n'
     '    Omega-6: vegetable oils, poultry, eggs\n\n'
     'Saturated fats (limit to <10% of calories):\n'
     '  Butter, cheese, red meat, coconut oil, palm oil\n\n'
     'Trans fats (AVOID completely):\n'
     '  Partially hydrogenated oils — linked to heart disease, inflammation\n'
     '  Found in: some margarines, commercial baked goods, fried foods'),
    ('Daily Fat Recommendations',
     'Recommended: 20-35% of total daily calories\n\n'
     'For a 2,000 kcal diet: 44-78 g fat per day\n\n'
     '• Prioritize unsaturated fats over saturated fats\n'
     '• Aim for 2-3 servings of fatty fish per week (omega-3)\n'
     '• Avoid trans fats completely\n'
     '• Cooking oils: olive oil and avocado oil are best for most uses\n'
     '• Don\'t fear healthy fats — they help you absorb nutrients and stay satisfied'),
  ]},
  {'title':'Fiber Guide','icon':'🥦','sections':[
    ('Soluble vs Insoluble Fiber',
     'Fiber is a carbohydrate the body cannot digest. It comes in two types:\n\n'
     'Soluble fiber (dissolves in water, forms a gel):\n'
     '  Oats, beans, apples, citrus, carrots, psyllium\n'
     '  • Lowers LDL cholesterol\n'
     '  • Stabilizes blood sugar\n'
     '  • Feeds beneficial gut bacteria\n\n'
     'Insoluble fiber (does not dissolve, adds bulk):\n'
     '  Whole wheat, bran, nuts, seeds, vegetables\n'
     '  • Promotes regular bowel movements\n'
     '  • Prevents constipation\n'
     '  • Supports colon health'),
    ('Health Benefits & Recommendations',
     'Benefits of adequate fiber intake:\n'
     '• Reduces risk of heart disease by 20-30%\n'
     '• Lowers type 2 diabetes risk\n'
     '• Promotes healthy gut microbiome\n'
     '• Increases satiety (helps with weight management)\n'
     '• Reduces colorectal cancer risk\n\n'
     'Daily recommendations:\n'
     '  Women: 25 g  |  Men: 38 g\n'
     '  Average intake: only 15 g/day — most people are far below!\n\n'
     'Increase fiber GRADUALLY to avoid bloating and gas.\n'
     'Drink plenty of water when increasing fiber intake.'),
  ]},
  {'title':'Vitamins Overview','icon':'💊','sections':[
    ('Fat-Soluble Vitamins',
     'Stored in body fat — can accumulate, so avoid mega-doses:\n\n'
     'Vitamin A — Vision, immune function, skin health\n'
     '  Sources: carrots, sweet potato, spinach, liver\n\n'
     'Vitamin D — Calcium absorption, bone health, immunity\n'
     '  Sources: sunlight, fatty fish, fortified milk, eggs\n'
     '  Many people are deficient, especially in northern climates\n\n'
     'Vitamin E — Antioxidant, protects cell membranes\n'
     '  Sources: almonds, sunflower seeds, spinach, avocado\n\n'
     'Vitamin K — Blood clotting, bone metabolism\n'
     '  Sources: kale, spinach, broccoli, Brussels sprouts'),
    ('Water-Soluble Vitamins',
     'Not stored in body — need daily intake:\n\n'
     'B1 (Thiamine) — Energy metabolism | Whole grains, pork, beans\n'
     'B2 (Riboflavin) — Energy, skin health | Dairy, eggs, lean meat\n'
     'B3 (Niacin) — Energy, nervous system | Poultry, fish, peanuts\n'
     'B6 — Protein metabolism, brain development | Chicken, bananas, potatoes\n'
     'B12 — Red blood cells, nerve function | Meat, fish, dairy (vegans need supplements)\n'
     'Folate (B9) — DNA synthesis, fetal development | Leafy greens, legumes, fortified grains\n'
     'Vitamin C — Immune function, collagen, antioxidant | Citrus, bell peppers, strawberries, broccoli'),
  ]},
  {'title':'Minerals Overview','icon':'⚡','sections':[
    ('Key Macrominerals',
     'Calcium (1000 mg/day) — Bones, teeth, muscle contraction, nerve signaling\n'
     '  Sources: dairy, fortified plant milks, broccoli, sardines, tofu\n\n'
     'Magnesium (310-420 mg/day) — 300+ enzyme reactions, muscle & nerve function\n'
     '  Sources: spinach, almonds, black beans, avocado, dark chocolate\n\n'
     'Potassium (2600-3400 mg/day) — Fluid balance, blood pressure regulation\n'
     '  Sources: bananas, potatoes, spinach, beans, yogurt\n\n'
     'Sodium (≤2300 mg/day) — Fluid balance, nerve function\n'
     '  Most people consume too much — limit processed foods'),
    ('Key Trace Minerals',
     'Iron (8-18 mg/day) — Oxygen transport, energy production\n'
     '  Heme iron (better absorbed): red meat, poultry, fish\n'
     '  Non-heme iron: spinach, lentils, fortified cereals\n'
     '  Tip: pair with vitamin C to boost absorption\n\n'
     'Zinc (8-11 mg/day) — Immune function, wound healing, taste/smell\n'
     '  Sources: oysters, beef, pumpkin seeds, lentils\n\n'
     'Iodine (150 mcg/day) — Thyroid hormones, metabolism\n'
     '  Sources: iodized salt, seafood, dairy\n\n'
     'Selenium (55 mcg/day) — Antioxidant, thyroid function\n'
     '  Sources: Brazil nuts (1 nut = daily needs), seafood, eggs'),
  ]},
  {'title':'Hydration','icon':'💧','sections':[
    ('Water & Your Body',
     'Water makes up 50-70% of your body weight. Every cell, tissue, and organ '
     'needs water to function properly.\n\n'
     'Water roles in the body:\n'
     '• Regulates body temperature\n'
     '• Lubricates and cushions joints\n'
     '• Protects sensitive tissues\n'
     '• Carries nutrients and oxygen to cells\n'
     '• Removes waste products\n'
     '• Maintains blood volume and pressure'),
    ('How Much Water Do You Need?',
     'General guidelines (including water from food):\n'
     '  Women: ~2.7 liters/day (~91 oz, ~9 cups)\n'
     '  Men: ~3.7 liters/day (~125 oz, ~13 cups)\n\n'
     'About 20% of water intake comes from food (fruits, vegetables, soups).\n\n'
     'Increase intake when you:\n'
     '• Exercise (add 0.5-1 L per hour of exercise)\n'
     '• Are in hot or humid weather\n'
     '• Are at high altitude\n'
     '• Are sick (fever, vomiting, diarrhea)\n'
     '• Are pregnant or breastfeeding'),
    ('Signs of Dehydration',
     'Mild dehydration (1-2% body weight lost):\n'
     '  Thirst, dry mouth, darker urine, fatigue, headache\n\n'
     'Moderate dehydration (3-5%):\n'
     '  Dizziness, rapid heartbeat, reduced urine output, dry skin\n\n'
     'Severe dehydration (>5%):\n'
     '  Confusion, fainting, no urine output, rapid breathing\n'
     '  SEEK MEDICAL ATTENTION IMMEDIATELY\n\n'
     'Tip: Check urine color — pale yellow = well hydrated, dark = drink more.\n'
     'By the time you feel thirsty, you are already mildly dehydrated.'),
  ]},
  {'title':'Reading Nutrition Labels','icon':'🏷️','sections':[
    ('How to Read a Nutrition Facts Label',
     '1. Serving Size — Everything on the label is PER SERVING. Check how many '
     'servings are in the container.\n\n'
     '2. Calories — Total energy per serving. Remember: calories from fat are '
     'a subset of total calories.\n\n'
     '3. Nutrients to LIMIT:\n'
     '   Saturated fat, trans fat, sodium, added sugars\n\n'
     '4. Nutrients to GET ENOUGH OF:\n'
     '   Dietary fiber, vitamin D, calcium, iron, potassium\n\n'
     '5. % Daily Value — Based on a 2,000 kcal diet:\n'
     '   <5% = low  |  >20% = high\n'
     '   Use this to quickly compare products'),
    ('Ingredients List Tips',
     'Ingredients are listed by weight (most first).\n\n'
     'Red flags in ingredients:\n'
     '• Sugar in the first 3 ingredients\n'
     '• Hydrogenated or partially hydrogenated oils (trans fat)\n'
     '• Long lists of unpronounceable additives\n'
     '• Multiple names for sugar (dextrose, maltose, sucrose, syrup, etc.)\n\n'
     'Health claims to be skeptical of:\n'
     '• "Natural" has no legal definition\n'
     '• "Low-fat" often means added sugar\n'
     '• "Multigrain" ≠ whole grain\n'
     '• "No cholesterol" on plant foods (they never have cholesterol)'),
  ]},
  {'title':'Healthy Plate Method','icon':'🍽️','sections':[
    ('The Balanced Plate',
     'An easy visual guide — no counting required:\n\n'
     '½ plate: Vegetables and fruits\n'
     '  Aim for variety and color. Non-starchy vegetables are best.\n\n'
     '¼ plate: Lean protein\n'
     '  Fish, poultry, beans, tofu, lean meat, eggs\n\n'
     '¼ plate: Whole grains or starchy vegetables\n'
     '  Brown rice, quinoa, sweet potato, whole wheat bread\n\n'
     'Side: Water or unsweetened beverage\n'
     'Small amount: Healthy fat (olive oil, avocado, nuts)'),
    ('Portion Size Guides (No Scale Needed)',
     'Palm (no fingers) = 3 oz meat/protein\n'
     'Fist = 1 cup (rice, pasta, cereal, vegetables)\n'
     'Cupped hand = ½ cup (oats, yogurt, fruit, ice cream)\n'
     'Thumb = 1 tablespoon (peanut butter, dressing, oil)\n'
     'Thumb tip = 1 teaspoon (butter, mayo, sugar)\n\n'
     'These are rough guides. Adjust for your calorie needs.\n'
     'Men generally need ~2x women\'s portions.'),
    ('Meal Planning Tips',
     '• Plan 3 meals + 1-2 snacks per day\n'
     '• Include protein at every meal for satiety\n'
     '• Prep ingredients on weekends (wash/chop veggies, cook grains)\n'
     '• Keep healthy snacks accessible (fruit, nuts, yogurt)\n'
     '• Batch cook soups, stews, and casseroles for the week\n'
     '• Use the plate method as a template for every meal\n'
     '• Don\'t shop hungry — you\'ll buy more processed food'),
  ]},
  {'title':'BMI & TDEE Calculator','icon':'🧮','calculator':True},
  {'title':'Nutrition Myths Debunked','icon':'❌','sections':[
    ('Common Misconceptions',
     '❌ "Carbs make you fat"\n'
     '✅ Excess calories from ANY source cause weight gain. Whole carb sources '
     '(oats, beans, fruit) are nutritious and filling.\n\n'
     '❌ "Eating late at night causes weight gain"\n'
     '✅ Total daily calories matter most. Late eating often leads to excess '
     'calories from snacking, not the timing itself.\n\n'
     '❌ "Detox diets cleanse your body"\n'
     '✅ Your liver, kidneys, and lungs detox your body 24/7. No juice or '
     'supplement does it better.'),
    ('More Myths',
     '❌ "All fats are bad"\n'
     '✅ Unsaturated fats are essential for health. Trans fats are the ones to avoid.\n\n'
     '❌ "You need protein supplements to build muscle"\n'
     '✅ Most people can meet protein needs through food. Supplements are '
     'convenient but not necessary.\n\n'
     '❌ "Fresh is always better than frozen"\n'
     '✅ Frozen fruits/vegetables are picked at peak ripeness and flash-frozen, '
     'often retaining more nutrients than "fresh" produce that traveled far.\n\n'
     '❌ "Brown sugar is healthier than white sugar"\n'
     '✅ Brown sugar is white sugar + molasses. The mineral difference is negligible.\n\n'
     '❌ "Skipping meals helps lose weight"\n'
     '✅ Often leads to overeating later. Regular meals support stable blood sugar.'),
  ]},
  {'title':'Eating on a Budget','icon':'💰','sections':[
    ('Affordable Nutritious Staples',
     'Proteins:\n'
     '  Eggs (~$0.15 each), canned tuna, lentils, beans, chicken thighs, tofu\n\n'
     'Grains:\n'
     '  Oats, brown rice, whole wheat pasta, barley\n\n'
     'Vegetables:\n'
     '  Cabbage, carrots, onions, frozen spinach, potatoes, seasonal produce\n\n'
     'Fruits:\n'
     '  Bananas, apples (in season), frozen berries, oranges\n\n'
     'Other:\n'
     '  Peanut butter, canned tomatoes, milk, yogurt'),
    ('Money-Saving Strategies',
     '• Plan meals for the week before shopping\n'
     '• Make a shopping list and stick to it\n'
     '• Buy in bulk for staples (rice, oats, beans)\n'
     '• Use frozen vegetables — just as nutritious, less waste\n'
     '• Cook large batches and freeze portions\n'
     '• Buy seasonal produce (cheaper and fresher)\n'
     '• Compare unit prices, not package prices\n'
     '• Reduce meat: use beans, lentils, and eggs as protein\n'
     '• Pack lunches instead of eating out\n'
     '• Never shop when hungry\n'
     '• Grow herbs and easy vegetables at home'),
  ]},
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class DataManager:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "nutritrack_data.json")
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path,'r') as f: return json.load(f)
            except Exception: pass
        return {"goals":{"calories":2000,"protein":150,"carbs":250,
                         "fat":65,"fiber":30,"water":8},
                "log":{},"foods":{}}

    def save(self):
        with open(self.path,'w') as f: json.dump(self.data,f,indent=2)

    # ── Day ────────────────────────────────────────────────────────────────
    def today_key(self): return date.today().isoformat()

    def get_day(self, dk=None):
        if dk is None: dk = self.today_key()
        if dk not in self.data["log"]:
            self.data["log"][dk] = {"meals":{c:[] for c in MEAL_CATS},"water":0}
        return self.data["log"][dk]

    def get_totals(self, dk=None):
        day = self.get_day(dk)
        t = {"cal":0,"protein":0,"carbs":0,"fat":0,"fiber":0}
        for cat in MEAL_CATS:
            for e in day["meals"][cat]:
                for k in t: t[k] += e.get(k,0)
        for k in t: t[k] = round(t[k],1)
        return t

    # ── Food DB ────────────────────────────────────────────────────────────
    def get_foods(self): return self.data.get("foods",{})
    def get_food(self, name): return self.data.get("foods",{}).get(name)

    def add_food(self, name, cat, cal, pro, carb, fat, fib, srv, unit):
        self.data["foods"][name] = {"category":cat,"cal":float(cal),
            "protein":float(pro),"carbs":float(carb),"fat":float(fat),
            "fiber":float(fib),"serving":float(srv),"unit":unit}
        self.save()

    def update_food(self, old_name, name, cat, cal, pro, carb, fat, fib, srv, unit):
        if old_name in self.data["foods"]:
            del self.data["foods"][old_name]
        self.add_food(name, cat, cal, pro, carb, fat, fib, srv, unit)

    def delete_food(self, name):
        if name in self.data.get("foods",{}):
            del self.data["foods"][name]; self.save()

    # ── Diary ──────────────────────────────────────────────────────────────
    def log_food(self, meal, name, servings, dk=None):
        fi = self.get_food(name)
        if not fi: return False
        entry = {"name":name,"servings":round(servings,2),
                 "cal":round(fi["cal"]*servings,1),
                 "protein":round(fi["protein"]*servings,1),
                 "carbs":round(fi["carbs"]*servings,1),
                 "fat":round(fi["fat"]*servings,1),
                 "fiber":round(fi["fiber"]*servings,1),
                 "unit":fi["unit"]}
        self.get_day(dk)["meals"][meal].append(entry); self.save(); return True

    def remove_entry(self, meal, idx, dk=None):
        day = self.get_day(dk)
        if 0 <= idx < len(day["meals"][meal]):
            day["meals"][meal].pop(idx); self.save()

    # ── Water ──────────────────────────────────────────────────────────────
    def add_water(self, dk=None):
        day = self.get_day(dk); day["water"] = min(day.get("water",0)+1,20); self.save()
    def rem_water(self, dk=None):
        day = self.get_day(dk); day["water"] = max(day.get("water",0)-1,0); self.save()
    def get_water(self, dk=None): return self.get_day(dk).get("water",0)

    # ── Goals ──────────────────────────────────────────────────────────────
    def set_goals(self, **kw):
        self.data["goals"] = {k:int(v) for k,v in kw.items()}; self.save()
    def get_goals(self): return self.data["goals"]

    # ── History ────────────────────────────────────────────────────────────
    def get_dates(self): return sorted(self.data["log"].keys(), reverse=True)[:60]

    def clear_day(self, dk=None):
        if dk is None: dk = self.today_key()
        self.data["log"][dk] = {"meals":{c:[] for c in MEAL_CATS},"water":0}
        self.save()


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM WIDGETS
# ═══════════════════════════════════════════════════════════════════════════════

class Card(BoxLayout):
    def __init__(self, bg=C['card'], radius=dp(10), **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*bg)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=lambda i,v: setattr(self._r,'pos',v),
                  size=lambda i,v: setattr(self._r,'size',v))


class PBar(FloatLayout):
    progress = NumericProperty(0)
    max_val  = NumericProperty(100)
    bar_col  = ListProperty([0.3,0.7,0.3,1])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint_y = None; self.height = dp(10)
        self.bind(size=self._draw, pos=self._draw, progress=self._draw, max_val=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*C['div'])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
            if self.max_val > 0:
                fw = max(self.width * min(self.progress/self.max_val, 1.0), 0)
                if fw > 0:
                    Color(*self.bar_col)
                    RoundedRectangle(pos=self.pos, size=(fw, self.height), radius=[dp(5)])


class MacroRow(BoxLayout):
    def __init__(self, label, consumed, goal, color, **kw):
        super().__init__(**kw)
        self.orientation = 'horizontal'
        self.size_hint_y = None; self.height = dp(30)
        self.padding = [dp(4),dp(1)]; self.spacing = dp(6)
        l = Label(text=label, font_size=sp(12), bold=True, color=C['txt'],
                  size_hint_x=0.18, halign='right')
        l.bind(size=l.setter('text_size')); self.add_widget(l)
        self.add_widget(PBar(progress=consumed, max_val=max(goal,1),
                             bar_col=color, size_hint_x=0.48))
        v = Label(text=f'{int(consumed)}/{int(goal)}g', font_size=sp(11),
                  color=C['txt2'], size_hint_x=0.34, halign='left')
        v.bind(size=v.setter('text_size')); self.add_widget(v)


def btn(text, bg=C['pri'], fg=C['white'], fs=sp(14), **kw):
    return Button(text=text, font_size=fs, color=fg,
                  background_normal='', background_color=bg, **kw)

def toast(msg):
    ct = BoxLayout(orientation='vertical', padding=dp(16))
    ct.add_widget(Label(text=msg, font_size=sp(14), color=C['txt']))
    p = Popup(title='', content=ct, size_hint=(0.7,0.22),
              background='', separator_color=(0,0,0,0))
    with p.canvas.before:
        Color(*C['card'])
        RoundedRectangle(pos=p.pos, size=p.size, radius=[dp(12)])
    p.open(); Clock.schedule_once(lambda dt: p.dismiss(), 1.8)

# ═══════════════════════════════════════════════════════════════════════════════
# HOME SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

class HomeScreen(Screen):
    def __init__(self, **kw): super().__init__(**kw); self._box = BoxLayout(); self.add_widget(self._box)

    def on_enter(self, *_): self._build()

    def _build(self):
        app = App.get_running_app(); dm = app.dm
        dk = app.viewing_date; goals = dm.get_goals()
        totals = dm.get_totals(dk); water = dm.get_water(dk)

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))
        self._box.add_widget(root)

        # date bar
        dbar = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(4))
        pb = btn('◀', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        pb.bind(on_release=lambda x: self._chg_day(-1)); dbar.add_widget(pb)
        d = date.fromisoformat(dk); td = date.today()
        dl = 'Today' if dk == td.isoformat() else 'Yesterday' if dk == (td-timedelta(1)).isoformat() else d.strftime('%a %b %d')
        dbar.add_widget(Label(text=dl, font_size=sp(16), bold=True, color=C['txt']))
        nb = btn('▶', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        nb.bind(on_release=lambda x: self._chg_day(1)); dbar.add_widget(nb)
        root.add_widget(dbar)

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=[dp(4),dp(4),dp(4),dp(8)])
        ct.bind(minimum_height=ct.setter('height'))

        # calorie card
        cc = Card(orientation='vertical', padding=dp(14), spacing=dp(4), size_hint_y=None, height=dp(125))
        cc.add_widget(Label(text=str(int(totals['cal'])), font_size=sp(40), bold=True, color=C['cal'], size_hint_y=0.48))
        rem = int(goals['calories']-totals['cal'])
        cc.add_widget(Label(text=f'{rem} cal remaining' if rem>=0 else f'{abs(rem)} cal over!', font_size=sp(13), color=C['txt2'], size_hint_y=0.18))
        pct = totals['cal']/max(goals['calories'],1)
        cc.add_widget(PBar(progress=totals['cal'], max_val=max(goals['calories'],1), bar_col=C['cal'] if pct<=1 else C['danger'], size_hint_y=0.18))
        cc.add_widget(Label(text=f'{int(pct*100)}% of {goals["calories"]} goal', font_size=sp(11), color=C['txt2'], size_hint_y=0.16))
        ct.add_widget(cc)

        # macros card
        mc = Card(orientation='vertical', padding=dp(12), spacing=dp(1), size_hint_y=None, height=dp(155))
        mc.add_widget(Label(text='Macronutrients', font_size=sp(14), bold=True, color=C['txt'], size_hint_y=0.16, halign='left'))
        for lbl,k,col in [('Protein','protein',C['pro']),('Carbs','carbs',C['carb']),('Fat','fat',C['fat_c']),('Fiber','fiber',C['fib'])]:
            mc.add_widget(MacroRow(lbl, totals[k], goals[k], col, size_hint_y=0.21))
        ct.add_widget(mc)

        # water card
        wc = Card(orientation='vertical', padding=dp(12), spacing=dp(4), size_hint_y=None, height=dp(100))
        wh = BoxLayout(size_hint_y=0.4)
        wh.add_widget(Label(text='💧 Water', font_size=sp(14), bold=True, color=C['txt'], halign='left', size_hint_x=0.5))
        wh.add_widget(Label(text=f'{water} / {goals["water"]} glasses', font_size=sp(14), color=C['water'], halign='right', size_hint_x=0.5))
        wc.add_widget(wh)
        wc.add_widget(PBar(progress=water, max_val=max(goals['water'],1), bar_col=C['water'], size_hint_y=0.25))
        wb = BoxLayout(size_hint_y=0.35, spacing=dp(8))
        mb = btn('−', bg=C['danger'], fs=sp(16), size_hint_x=0.3)
        mb.bind(on_release=lambda x: (dm.rem_water(dk), self._build()))
        ab = btn('+ Add Glass', bg=C['water'], fs=sp(13), size_hint_x=0.7)
        ab.bind(on_release=lambda x: (dm.add_water(dk), self._build()))
        wb.add_widget(mb); wb.add_widget(ab)
        wc.add_widget(wb)
        ct.add_widget(wc)

        # meals summary
        day = dm.get_day(dk)
        for meal in MEAL_CATS:
            entries = day['meals'][meal]
            mc2 = Card(orientation='vertical', padding=dp(10), spacing=dp(4), size_hint_y=None)
            h = BoxLayout(size_hint_y=None, height=dp(28))
            with h.canvas.before:
                Color(*MEAL_BG[meal])
                RoundedRectangle(pos=h.pos, size=h.size, radius=[dp(6)])
            h.bind(pos=lambda i,v,_r=h.canvas.before.children[-1]: setattr(_r,'pos',v),
                   size=lambda i,v,_r=h.canvas.before.children[-1]: setattr(_r,'size',v))
            h.add_widget(Label(text=f'{MEAL_ICON[meal]} {meal}', font_size=sp(13), bold=True, color=C['txt'], halign='left', size_hint_x=0.6))
            mcal = sum(e['cal'] for e in entries)
            h.add_widget(Label(text=f'{int(mcal)} cal', font_size=sp(12), color=C['txt2'], halign='right', size_hint_x=0.4))
            mc2.add_widget(h)
            if entries:
                for e in entries:
                    r = BoxLayout(size_hint_y=None, height=dp(24), padding=[dp(8),0])
                    r.add_widget(Label(text=f'{e["name"]}  ×{e["servings"]}', font_size=sp(11), color=C['txt2'], halign='left', size_hint_x=0.7))
                    r.add_widget(Label(text=f'{int(e["cal"])} cal', font_size=sp(11), color=C['txt2'], halign='right', size_hint_x=0.3))
                    mc2.add_widget(r)
                mc2.height = dp(32) + dp(24)*len(entries)
            else:
                mc2.add_widget(Label(text='No entries', font_size=sp(11), color=C['div'], size_hint_y=None, height=dp(22)))
                mc2.height = dp(54)
            ct.add_widget(mc2)

        scr.add_widget(ct); root.add_widget(scr)

    def _chg_day(self, delta):
        app = App.get_running_app()
        d = date.fromisoformat(app.viewing_date) + timedelta(delta)
        app.viewing_date = d.isoformat(); self._build()


# ═══════════════════════════════════════════════════════════════════════════════
# FOODS SCREEN (User-Built Database)
# ═══════════════════════════════════════════════════════════════════════════════

class FoodsScreen(Screen):
    def __init__(self, **kw): super().__init__(**kw); self._box = BoxLayout(); self.add_widget(self._box)
    def on_enter(self, *_): self._build()

    def _build(self):
        dm = App.get_running_app().dm
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))

        # top bar
        tb = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        tb.add_widget(Label(text='🍎 My Foods', font_size=sp(18), bold=True, color=C['txt'], halign='left', size_hint_x=0.6))
        ab = btn('+ Add Food', bg=C['sec'], fs=sp(13), size_hint_x=0.4)
        ab.bind(on_release=lambda x: self._show_add_form())
        tb.add_widget(ab); root.add_widget(tb)

        # search
        self._search = TextInput(hint_text='🔍 Search foods...', size_hint_y=None, height=dp(40),
                                  font_size=sp(14), multiline=False,
                                  background_normal='', background_color=C['card'])
        self._search.bind(text=lambda i,v: self._filter_list())
        root.add_widget(self._search)

        # category filter
        self._cat_spin = Spinner(text='All Categories', values=['All Categories']+FOOD_CATS,
                                  size_hint_y=None, height=dp(36), font_size=sp(12),
                                  background_normal='', background_color=C['card'])
        self._cat_spin.bind(text=lambda i,v: self._filter_list())
        root.add_widget(self._cat_spin)

        # food list
        self._scroll = ScrollView()
        self._list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(6), padding=dp(2))
        self._list.bind(minimum_height=self._list.setter('height'))
        self._scroll.add_widget(self._list)
        root.add_widget(self._scroll)
        self._box.add_widget(root)
        self._filter_list()

    def _filter_list(self):
        dm = App.get_running_app().dm
        self._list.clear_widgets()
        foods = dm.get_foods()
        q = self._search.text.lower() if hasattr(self, '_search') else ''
        cat = self._cat_spin.text if hasattr(self, '_cat_spin') else 'All Categories'

        for name, fi in foods.items():
            if q and q not in name.lower(): continue
            if cat != 'All Categories' and fi.get('category','') != cat: continue
            self._add_food_row(name, fi)

        if not self._list.children:
            self._list.add_widget(Label(
                text='No foods yet!\nTap "+ Add Food" to create your first food entry.',
                font_size=sp(14), color=C['txt2'], size_hint_y=None, height=dp(120)))

    def _add_food_row(self, name, fi):
        card = Card(orientation='vertical', padding=dp(10), spacing=dp(2), size_hint_y=None, height=dp(95))
        r1 = BoxLayout(size_hint_y=0.32)
        r1.add_widget(Label(text=name, font_size=sp(14), bold=True, color=C['txt'], halign='left', size_hint_x=0.55))
        r1.add_widget(Label(text=fi.get('category',''), font_size=sp(10), color=C['pri'], halign='right', size_hint_x=0.45))
        card.add_widget(r1)
        r2 = BoxLayout(size_hint_y=0.24)
        r2.add_widget(Label(text=f'{fi["serving"]} {fi["unit"]}', font_size=sp(10), color=C['txt2'], halign='left'))
        card.add_widget(r2)
        r3 = BoxLayout(size_hint_y=0.22)
        for lbl,k,col in [('Cal',C['cal'],'cal'),('Pro',C['pro'],'protein'),('Carb',C['carb'],'carbs'),('Fat',C['fat_c'],'fat'),('Fib',C['fib'],'fiber')]:
            r3.add_widget(Label(text=f'{lbl}:{fi[k]}g' if k!='cal' else f'{fi[k]}cal',
                                font_size=sp(10), color=col))
        card.add_widget(r3)
        r4 = BoxLayout(size_hint_y=0.22, spacing=dp(6))
        eb = btn('✏️ Edit', bg=C['pri'], fs=sp(11), size_hint_x=0.5)
        eb.bind(on_release=lambda x,n=name: self._show_add_form(n))
        db = btn('🗑️ Delete', bg=C['danger'], fs=sp(11), size_hint_x=0.5)
        db.bind(on_release=lambda x,n=name: self._confirm_delete(n))
        r4.add_widget(eb); r4.add_widget(db)
        card.add_widget(r4)
        self._list.add_widget(card)

    def _show_add_form(self, edit_name=None):
        dm = App.get_running_app().dm
        fi = dm.get_food(edit_name) if edit_name else None
        title = 'Edit Food' if edit_name else 'Add New Food'

        lay = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(16), size_hint_y=None)
        lay.bind(minimum_height=lay.setter('height'))

        fields = {}
        for lbl, key, default, hint in [
            ('Food Name','name', edit_name or '', 'e.g. Chicken Breast'),
            ('Category','category', fi.get('category','Other') if fi else 'Other', ''),
            ('Serving Size','serving', str(fi.get('serving',1)) if fi else '1', 'number'),
            ('Serving Unit','unit', fi.get('unit','serving') if fi else 'serving', 'e.g. cup, oz, piece'),
            ('Calories','cal', str(fi.get('cal',0)) if fi else '0', 'kcal per serving'),
            ('Protein (g)','protein', str(fi.get('protein',0)) if fi else '0', 'grams'),
            ('Carbs (g)','carbs', str(fi.get('carbs',0)) if fi else '0', 'grams'),
            ('Fat (g)','fat', str(fi.get('fat',0)) if fi else '0', 'grams'),
            ('Fiber (g)','fiber', str(fi.get('fiber',0)) if fi else '0', 'grams'),
        ]:
            lay.add_widget(Label(text=lbl, font_size=sp(12), color=C['txt'], halign='left', size_hint_y=None, height=dp(20)))
            if key == 'category':
                sp = Spinner(text=default, values=FOOD_CATS, size_hint_y=None, height=dp(36),
                             font_size=sp(13), background_normal='', background_color=C['card'])
                lay.add_widget(sp); fields[key] = sp
            else:
                inp = TextInput(text=default, hint_text=hint, size_hint_y=None, height=dp(36),
                                font_size=sp(13), multiline=False,
                                input_filter='float' if key not in ('name','unit') else None,
                                background_normal='', background_color=C['card'])
                lay.add_widget(inp); fields[key] = inp

        sv = ScrollView(size_hint_y=1); sv.add_widget(lay)

        def save(inst):
            nm = fields['name'].text.strip()
            if not nm:
                toast('Food name is required!'); return
            try:
                dm.update_food(edit_name, nm, fields['category'].text,
                    float(fields['cal'].text or 0), float(fields['protein'].text or 0),
                    float(fields['carbs'].text or 0), float(fields['fat'].text or 0),
                    float(fields['fiber'].text or 0), float(fields['serving'].text or 1),
                    fields['unit'].text.strip() or 'serving') if edit_name else \
                dm.add_food(nm, fields['category'].text,
                    float(fields['cal'].text or 0), float(fields['protein'].text or 0),
                    float(fields['carbs'].text or 0), float(fields['fat'].text or 0),
                    float(fields['fiber'].text or 0), float(fields['serving'].text or 1),
                    fields['unit'].text.strip() or 'serving')
            except ValueError:
                toast('Please enter valid numbers!'); return
            popup.dismiss(); self._build(); toast(f'{nm} saved!')

        btns = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        btns.add_widget(btn('Cancel', bg=C['txt2'], size_hint_x=0.4))
        btns.add_widget(btn('💾 Save', bg=C['sec'], size_hint_x=0.6))
        btns.children[0].bind(on_release=save)
        btns.children[1].bind(on_release=lambda x: popup.dismiss())

        content = BoxLayout(orientation='vertical', spacing=dp(4))
        content.add_widget(Label(text=title, font_size=sp(16), bold=True, color=C['pri'], size_hint_y=None, height=dp(32)))
        content.add_widget(sv); content.add_widget(btns)

        popup = Popup(title='', content=content, size_hint=(0.92, 0.88),
                      background='', separator_color=(0,0,0,0))
        with popup.canvas.before:
            Color(*C['card'])
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(14)])
        popup.open()

    def _confirm_delete(self, name):
        ct = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        ct.add_widget(Label(text=f'Delete "{name}"?', font_size=sp(15), color=C['txt']))
        ct.add_widget(Label(text='This will also remove it from any future logging. Past diary entries are kept.',
                            font_size=sp(11), color=C['txt2']))
        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        bb.add_widget(btn('Cancel', bg=C['txt2'], size_hint_x=0.5))
        bb.add_widget(btn('Delete', bg=C['danger'], size_hint_x=0.5))
        p = Popup(title='', content=ct, size_hint=(0.75, 0.3), background='', separator_color=(0,0,0,0))
        bb.children[0].bind(on_release=lambda x: (App.get_running_app().dm.delete_food(name), p.dismiss(), self._build(), toast('Deleted!')))
        bb.children[1].bind(on_release=lambda x: p.dismiss())
        ct.add_widget(bb); p.open()


# ═══════════════════════════════════════════════════════════════════════════════
# DIARY SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

class DiaryScreen(Screen):
    def __init__(self, **kw): super().__init__(**kw); self._box = BoxLayout(); self.add_widget(self._box)
    def on_enter(self, *_): self._build()

    def _build(self):
        app = App.get_running_app(); dm = app.dm; dk = app.viewing_date
        day = dm.get_day(dk); totals = dm.get_totals(dk); goals = dm.get_goals()

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))

        # date bar
        dbar = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(4))
        pb = btn('◀', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        pb.bind(on_release=lambda x: self._chg_day(-1)); dbar.add_widget(pb)
        d = date.fromisoformat(dk); td = date.today()
        dl = 'Today' if dk == td.isoformat() else 'Yesterday' if dk == (td-timedelta(1)).isoformat() else d.strftime('%a %b %d')
        dbar.add_widget(Label(text=f'📔 {dl}', font_size=sp(16), bold=True, color=C['txt']))
        nb = btn('▶', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        nb.bind(on_release=lambda x: self._chg_day(1)); dbar.add_widget(nb)
        root.add_widget(dbar)

        # totals bar
        tbar = Card(orientation='horizontal', padding=[dp(8),dp(6)], size_hint_y=None, height=dp(30), spacing=dp(4))
        for lbl,k,col in [('🔥',C['cal'],'cal'),('🥩',C['pro'],'protein'),('🍞',C['carb'],'carbs'),('🧈',C['fat_c'],'fat'),('🥦',C['fib'],'fiber')]:
            tbar.add_widget(Label(text=f'{lbl}{int(totals[k])}/{goals[k+"s" if k!="fiber" else "fiber"] if k!="cal" else goals["calories"]}',
                                  font_size=sp(10), color=col, size_hint_x=0.2))
        root.add_widget(tbar)

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8), padding=dp(2))
        ct.bind(minimum_height=ct.setter('height'))

        for meal in MEAL_CATS:
            entries = day['meals'][meal]
            mc = Card(orientation='vertical', padding=dp(10), spacing=dp(4), size_hint_y=None)

            # meal header
            mh = BoxLayout(size_hint_y=None, height=dp(32))
            mh.add_widget(Label(text=f'{MEAL_ICON[meal]} {meal}', font_size=sp(14), bold=True, color=C['txt'], halign='left', size_hint_x=0.6))
            mcal = sum(e['cal'] for e in entries)
            mh.add_widget(Label(text=f'{int(mcal)} cal', font_size=sp(12), color=C['txt2'], halign='right', size_hint_x=0.25))
            addb = btn('+', bg=C['sec'], fs=sp(16), size_hint_x=0.15)
            addb.bind(on_release=lambda x,m=meal: self._pick_food(m))
            mh.add_widget(addb)
            mc.add_widget(mh)

            for idx, e in enumerate(entries):
                er = BoxLayout(size_hint_y=None, height=dp(28), padding=[dp(4),0])
                er.add_widget(Label(text=f'{e["name"]}  ×{e["servings"]}', font_size=sp(11), color=C['txt'], halign='left', size_hint_x=0.55))
                er.add_widget(Label(text=f'P:{int(e["protein"])}g C:{int(e["carbs"])}g F:{int(e["fat"])}g',
                                    font_size=sp(9), color=C['txt2'], size_hint_x=0.3))
                rb = btn('✕', bg=C['danger'], fs=sp(12), size_hint_x=0.15)
                rb.bind(on_release=lambda x,m=meal,i=idx: self._remove(m,i))
                er.add_widget(rb)
                mc.add_widget(er)

            if not entries:
                mc.add_widget(Label(text='Tap + to add food', font_size=sp(11), color=C['div'], size_hint_y=None, height=dp(22)))

            mc.height = dp(38) + (dp(28)*len(entries) if entries else dp(22))
            ct.add_widget(mc)

        # clear day button
        cb = btn('🗑️ Clear Entire Day', bg=C['danger'], fs=sp(12), size_hint_y=None, height=dp(38))
        cb.bind(on_release=lambda x: self._confirm_clear())
        ct.add_widget(cb)

        scr.add_widget(ct); root.add_widget(scr)
        self._box.add_widget(root)

    def _chg_day(self, delta):
        app = App.get_running_app()
        d = date.fromisoformat(app.viewing_date) + timedelta(delta)
        app.viewing_date = d.isoformat(); self._build()

    def _remove(self, meal, idx):
        App.get_running_app().dm.remove_entry(meal, idx, App.get_running_app().viewing_date)
        self._build()

    def _pick_food(self, meal):
        dm = App.get_running_app().dm; foods = dm.get_foods()
        if not foods:
            toast('No foods in database! Add some in the Foods tab.'); return

        lay = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))

        search = TextInput(hint_text='🔍 Search your foods...', size_hint_y=None, height=dp(38),
                           font_size=sp(14), multiline=False,
                           background_normal='', background_color=C['card'])
        lay.add_widget(search)
        lay.add_widget(Label(text=f'Adding to {MEAL_ICON[meal]} {meal}', font_size=sp(12), color=C['pri'], size_hint_y=None, height=dp(20)))

        scr = ScrollView()
        flist = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4))
        flist.bind(minimum_height=flist.setter('height'))

        food_btns = []
        for name, fi in foods.items():
            fb = btn(f'{name}  ({int(fi["cal"])} cal / {fi["serving"]} {fi["unit"]})',
                     bg=C['card'], fg=C['txt'], fs=sp(12), size_hint_y=None, height=dp(36))
            fb.bind(on_release=lambda x,n=name: self._set_servings(meal, n))
            flist.add_widget(fb); food_btns.append((fb, name, fi))

        scr.add_widget(flist); lay.add_widget(scr)
        lay.add_widget(btn('Cancel', bg=C['txt2'], size_hint_y=None, height=dp(38)))

        popup = Popup(title='Select Food', content=lay, size_hint=(0.9, 0.8),
                      background='', separator_color=(0,0,0,0))

        def do_search(inst, val):
            q = val.lower()
            for fb, nm, fi in food_btns:
                fb.opacity = 1 if q in nm.lower() else 0; fb.height = dp(36) if q in nm.lower() else 0
                fb.disabled = q not in nm.lower()

        search.bind(text=do_search)
        lay.children[0].bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def _set_servings(self, meal, food_name):
        fi = App.get_running_app().dm.get_food(food_name)
        lay = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        lay.add_widget(Label(text=food_name, font_size=sp(16), bold=True, color=C['txt']))
        lay.add_widget(Label(text=f'{fi["cal"]} cal | {fi["protein"]}g P | {fi["carbs"]}g C | {fi["fat"]}g F per {fi["serving"]} {fi["unit"]}',
                            font_size=sp(11), color=C['txt2']))
        lay.add_widget(Label(text='Number of servings:', font_size=sp(13), color=C['txt']))
        inp = TextInput(text='1', input_filter='float', size_hint_y=None, height=dp(40),
                        font_size=sp(16), multiline=False, background_normal='', background_color=C['card'])
        lay.add_widget(inp)
        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        bb.add_widget(btn('Cancel', bg=C['txt2'], size_hint_x=0.4))
        bb.add_widget(btn('✅ Add', bg=C['sec'], size_hint_x=0.6))

        p = Popup(title=f'{MEAL_ICON[meal]} {meal}', content=lay, size_hint=(0.8, 0.45),
                  background='', separator_color=(0,0,0,0))

        def add(inst):
            try: srv = float(inp.text or 0)
            except ValueError: toast('Enter a valid number!'); return
            if srv <= 0: toast('Enter a positive number!'); return
            App.get_running_app().dm.log_food(meal, food_name, srv, App.get_running_app().viewing_date)
            p.dismiss(); self._build(); toast(f'Added {food_name}!')
        bb.children[0].bind(on_release=add)
        bb.children[1].bind(on_release=lambda x: p.dismiss())
        lay.add_widget(bb); p.open()

    def _confirm_clear(self):
        ct = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        ct.add_widget(Label(text='Clear all entries for this day?', font_size=sp(15), color=C['txt']))
        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        bb.add_widget(btn('Cancel', bg=C['txt2'], size_hint_x=0.5))
        bb.add_widget(btn('Clear', bg=C['danger'], size_hint_x=0.5))
        p = Popup(title='', content=ct, size_hint=(0.7, 0.28), background='', separator_color=(0,0,0,0))
        bb.children[0].bind(on_release=lambda x: (App.get_running_app().dm.clear_day(App.get_running_app().viewing_date), p.dismiss(), self._build(), toast('Day cleared!')))
        bb.children[1].bind(on_release=lambda x: p.dismiss())
        ct.add_widget(bb); p.open()


# ═══════════════════════════════════════════════════════════════════════════════
# LEARN SCREEN (Education)
# ═══════════════════════════════════════════════════════════════════════════════

class LearnScreen(Screen):
    def __init__(self, **kw): super().__init__(**kw); self._box = BoxLayout(); self.add_widget(self._box)
    def on_enter(self, *_): self._show_topics()

    def _show_topics(self):
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))
        root.add_widget(Label(text='📚 Nutrition Library', font_size=sp(20), bold=True,
                              color=C['txt'], size_hint_y=None, height=dp(40)))
        scr = ScrollView()
        ct = GridLayout(cols=1, size_hint_y=None, spacing=dp(8), padding=dp(4))
        ct.bind(minimum_height=ct.setter('height'))

        colors = [C['cal'], C['pro'], C['carb'], C['fat_c'], C['fib'], C['water'],
                  C['acc'], C['sec'], C['pri'], C['danger'], [0.6,0.4,0.8,1], [0.4,0.7,0.5,1],
                  [0.8,0.6,0.3,1]]

        for i, topic in enumerate(EDU_TOPICS):
            col = colors[i % len(colors)]
            card = Card(orientation='horizontal', padding=[dp(12),dp(10)], size_hint_y=None, height=dp(54), spacing=dp(10))
            with card.canvas.before:
                Color(*col)
                rr = RoundedRectangle(pos=(card.x, card.y, dp(4), card.height), size=(dp(5), card.height), radius=[dp(2)])
            card.add_widget(Label(text=topic['icon'], font_size=sp(22), size_hint_x=0.12))
            info = BoxLayout(orientation='vertical', size_hint_x=0.78)
            info.add_widget(Label(text=topic['title'], font_size=sp(14), bold=True, color=C['txt'], halign='left'))
            if topic.get('calculator'):
                info.add_widget(Label(text='Interactive calculator', font_size=sp(10), color=col, halign='left'))
            elif topic.get('sections'):
                info.add_widget(Label(text=f'{len(topic["sections"])} sections • Tap to read', font_size=sp(10), color=C['txt2'], halign='left'))
            card.add_widget(info)
            card.add_widget(Label(text='›', font_size=sp(22), color=col, size_hint_x=0.1))
            card.bind(on_touch_down=lambda inst, touch, t=topic: self._on_tap(inst, touch, t))
            ct.add_widget(card)

        scr.add_widget(ct); root.add_widget(scr); self._box.add_widget(root)

    def _on_tap(self, inst, touch, topic):
        if not inst.collide_point(*touch.pos): return
        if topic.get('calculator'):
            self._show_calculator()
        else:
            self._show_article(topic)

    def _show_article(self, topic):
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))

        # back button
        bb = btn('← Back to Library', bg=C['pri_dk'], fs=sp(13), size_hint_y=None, height=dp(36))
        bb.bind(on_release=lambda x: self._show_topics())
        root.add_widget(bb)

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12), padding=dp(4))
        ct.bind(minimum_height=ct.setter('height'))

        # title
        ct.add_widget(Label(text=f'{topic["icon"]}  {topic["title"]}', font_size=sp(20),
                            bold=True, color=C['pri'], size_hint_y=None, height=dp(44)))

        for subtitle, text in topic.get('sections', []):
            # section card
            sc = Card(orientation='vertical', padding=dp(14), spacing=dp(4), size_hint_y=None)
            sc.add_widget(Label(text=subtitle, font_size=sp(15), bold=True, color=C['txt'],
                                size_hint_y=None, halign='left', valign='middle'))
            sc.children[0].bind(size=sc.children[0].setter('text_size'))
            sc.children[0].texture_update()
            sc.children[0].height = sc.children[0].texture_size[1] + dp(4)

            lbl = Label(text=text, font_size=sp(12), color=C['txt2'],
                        size_hint_y=None, halign='left', valign='top', markup=True)
            lbl.bind(size=lambda i,v: setattr(lbl, 'text_size', (v[0]-dp(8), None)))
            lbl.bind(texture_size=lambda i,v: setattr(lbl, 'height', v[1]+dp(8)))
            sc.add_widget(lbl)
            sc.height = dp(34) + sc.children[0].height + lbl.height + dp(20)
            ct.add_widget(sc)

        scr.add_widget(ct); root.add_widget(scr); self._box.add_widget(root)

    def _show_calculator(self):
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))

        bb = btn('← Back to Library', bg=C['pri_dk'], fs=sp(13), size_hint_y=None, height=dp(36))
        bb.bind(on_release=lambda x: self._show_topics())
        root.add_widget(bb)

        scr = ScrollView()
        ct = Card(orientation='vertical', padding=dp(16), spacing=dp(8), size_hint_y=None)
        ct.bind(minimum_height=ct.setter('height'))

        ct.add_widget(Label(text='🧮 BMI & TDEE Calculator', font_size=sp(18), bold=True,
                            color=C['pri'], size_hint_y=None, height=dp(36)))
        ct.add_widget(Label(text='Estimate your daily calorie needs based on your body and activity level.',
                            font_size=sp(11), color=C['txt2'], size_hint_y=None, height=dp(28)))

        self._calc_fields = {}
        for lbl, key, default, hint in [
            ('Age (years)','age','25','18-100'),
            ('Gender','gender','Male',''),
            ('Weight (kg)','weight','70','e.g. 70'),
            ('Height (cm)','height','175','e.g. 175'),
            ('Activity Level','activity','Moderately active (3-5 days/week)',''),
        ]:
            ct.add_widget(Label(text=lbl, font_size=sp(12), bold=True, color=C['txt'], halign='left', size_hint_y=None, height=dp(20)))
            if key == 'gender':
                sp = Spinner(text='Male', values=['Male','Female'], size_hint_y=None, height=dp(36),
                             font_size=sp(13), background_normal='', background_color=C['card'])
                ct.add_widget(sp); self._calc_fields[key] = sp
            elif key == 'activity':
                sp = Spinner(text='Moderately active (3-5 days/week)', values=[
                    'Sedentary (little/no exercise)',
                    'Lightly active (1-3 days/week)',
                    'Moderately active (3-5 days/week)',
                    'Very active (6-7 days/week)',
                    'Extra active (athlete/physical job)'
                ], size_hint_y=None, height=dp(36), font_size=sp(11),
                    background_normal='', background_color=C['card'])
                ct.add_widget(sp); self._calc_fields[key] = sp
            else:
                inp = TextInput(text=default, hint_text=hint, size_hint_y=None, height=dp(36),
                                font_size=sp(13), multiline=False, input_filter='float',
                                background_normal='', background_color=C['card'])
                ct.add_widget(inp); self._calc_fields[key] = inp

        cb = btn('📊 Calculate', bg=C['sec'], fs=sp(15), size_hint_y=None, height=dp(42))
        cb.bind(on_release=lambda x: self._do_calc())
        ct.add_widget(cb)

        self._result_card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(1))
        ct.add_widget(self._result_card)

        scr.add_widget(ct); root.add_widget(scr); self._box.add_widget(root)

    def _do_calc(self):
        try:
            age = float(self._calc_fields['age'].text)
            wt = float(self._calc_fields['weight'].text)
            ht = float(self._calc_fields['height'].text)
        except ValueError:
            toast('Please enter valid numbers!'); return

        gender = self._calc_fields['gender'].text
        act_text = self._calc_fields['activity'].text
        act_factors = {'Sedentary':1.2, 'Lightly active':1.375,
                       'Moderately active':1.55, 'Very active':1.725, 'Extra active':1.9}
        act_key = [k for k in act_factors if act_text.startswith(k)]
        af = act_factors.get(act_key[0], 1.55) if act_key else 1.55

        # BMI
        ht_m = ht / 100
        bmi = wt / (ht_m * ht_m) if ht_m > 0 else 0
        if bmi < 18.5: cat = 'Underweight'
        elif bmi < 25: cat = 'Normal weight'
        elif bmi < 30: cat = 'Overweight'
        else: cat = 'Obese'

        # BMR (Mifflin-St Jeor)
        if gender == 'Male':
            bmr = 10*wt + 6.25*ht - 5*age + 5
        else:
            bmr = 10*wt + 6.25*ht - 5*age - 161

        tdee = bmr * af

        # Macro suggestions
        pro_g = round(wt * 1.8)
        fat_g = round(tdee * 0.28 / 9)
        carb_g = round((tdee - pro_g*4 - fat_g*9) / 4)

        self._result_card.clear_widgets()
        self._result_card.height = dp(280)

        rc = Card(orientation='vertical', padding=dp(14), spacing=dp(6))
        rc.add_widget(Label(text='Your Results', font_size=sp(16), bold=True, color=C['sec'], size_hint_y=None, height=dp(28)))

        rc.add_widget(Label(text=f'BMI: {bmi:.1f}  ({cat})', font_size=sp(15), bold=True, color=C['txt'], size_hint_y=None, height=dp(26)))
        rc.add_widget(Label(text=f'BMR: {int(bmr)} cal/day (at rest)', font_size=sp(13), color=C['txt2'], size_hint_y=None, height=dp(22)))
        rc.add_widget(Label(text=f'TDEE: {int(tdee)} cal/day', font_size=sp(15), bold=True, color=C['cal'], size_hint_y=None, height=dp(26)))
        rc.add_widget(Label(text=f'Activity factor: {af}', font_size=sp(11), color=C['txt2'], size_hint_y=None, height=dp(18)))

        rc.add_widget(Label(text='── Suggested Daily Targets ──', font_size=sp(12), color=C['pri'], size_hint_y=None, height=dp(22)))
        rc.add_widget(Label(text=f'🔥 Maintain weight: {int(tdee)} cal', font_size=sp(13), color=C['txt'], size_hint_y=None, height=dp(22)))
        rc.add_widget(Label(text=f'📉 Lose 0.5 kg/week: {int(tdee-500)} cal', font_size=sp(13), color=C['cal'], size_hint_y=None, height=dp(22)))
        rc.add_widget(Label(text=f'📈 Gain 0.5 kg/week: {int(tdee+500)} cal', font_size=sp(13), color=C['sec'], size_hint_y=None, height=dp(22)))
        rc.add_widget(Label(text=f'🥩 Protein: ~{pro_g}g  |  🧈 Fat: ~{fat_g}g  |  🍞 Carbs: ~{carb_g}g',
                            font_size=sp(12), color=C['txt2'], size_hint_y=None, height=dp(22)))

        self._result_card.add_widget(rc)


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

class SettingsScreen(Screen):
    def __init__(self, **kw): super().__init__(**kw); self._box = BoxLayout(); self.add_widget(self._box)
    def on_enter(self, *_): self._build()

    def _build(self):
        dm = App.get_running_app().dm; goals = dm.get_goals()
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))
        root.add_widget(Label(text='⚙️ Settings', font_size=sp(20), bold=True,
                              color=C['txt'], size_hint_y=None, height=dp(40)))

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10), padding=dp(4))
        ct.bind(minimum_height=ct.setter('height'))

        # goals card
        gc = Card(orientation='vertical', padding=dp(14), spacing=dp(8))
        gc.add_widget(Label(text='🎯 Daily Goals', font_size=sp(16), bold=True, color=C['pri'], halign='left', size_hint_y=None, height=dp(28)))

        self._goal_inputs = {}
        for lbl, key, default in [
            ('Calories (kcal)','calories', goals['calories']),
            ('Protein (g)','protein', goals['protein']),
            ('Carbs (g)','carbs', goals['carbs']),
            ('Fat (g)','fat', goals['fat']),
            ('Fiber (g)','fiber', goals['fiber']),
            ('Water (glasses)','water', goals['water']),
        ]:
            row = BoxLayout(size_hint_y=None, height=dp(36))
            row.add_widget(Label(text=lbl, font_size=sp(12), color=C['txt'], halign='left', size_hint_x=0.5))
            inp = TextInput(text=str(default), input_filter='int', size_hint_x=0.5,
                           font_size=sp(13), multiline=False, background_normal='', background_color=C['card'])
            row.add_widget(inp); gc.add_widget(row)
            self._goal_inputs[key] = inp

        sb = btn('💾 Save Goals', bg=C['sec'], size_hint_y=None, height=dp(40))
        sb.bind(on_release=lambda x: self._save_goals())
        gc.add_widget(sb)
        ct.add_widget(gc)

        # data card
        dc = Card(orientation='vertical', padding=dp(14), spacing=dp(8))
        dc.add_widget(Label(text='💾 Data Management', font_size=sp(16), bold=True, color=C['pri'], halign='left', size_hint_y=None, height=dp(28)))

        foods = dm.get_foods()
        dates = dm.get_dates()
        dc.add_widget(Label(text=f'Food database: {len(foods)} items', font_size=sp(12), color=C['txt'], halign='left', size_hint_y=None, height=dp(22)))
        dc.add_widget(Label(text=f'Diary days: {len(dates)} days logged', font_size=sp(12), color=C['txt'], halign='left', size_hint_y=None, height=dp(22)))

        eb = btn('📋 Export Data (JSON)', bg=C['pri'], size_hint_y=None, height=dp(36))
        eb.bind(on_release=lambda x: self._export())
        dc.add_widget(eb)
        ct.add_widget(dc)

        # about card
        ac = Card(orientation='vertical', padding=dp(14), spacing=dp(4))
        ac.add_widget(Label(text='ℹ️ About NutriTrack', font_size=sp(16), bold=True, color=C['pri'], halign='left', size_hint_y=None, height=dp(28)))
        ac.add_widget(Label(text='A 100% local nutrition tracker.\nNo APIs. No AI. No cloud.\nYour data stays on YOUR device.\n\nBuild your own food database,\ntrack daily intake, and learn\nnutrition fundamentals.', 
                            font_size=sp(12), color=C['txt2'], size_hint_y=None, height=dp(120)))
        ct.add_widget(ac)

        scr.add_widget(ct); root.add_widget(scr); self._box.add_widget(root)

    def _save_goals(self):
        try:
            goals = {k: int(v.text) for k,v in self._goal_inputs.items()}
            if any(v < 0 for v in goals.values()):
                toast('Goals must be positive!'); return
            App.get_running_app().dm.set_goals(**goals)
            toast('Goals saved! ✓')
        except ValueError:
            toast('Please enter valid numbers!')

    def _export(self):
        dm = App.get_running_app().dm
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "nutritrack_export.json")
        with open(path,'w') as f: json.dump(dm.data, f, indent=2)
        toast(f'Exported to {path}')


# ═══════════════════════════════════════════════════════════════════════════════
# APP WITH BOTTOM NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

class NutriTrackApp(App):
    def build(self):
        self.dm = DataManager()
        self.viewing_date = self.dm.today_key()

        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(FoodsScreen(name='foods'))
        self.sm.add_widget(DiaryScreen(name='diary'))
        self.sm.add_widget(LearnScreen(name='learn'))
        self.sm.add_widget(SettingsScreen(name='settings'))

        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.sm)

        # bottom nav
        nav = BoxLayout(size_hint_y=None, height=dp(58), spacing=dp(0), padding=[dp(2),0,dp(2),dp(2)])
        with nav.canvas.before:
            Color(*C['card'])
            self._nav_bg = RoundedRectangle(pos=nav.pos, size=nav.size, radius=[0])
        nav.bind(pos=lambda i,v: setattr(self._nav_bg,'pos',v),
                 size=lambda i,v: setattr(self._nav_bg,'size',v))

        tabs = [('🏠','Home','home'),('🍎','Foods','foods'),
                ('📔','Diary','diary'),('📚','Learn','learn'),('⚙️','Settings','settings')]
        self._nav_btns = []
        for icon, label, key in tabs:
            b = ToggleButton(text=f'{icon}\n{label}', font_size=sp(10),
                             color=C['txt2'], background_normal='',
                             background_down='', background_color=(0,0,0,0),
                             group='nav', allow_no_selection=False)
            b.key = key
            b.bind(on_release=lambda inst, k=key: self._switch(k))
            nav.add_widget(b); self._nav_btns.append(b)

        self.root.add_widget(nav)
        self._switch('home')
        return self.root

    def _switch(self, key):
        self.sm.current = key
        self.viewing_date = self.dm.today_key()  # reset to today on tab switch
        for b in self._nav_btns:
            if b.key == key:
                b.color = C['pri']
                with b.canvas.after:
                    Color(*C['pri'])
                    RoundedRectangle(pos=(b.x, b.y), size=(b.width, dp(3)), radius=[dp(1)])
            else:
                b.color = C['txt2']
                b.canvas.after.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    NutriTrackApp().run()
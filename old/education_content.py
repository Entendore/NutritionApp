"""
NutriTrack — Built-in nutrition education library.
All content is local — no API or AI required.
"""

EDU_TOPICS = [
    {'title': 'Understanding Calories', 'icon': '🔥', 'sections': [
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

    {'title': 'Protein Guide', 'icon': '🥩', 'sections': [
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

    {'title': 'Carbohydrates Guide', 'icon': '🍞', 'sections': [
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

    {'title': 'Fats Guide', 'icon': '🥑', 'sections': [
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

    {'title': 'Fiber Guide', 'icon': '🥦', 'sections': [
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

    {'title': 'Vitamins Overview', 'icon': '💊', 'sections': [
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

    {'title': 'Minerals Overview', 'icon': '⚡', 'sections': [
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

    {'title': 'Hydration', 'icon': '💧', 'sections': [
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

    {'title': 'Reading Nutrition Labels', 'icon': '🏷️', 'sections': [
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

    {'title': 'Healthy Plate Method', 'icon': '🍽️', 'sections': [
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

    {'title': 'BMI & TDEE Calculator', 'icon': '🧮', 'calculator': True},

    {'title': 'Nutrition Myths Debunked', 'icon': '❌', 'sections': [
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

    {'title': 'Eating on a Budget', 'icon': '💰', 'sections': [
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
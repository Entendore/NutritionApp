"""
NutriTrack — Education screen.
Browse built-in nutrition articles and use the BMI/TDEE calculator.
"""

import math

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp

from constants import C
from education_content import EDU_TOPICS
from widgets import Card, btn, toast


class EducationScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._box = BoxLayout()
        self.add_widget(self._box)

    def on_enter(self, *_):
        self._build()

    def _build(self):
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))

        root.add_widget(Label(text='📚 Nutrition Education', font_size=sp(18),
                              bold=True, color=C['txt'],
                              size_hint_y=None, height=dp(36)))

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None,
                       spacing=dp(8), padding=dp(2))
        ct.bind(minimum_height=ct.setter('height'))

        for topic in EDU_TOPICS:
            tc = Card(orientation='vertical', padding=dp(12), spacing=dp(4),
                      size_hint_y=None, height=dp(56))
            h = BoxLayout(size_hint_y=0.6)
            h.add_widget(Label(text=f'{topic["icon"]}  {topic["title"]}',
                               font_size=sp(14), bold=True, color=C['txt'],
                               halign='left'))
            tc.add_widget(h)
            sub = ('Calculator' if topic.get('calculator')
                   else f'{len(topic.get("sections", []))} sections')
            tc.add_widget(Label(text=sub, font_size=sp(11),
                                color=C['txt2'], halign='left', size_hint_y=0.4))
            open_b = btn('Read', bg=C['pri'], fs=sp(12), size_hint_y=None, height=dp(30))
            if topic.get('calculator'):
                open_b.bind(on_release=lambda x, t=topic: self._show_calculator())
            else:
                open_b.bind(on_release=lambda x, t=topic: self._show_topic(t))
            tc.add_widget(open_b)
            ct.add_widget(tc)

        scr.add_widget(ct)
        root.add_widget(scr)
        self._box.add_widget(root)

    # ── Topic Reader ───────────────────────────────────────────────────────

    def _show_topic(self, topic):
        lay = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(12))

        header = BoxLayout(size_hint_y=None, height=dp(36))
        header.add_widget(Label(
            text=f'{topic["icon"]}  {topic["title"]}',
            font_size=sp(16), bold=True, color=C['pri']))
        lay.add_widget(header)

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(12))
        ct.bind(minimum_height=ct.setter('height'))

        for section_title, section_text in topic.get('sections', []):
            sc = Card(orientation='vertical', padding=dp(12), spacing=dp(4),
                      size_hint_y=None)
            sc.add_widget(Label(text=section_title, font_size=sp(14), bold=True,
                                color=C['txt'], size_hint_y=None, halign='left'))
            sc.add_widget(Label(text=section_text, font_size=sp(12),
                                color=C['txt2'], halign='left',
                                size_hint_y=None, markup=False))
            # Force height calculation
            sc.bind(minimum_height=sc.setter('height'))
            for child in sc.children:
                child.bind(size=sc.setter('height'))
            ct.add_widget(sc)

        scr.add_widget(ct)
        lay.add_widget(scr)
        close_b = btn('Close', bg=C['pri'], size_hint_y=None, height=dp(40))
        lay.add_widget(close_b)

        popup = Popup(title='', content=lay, size_hint=(0.95, 0.92),
                      background='', separator_color=(0, 0, 0, 0))
        close_b.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    # ── BMI / TDEE Calculator ──────────────────────────────────────────────

    def _show_calculator(self):
        lay = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(16))

        lay.add_widget(Label(text='🧮 BMI & TDEE Calculator',
                             font_size=sp(16), bold=True, color=C['pri'],
                             size_hint_y=None, height=dp(32)))

        fields = {}
        for lbl, key, hint in [
            ('Age (years)', 'age', 'e.g. 30'),
            ('Weight (kg)', 'weight', 'e.g. 70'),
            ('Height (cm)', 'height', 'e.g. 175'),
        ]:
            lay.add_widget(Label(text=lbl, font_size=sp(12), color=C['txt'],
                                 halign='left', size_hint_y=None, height=dp(20)))
            inp = TextInput(hint_text=hint, size_hint_y=None, height=dp(36),
                            font_size=sp(14), multiline=False,
                            input_filter='float',
                            background_normal='', background_color=C['card'])
            lay.add_widget(inp)
            fields[key] = inp

        # Gender
        lay.add_widget(Label(text='Gender', font_size=sp(12), color=C['txt'],
                             halign='left', size_hint_y=None, height=dp(20)))
        gender_row = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(8))
        male_b = ToggleButton(text='♂ Male', group='gender', font_size=sp(13),
                              background_normal='', background_color=C['pri'])
        female_b = ToggleButton(text='♀ Female', group='gender', font_size=sp(13),
                                background_normal='', background_color=C['pri'])
        gender_row.add_widget(male_b)
        gender_row.add_widget(female_b)
        lay.add_widget(gender_row)

        # Activity
        lay.add_widget(Label(text='Activity Level', font_size=sp(12), color=C['txt'],
                             halign='left', size_hint_y=None, height=dp(20)))
        act_spin = Spinner(
            text='Moderate (3-5 days/week)',
            values=['Sedentary (little/no exercise)',
                    'Light (1-3 days/week)',
                    'Moderate (3-5 days/week)',
                    'Active (6-7 days/week)',
                    'Very Active (2x/day or physical job)'],
            size_hint_y=None, height=dp(36), font_size=sp(12),
            background_normal='', background_color=C['card'])
        lay.add_widget(act_spin)

        result_label = Label(text='', font_size=sp(13), color=C['txt'],
                             size_hint_y=None, height=dp(80),
                             halign='left', valign='top')
        result_label.bind(size=result_label.setter('text_size'))
        lay.add_widget(result_label)

        calc_b = btn('Calculate', bg=C['sec'], size_hint_y=None, height=dp(40))
        close_b = btn('Close', bg=C['txt2'], size_hint_y=None, height=dp(40))
        btn_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
        btn_row.add_widget(calc_b)
        btn_row.add_widget(close_b)
        lay.add_widget(btn_row)

        popup = Popup(title='', content=lay, size_hint=(0.9, 0.85),
                      background='', separator_color=(0, 0, 0, 0))

        def calculate(inst):
            try:
                age = float(fields['age'].text)
                wt = float(fields['weight'].text)
                ht = float(fields['height'].text)
            except ValueError:
                toast('Enter valid numbers!')
                return
            if not (male_b.state == 'down' or female_b.state == 'down'):
                toast('Select gender!')
                return

            bmi = wt / ((ht / 100) ** 2)
            if male_b.state == 'down':
                bmr = 10 * wt + 6.25 * ht - 5 * age + 5
            else:
                bmr = 10 * wt + 6.25 * ht - 5 * age - 161

            act_map = {
                'Sedentary (little/no exercise)': 1.2,
                'Light (1-3 days/week)': 1.375,
                'Moderate (3-5 days/week)': 1.55,
                'Active (6-7 days/week)': 1.725,
                'Very Active (2x/day or physical job)': 1.9,
            }
            tdee = bmr * act_map.get(act_spin.text, 1.55)

            if bmi < 18.5:
                cat = 'Underweight'
            elif bmi < 25:
                cat = 'Normal weight'
            elif bmi < 30:
                cat = 'Overweight'
            else:
                cat = 'Obese'

            result_label.text = (
                f'BMI: {bmi:.1f} ({cat})\n'
                f'BMR: {int(bmr)} kcal/day\n'
                f'TDEE: {int(tdee)} kcal/day\n'
                f'Lose: {int(tdee - 500)} kcal | Gain: {int(tdee + 500)} kcal'
            )

        calc_b.bind(on_release=calculate)
        close_b.bind(on_release=lambda x: popup.dismiss())
        popup.open()
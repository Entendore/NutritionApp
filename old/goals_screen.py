"""
NutriTrack — Goals & History screens.
Set daily nutrition targets and review past days.
"""

from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp

from constants import C, MEAL_CATS, MEAL_ICON
from widgets import Card, PBar, btn, toast


# ═══════════════════════════════════════════════════════════════════════════
# GOALS SCREEN
# ═══════════════════════════════════════════════════════════════════════════

class GoalsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._box = BoxLayout()
        self.add_widget(self._box)

    def on_enter(self, *_):
        self._build()

    def _build(self):
        dm = App.get_running_app().dm
        goals = dm.get_goals()

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(12))

        root.add_widget(Label(text='🎯 Daily Goals', font_size=sp(18),
                              bold=True, color=C['txt'],
                              size_hint_y=None, height=dp(36)))

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None,
                       spacing=dp(8), padding=dp(4))
        ct.bind(minimum_height=ct.setter('height'))

        self._fields = {}
        field_defs = [
            ('Calories (kcal)', 'calories', goals['calories']),
            ('Protein (g)', 'protein', goals['protein']),
            ('Carbs (g)', 'carbs', goals['carbs']),
            ('Fat (g)', 'fat', goals['fat']),
            ('Fiber (g)', 'fiber', goals['fiber']),
            ('Water (glasses)', 'water', goals['water']),
        ]

        for lbl, key, default in field_defs:
            fc = Card(orientation='vertical', padding=dp(10), spacing=dp(2),
                      size_hint_y=None, height=dp(70))
            fc.add_widget(Label(text=lbl, font_size=sp(13), bold=True,
                                color=C['txt'], halign='left', size_hint_y=0.35))
            inp = TextInput(text=str(default), size_hint_y=None, height=dp(34),
                            font_size=sp(15), multiline=False,
                            input_filter='int',
                            background_normal='', background_color=C['card'])
            fc.add_widget(inp)
            self._fields[key] = inp
            ct.add_widget(fc)

        # Preset buttons
        preset_card = Card(orientation='vertical', padding=dp(10), spacing=dp(4),
                           size_hint_y=None, height=dp(90))
        preset_card.add_widget(Label(text='Quick Presets', font_size=sp(13),
                                     bold=True, color=C['txt'],
                                     halign='left', size_hint_y=0.25))
        preset_row1 = BoxLayout(size_hint_y=0.35, spacing=dp(4))
        for name, vals in [('Weight Loss',  {'calories': 1500, 'protein': 150, 'carbs': 150, 'fat': 50, 'fiber': 30, 'water': 10}),
                            ('Maintenance', {'calories': 2000, 'protein': 150, 'carbs': 250, 'fat': 65, 'fiber': 30, 'water': 8})]:
            pb = btn(name, bg=C['pri'], fs=sp(11), size_hint_x=0.5)
            pb.bind(on_release=lambda x, v=vals: self._apply_preset(v))
            preset_row1.add_widget(pb)
        preset_card.add_widget(preset_row1)

        preset_row2 = BoxLayout(size_hint_y=0.35, spacing=dp(4))
        for name, vals in [('Muscle Gain',  {'calories': 2500, 'protein': 200, 'carbs': 300, 'fat': 80, 'fiber': 35, 'water': 10}),
                            ('Keto',         {'calories': 1800, 'protein': 120, 'carbs': 30,  'fat': 140, 'fiber': 25, 'water': 10})]:
            pb = btn(name, bg=C['acc'], fs=sp(11), size_hint_x=0.5)
            pb.bind(on_release=lambda x, v=vals: self._apply_preset(v))
            preset_row2.add_widget(pb)
        preset_card.add_widget(preset_row2)
        ct.add_widget(preset_card)

        scr.add_widget(ct)
        root.add_widget(scr)

        save_b = btn('💾 Save Goals', bg=C['sec'], fs=sp(16),
                     size_hint_y=None, height=dp(48))
        save_b.bind(on_release=self._save_goals)
        root.add_widget(save_b)

        self._box.add_widget(root)

    def _apply_preset(self, vals):
        for key, val in vals.items():
            if key in self._fields:
                self._fields[key].text = str(val)
        toast('Preset applied — tap Save to confirm!')

    def _save_goals(self, inst):
        try:
            vals = {k: max(int(v.text or 0), 1) for k, v in self._fields.items()}
        except ValueError:
            toast('Enter valid numbers!')
            return
        App.get_running_app().dm.set_goals(**vals)
        toast('Goals saved!')


# ═══════════════════════════════════════════════════════════════════════════
# HISTORY SCREEN
# ═══════════════════════════════════════════════════════════════════════════

class HistoryScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._box = BoxLayout()
        self.add_widget(self._box)

    def on_enter(self, *_):
        self._build()

    def _build(self):
        dm = App.get_running_app().dm
        goals = dm.get_goals()
        dates = dm.get_dates()

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))

        root.add_widget(Label(text='📊 History', font_size=sp(18),
                              bold=True, color=C['txt'],
                              size_hint_y=None, height=dp(36)))

        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None,
                       spacing=dp(6), padding=dp(2))
        ct.bind(minimum_height=ct.setter('height'))

        if not dates:
            ct.add_widget(Label(text='No history yet!\nLog some meals to see data here.',
                                font_size=sp(14), color=C['txt2'],
                                size_hint_y=None, height=dp(100)))

        for dk in dates:
            totals = dm.get_totals(dk)
            water = dm.get_water(dk)
            day = dm.get_day(dk)

            dc = Card(orientation='vertical', padding=dp(10), spacing=dp(4),
                      size_hint_y=None)

            d = date.fromisoformat(dk)
            td = date.today()
            dl = ('Today' if dk == td.isoformat()
                  else 'Yesterday' if dk == (td - timedelta(1)).isoformat()
                  else d.strftime('%a %b %d'))

            dh = BoxLayout(size_hint_y=None, height=dp(28))
            dh.add_widget(Label(text=dl, font_size=sp(14), bold=True,
                                color=C['txt'], halign='left', size_hint_x=0.6))
            dh.add_widget(Label(text=f'{int(totals["cal"])} cal',
                                font_size=sp(13), color=C['cal'],
                                halign='right', size_hint_x=0.4))
            dc.add_widget(dh)

            # Mini progress bars
            for lbl, k, col, gk in [('P', 'protein', C['pro'], 'protein'),
                                      ('C', 'carbs', C['carb'], 'carbs'),
                                      ('F', 'fat', C['fat_c'], 'fat')]:
                row = BoxLayout(size_hint_y=None, height=dp(16))
                row.add_widget(Label(text=lbl, font_size=sp(9), bold=True,
                                     color=col, size_hint_x=0.08))
                row.add_widget(PBar(progress=totals[k], max_val=max(goals[gk], 1),
                                    bar_col=col, size_hint_x=0.72))
                row.add_widget(Label(text=f'{int(totals[k])}/{goals[gk]}',
                                     font_size=sp(9), color=C['txt2'],
                                     size_hint_x=0.2))
                dc.add_widget(row)

            dc.add_widget(Label(text=f'💧 {water}/{goals["water"]} glasses',
                                font_size=sp(10), color=C['water'],
                                halign='left', size_hint_y=None, height=dp(18)))

            # View button
            vb = btn('View in Diary', bg=C['pri'], fs=sp(11),
                     size_hint_y=None, height=dp(28))
            vb.bind(on_release=lambda x, d=dk: self._go_to_day(d))
            dc.add_widget(vb)

            dc.height = dp(28) + dp(16) * 3 + dp(18) + dp(28) + dp(16)
            ct.add_widget(dc)

        scr.add_widget(ct)
        root.add_widget(scr)
        self._box.add_widget(root)

    def _go_to_day(self, dk):
        app = App.get_running_app()
        app.viewing_date = dk
        app.sm.current = 'home'
"""
NutriTrack — Home / Dashboard screen.
Shows daily summary: calories, macros, water, meal overview.
"""

from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle

from constants import C, MEAL_CATS, MEAL_ICON, MEAL_BG
from widgets import Card, PBar, MacroRow, btn


class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._box = BoxLayout()
        self.add_widget(self._box)

    def on_enter(self, *_):
        self._build()

    def _build(self):
        app = App.get_running_app()
        dm = app.dm
        dk = app.viewing_date
        goals = dm.get_goals()
        totals = dm.get_totals(dk)
        water = dm.get_water(dk)

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))
        self._box.add_widget(root)

        # ── Date bar ───────────────────────────────────────────────────────
        dbar = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(4))
        pb = btn('◀', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        pb.bind(on_release=lambda x: self._chg_day(-1))
        dbar.add_widget(pb)

        d = date.fromisoformat(dk)
        td = date.today()
        dl = ('Today' if dk == td.isoformat()
              else 'Yesterday' if dk == (td - timedelta(1)).isoformat()
              else d.strftime('%a %b %d'))
        dbar.add_widget(Label(text=dl, font_size=sp(16), bold=True, color=C['txt']))

        nb = btn('▶', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        nb.bind(on_release=lambda x: self._chg_day(1))
        dbar.add_widget(nb)
        root.add_widget(dbar)

        # ── Scrollable content ─────────────────────────────────────────────
        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None,
                       spacing=dp(10), padding=[dp(4), dp(4), dp(4), dp(8)])
        ct.bind(minimum_height=ct.setter('height'))

        # Calorie card
        cc = Card(orientation='vertical', padding=dp(14), spacing=dp(4),
                  size_hint_y=None, height=dp(125))
        cc.add_widget(Label(text=str(int(totals['cal'])), font_size=sp(40),
                            bold=True, color=C['cal'], size_hint_y=0.48))
        rem = int(goals['calories'] - totals['cal'])
        cc.add_widget(Label(
            text=f'{rem} cal remaining' if rem >= 0 else f'{abs(rem)} cal over!',
            font_size=sp(13), color=C['txt2'], size_hint_y=0.18))
        pct = totals['cal'] / max(goals['calories'], 1)
        cc.add_widget(PBar(progress=totals['cal'], max_val=max(goals['calories'], 1),
                           bar_col=C['cal'] if pct <= 1 else C['danger'],
                           size_hint_y=0.18))
        cc.add_widget(Label(text=f'{int(pct * 100)}% of {goals["calories"]} goal',
                            font_size=sp(11), color=C['txt2'], size_hint_y=0.16))
        ct.add_widget(cc)

        # Macros card
        mc = Card(orientation='vertical', padding=dp(12), spacing=dp(1),
                  size_hint_y=None, height=dp(155))
        mc.add_widget(Label(text='Macronutrients', font_size=sp(14), bold=True,
                            color=C['txt'], size_hint_y=0.16, halign='left'))
        for lbl, k, col in [('Protein', 'protein', C['pro']),
                             ('Carbs', 'carbs', C['carb']),
                             ('Fat', 'fat', C['fat_c']),
                             ('Fiber', 'fiber', C['fib'])]:
            mc.add_widget(MacroRow(lbl, totals[k], goals[k], col, size_hint_y=0.21))
        ct.add_widget(mc)

        # Water card
        wc = Card(orientation='vertical', padding=dp(12), spacing=dp(4),
                  size_hint_y=None, height=dp(100))
        wh = BoxLayout(size_hint_y=0.4)
        wh.add_widget(Label(text='💧 Water', font_size=sp(14), bold=True,
                            color=C['txt'], halign='left', size_hint_x=0.5))
        wh.add_widget(Label(text=f'{water} / {goals["water"]} glasses',
                            font_size=sp(14), color=C['water'],
                            halign='right', size_hint_x=0.5))
        wc.add_widget(wh)
        wc.add_widget(PBar(progress=water, max_val=max(goals['water'], 1),
                           bar_col=C['water'], size_hint_y=0.25))
        wb = BoxLayout(size_hint_y=0.35, spacing=dp(8))
        mb = btn('−', bg=C['danger'], fs=sp(16), size_hint_x=0.3)
        mb.bind(on_release=lambda x: (dm.rem_water(dk), self._build()))
        ab = btn('+ Add Glass', bg=C['water'], fs=sp(13), size_hint_x=0.7)
        ab.bind(on_release=lambda x: (dm.add_water(dk), self._build()))
        wb.add_widget(mb)
        wb.add_widget(ab)
        wc.add_widget(wb)
        ct.add_widget(wc)

        # Meals summary
        day = dm.get_day(dk)
        for meal in MEAL_CATS:
            entries = day['meals'][meal]
            mc2 = Card(orientation='vertical', padding=dp(10), spacing=dp(4),
                       size_hint_y=None)
            h = BoxLayout(size_hint_y=None, height=dp(28))
            with h.canvas.before:
                Color(*MEAL_BG[meal])
                _r = RoundedRectangle(pos=h.pos, size=h.size, radius=[dp(6)])
            h.bind(pos=lambda i, v, _r=_r: setattr(_r, 'pos', v),
                   size=lambda i, v, _r=_r: setattr(_r, 'size', v))
            h.add_widget(Label(text=f'{MEAL_ICON[meal]} {meal}', font_size=sp(13),
                               bold=True, color=C['txt'], halign='left', size_hint_x=0.6))
            mcal = sum(e['cal'] for e in entries)
            h.add_widget(Label(text=f'{int(mcal)} cal', font_size=sp(12),
                               color=C['txt2'], halign='right', size_hint_x=0.4))
            mc2.add_widget(h)
            if entries:
                for e in entries:
                    r = BoxLayout(size_hint_y=None, height=dp(24), padding=[dp(8), 0])
                    r.add_widget(Label(text=f'{e["name"]}  ×{e["servings"]}',
                                       font_size=sp(11), color=C['txt2'],
                                       halign='left', size_hint_x=0.7))
                    r.add_widget(Label(text=f'{int(e["cal"])} cal',
                                       font_size=sp(11), color=C['txt2'],
                                       halign='right', size_hint_x=0.3))
                    mc2.add_widget(r)
                mc2.height = dp(32) + dp(24) * len(entries)
            else:
                mc2.add_widget(Label(text='No entries', font_size=sp(11),
                                     color=C['div'], size_hint_y=None, height=dp(22)))
                mc2.height = dp(54)
            ct.add_widget(mc2)

        scr.add_widget(ct)
        root.add_widget(scr)

    def _chg_day(self, delta):
        app = App.get_running_app()
        d = date.fromisoformat(app.viewing_date) + timedelta(delta)
        app.viewing_date = d.isoformat()
        self._build()
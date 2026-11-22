"""
NutriTrack — Diary screen.
Log foods to meals, view daily breakdown, remove entries.
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

from constants import C, MEAL_CATS, MEAL_ICON, MEAL_BG
from widgets import Card, btn, toast


class DiaryScreen(Screen):
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
        day = dm.get_day(dk)
        totals = dm.get_totals(dk)
        goals = dm.get_goals()

        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(4), padding=dp(8))

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
        dbar.add_widget(Label(text=f'📔 {dl}', font_size=sp(16),
                              bold=True, color=C['txt']))

        nb = btn('▶', bg=C['pri_dk'], fs=sp(18), size_hint_x=0.12)
        nb.bind(on_release=lambda x: self._chg_day(1))
        dbar.add_widget(nb)
        root.add_widget(dbar)

        # ── Totals bar ─────────────────────────────────────────────────────
        tbar = Card(orientation='horizontal', padding=[dp(8), dp(6)],
                    size_hint_y=None, height=dp(30), spacing=dp(4))
        for lbl, k, col in [('🔥', C['cal'], 'cal'), ('🥩', C['pro'], 'protein'),
                             ('🍞', C['carb'], 'carbs'), ('🧈', C['fat_c'], 'fat'),
                             ('🥦', C['fib'], 'fiber')]:
            goal_key = 'calories' if k == 'cal' else k
            tbar.add_widget(Label(
                text=f'{lbl}{int(totals[k])}/{goals[goal_key]}',
                font_size=sp(10), color=col, size_hint_x=0.2))
        root.add_widget(tbar)

        # ── Scrollable meals ───────────────────────────────────────────────
        scr = ScrollView()
        ct = BoxLayout(orientation='vertical', size_hint_y=None,
                       spacing=dp(8), padding=dp(2))
        ct.bind(minimum_height=ct.setter('height'))

        for meal in MEAL_CATS:
            entries = day['meals'][meal]
            mc = Card(orientation='vertical', padding=dp(10), spacing=dp(4),
                      size_hint_y=None)

            mh = BoxLayout(size_hint_y=None, height=dp(32))
            mh.add_widget(Label(text=f'{MEAL_ICON[meal]} {meal}',
                                font_size=sp(14), bold=True, color=C['txt'],
                                halign='left', size_hint_x=0.6))
            mcal = sum(e['cal'] for e in entries)
            mh.add_widget(Label(text=f'{int(mcal)} cal', font_size=sp(12),
                                color=C['txt2'], halign='right', size_hint_x=0.25))
            addb = btn('+', bg=C['sec'], fs=sp(16), size_hint_x=0.15)
            addb.bind(on_release=lambda x, m=meal: self._pick_food(m))
            mh.add_widget(addb)
            mc.add_widget(mh)

            for idx, e in enumerate(entries):
                er = BoxLayout(size_hint_y=None, height=dp(28), padding=[dp(4), 0])
                er.add_widget(Label(text=f'{e["name"]}  ×{e["servings"]}',
                                    font_size=sp(11), color=C['txt'],
                                    halign='left', size_hint_x=0.55))
                er.add_widget(Label(
                    text=f'P:{int(e["protein"])}g C:{int(e["carbs"])}g F:{int(e["fat"])}g',
                    font_size=sp(9), color=C['txt2'], size_hint_x=0.3))
                rb = btn('✕', bg=C['danger'], fs=sp(12), size_hint_x=0.15)
                rb.bind(on_release=lambda x, m=meal, i=idx: self._remove(m, i))
                er.add_widget(rb)
                mc.add_widget(er)

            if not entries:
                mc.add_widget(Label(text='Tap + to add food', font_size=sp(11),
                                    color=C['div'], size_hint_y=None, height=dp(22)))

            mc.height = dp(38) + (dp(28) * len(entries) if entries else dp(22))
            ct.add_widget(mc)

        # Clear day button
        cb = btn('🗑️ Clear Entire Day', bg=C['danger'], fs=sp(12),
                 size_hint_y=None, height=dp(38))
        cb.bind(on_release=lambda x: self._confirm_clear())
        ct.add_widget(cb)

        scr.add_widget(ct)
        root.add_widget(scr)
        self._box.add_widget(root)

    def _chg_day(self, delta):
        app = App.get_running_app()
        d = date.fromisoformat(app.viewing_date) + timedelta(delta)
        app.viewing_date = d.isoformat()
        self._build()

    def _remove(self, meal, idx):
        App.get_running_app().dm.remove_entry(
            meal, idx, App.get_running_app().viewing_date)
        self._build()

    # ── Food Picker Popup ──────────────────────────────────────────────────

    def _pick_food(self, meal):
        dm = App.get_running_app().dm
        foods = dm.get_foods()
        if not foods:
            toast('No foods in database! Add some in the Foods tab.')
            return

        lay = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(10))
        search = TextInput(hint_text='🔍 Search your foods...', size_hint_y=None,
                           height=dp(38), font_size=sp(14), multiline=False,
                           background_normal='', background_color=C['card'])
        lay.add_widget(search)
        lay.add_widget(Label(text=f'Adding to {MEAL_ICON[meal]} {meal}',
                             font_size=sp(12), color=C['pri'],
                             size_hint_y=None, height=dp(20)))

        scr = ScrollView()
        flist = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4))
        flist.bind(minimum_height=flist.setter('height'))

        food_btns = []
        for name, fi in foods.items():
            fb = btn(
                f'{name}  ({int(fi["cal"])} cal / {fi["serving"]} {fi["unit"]})',
                bg=C['card'], fg=C['txt'], fs=sp(12),
                size_hint_y=None, height=dp(36))
            fb.bind(on_release=lambda x, n=name: self._set_servings(meal, n))
            flist.add_widget(fb)
            food_btns.append((fb, name, fi))

        scr.add_widget(flist)
        lay.add_widget(scr)
        cancel_b = btn('Cancel', bg=C['txt2'], size_hint_y=None, height=dp(38))
        lay.add_widget(cancel_b)

        popup = Popup(title='Select Food', content=lay, size_hint=(0.9, 0.8),
                      background='', separator_color=(0, 0, 0, 0))

        def do_search(inst, val):
            q = val.lower()
            for fb, nm, fi in food_btns:
                match = q in nm.lower()
                fb.opacity = 1 if match else 0
                fb.height = dp(36) if match else 0
                fb.disabled = not match

        search.bind(text=do_search)
        cancel_b.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    # ── Servings Popup ─────────────────────────────────────────────────────

    def _set_servings(self, meal, food_name):
        fi = App.get_running_app().dm.get_food(food_name)
        lay = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        lay.add_widget(Label(text=food_name, font_size=sp(16), bold=True, color=C['txt']))
        lay.add_widget(Label(
            text=f'{fi["cal"]} cal | {fi["protein"]}g P | '
                 f'{fi["carbs"]}g C | {fi["fat"]}g F per {fi["serving"]} {fi["unit"]}',
            font_size=sp(11), color=C['txt2']))
        lay.add_widget(Label(text='Number of servings:', font_size=sp(13), color=C['txt']))
        inp = TextInput(text='1', input_filter='float', size_hint_y=None, height=dp(40),
                        font_size=sp(16), multiline=False,
                        background_normal='', background_color=C['card'])
        lay.add_widget(inp)

        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        cancel_b = btn('Cancel', bg=C['txt2'], size_hint_x=0.4)
        add_b = btn('✅ Add', bg=C['sec'], size_hint_x=0.6)
        bb.add_widget(cancel_b)
        bb.add_widget(add_b)

        p = Popup(title=f'{MEAL_ICON[meal]} {meal}', content=lay,
                  size_hint=(0.8, 0.45), background='', separator_color=(0, 0, 0, 0))

        def add(inst):
            try:
                srv = float(inp.text or 0)
            except ValueError:
                toast('Enter a valid number!')
                return
            if srv <= 0:
                toast('Enter a positive number!')
                return
            App.get_running_app().dm.log_food(
                meal, food_name, srv, App.get_running_app().viewing_date)
            p.dismiss()
            self._build()
            toast(f'Added {food_name} to {meal}!')

        add_b.bind(on_release=add)
        cancel_b.bind(on_release=lambda x: p.dismiss())
        lay.add_widget(bb)
        p.open()

    # ── Clear Day Confirmation ─────────────────────────────────────────────

    def _confirm_clear(self):
        ct = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        ct.add_widget(Label(text='Clear all entries for this day?',
                            font_size=sp(15), color=C['txt']))
        ct.add_widget(Label(text='This cannot be undone.',
                            font_size=sp(11), color=C['txt2']))
        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        cancel_b = btn('Cancel', bg=C['txt2'], size_hint_x=0.5)
        clear_b = btn('Clear Day', bg=C['danger'], size_hint_x=0.5)
        bb.add_widget(cancel_b)
        bb.add_widget(clear_b)

        p = Popup(title='', content=ct, size_hint=(0.75, 0.3),
                  background='', separator_color=(0, 0, 0, 0))
        clear_b.bind(on_release=lambda x: (
            App.get_running_app().dm.clear_day(App.get_running_app().viewing_date),
            p.dismiss(), self._build(), toast('Day cleared!')))
        cancel_b.bind(on_release=lambda x: p.dismiss())
        ct.add_widget(bb)
        p.open()
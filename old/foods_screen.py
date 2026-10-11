"""
NutriTrack — Food database screen.
Users build their own food database with full CRUD operations.
"""

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp

from constants import C, FOOD_CATS
from widgets import Card, btn, toast


class FoodsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._box = BoxLayout()
        self.add_widget(self._box)

    def on_enter(self, *_):
        self._build()

    def _build(self):
        dm = App.get_running_app().dm
        self._box.clear_widgets()
        root = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(8))

        # ── Top bar ────────────────────────────────────────────────────────
        tb = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))
        tb.add_widget(Label(text='🍎 My Foods', font_size=sp(18), bold=True,
                            color=C['txt'], halign='left', size_hint_x=0.6))
        ab = btn('+ Add Food', bg=C['sec'], fs=sp(13), size_hint_x=0.4)
        ab.bind(on_release=lambda x: self._show_add_form())
        tb.add_widget(ab)
        root.add_widget(tb)

        # ── Search ─────────────────────────────────────────────────────────
        self._search = TextInput(
            hint_text='🔍 Search foods...', size_hint_y=None, height=dp(40),
            font_size=sp(14), multiline=False,
            background_normal='', background_color=C['card'])
        self._search.bind(text=lambda i, v: self._filter_list())
        root.add_widget(self._search)

        # ── Category filter ────────────────────────────────────────────────
        self._cat_spin = Spinner(
            text='All Categories', values=['All Categories'] + FOOD_CATS,
            size_hint_y=None, height=dp(36), font_size=sp(12),
            background_normal='', background_color=C['card'])
        self._cat_spin.bind(text=lambda i, v: self._filter_list())
        root.add_widget(self._cat_spin)

        # ── Food list ──────────────────────────────────────────────────────
        self._scroll = ScrollView()
        self._list = BoxLayout(orientation='vertical', size_hint_y=None,
                               spacing=dp(6), padding=dp(2))
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
            if q and q not in name.lower():
                continue
            if cat != 'All Categories' and fi.get('category', '') != cat:
                continue
            self._add_food_row(name, fi)

        if not self._list.children:
            self._list.add_widget(Label(
                text='No foods yet!\nTap "+ Add Food" to create your first food entry.',
                font_size=sp(14), color=C['txt2'], size_hint_y=None, height=dp(120)))

    def _add_food_row(self, name, fi):
        card = Card(orientation='vertical', padding=dp(10), spacing=dp(2),
                    size_hint_y=None, height=dp(95))

        r1 = BoxLayout(size_hint_y=0.32)
        r1.add_widget(Label(text=name, font_size=sp(14), bold=True,
                            color=C['txt'], halign='left', size_hint_x=0.55))
        r1.add_widget(Label(text=fi.get('category', ''), font_size=sp(10),
                            color=C['pri'], halign='right', size_hint_x=0.45))
        card.add_widget(r1)

        r2 = BoxLayout(size_hint_y=0.24)
        r2.add_widget(Label(text=f'{fi["serving"]} {fi["unit"]}',
                            font_size=sp(10), color=C['txt2'], halign='left'))
        card.add_widget(r2)

        r3 = BoxLayout(size_hint_y=0.22)
        for lbl, k, col in [('Cal', C['cal'], 'cal'), ('Pro', C['pro'], 'protein'),
                             ('Carb', C['carb'], 'carbs'), ('Fat', C['fat_c'], 'fat'),
                             ('Fib', C['fib'], 'fiber')]:
            r3.add_widget(Label(
                text=f'{lbl}:{fi[k]}g' if k != 'cal' else f'{fi[k]}cal',
                font_size=sp(10), color=col))
        card.add_widget(r3)

        r4 = BoxLayout(size_hint_y=0.22, spacing=dp(6))
        eb = btn('✏️ Edit', bg=C['pri'], fs=sp(11), size_hint_x=0.5)
        eb.bind(on_release=lambda x, n=name: self._show_add_form(n))
        db = btn('🗑️ Delete', bg=C['danger'], fs=sp(11), size_hint_x=0.5)
        db.bind(on_release=lambda x, n=name: self._confirm_delete(n))
        r4.add_widget(eb)
        r4.add_widget(db)
        card.add_widget(r4)
        self._list.add_widget(card)

    # ── Add / Edit Form ────────────────────────────────────────────────────

    def _show_add_form(self, edit_name=None):
        dm = App.get_running_app().dm
        fi = dm.get_food(edit_name) if edit_name else None
        title = 'Edit Food' if edit_name else 'Add New Food'

        lay = BoxLayout(orientation='vertical', spacing=dp(6), padding=dp(16),
                        size_hint_y=None)
        lay.bind(minimum_height=lay.setter('height'))

        fields = {}
        for lbl, key, default, hint in [
            ('Food Name',   'name',     edit_name or '',                          'e.g. Chicken Breast'),
            ('Category',    'category', fi.get('category', 'Other') if fi else 'Other', ''),
            ('Serving Size','serving',  str(fi.get('serving', 1)) if fi else '1',       'number'),
            ('Serving Unit','unit',     fi.get('unit', 'serving') if fi else 'serving',  'e.g. cup, oz, piece'),
            ('Calories',    'cal',      str(fi.get('cal', 0)) if fi else '0',            'kcal per serving'),
            ('Protein (g)', 'protein',  str(fi.get('protein', 0)) if fi else '0',        'grams'),
            ('Carbs (g)',   'carbs',    str(fi.get('carbs', 0)) if fi else '0',          'grams'),
            ('Fat (g)',     'fat',      str(fi.get('fat', 0)) if fi else '0',            'grams'),
            ('Fiber (g)',   'fiber',    str(fi.get('fiber', 0)) if fi else '0',          'grams'),
        ]:
            lay.add_widget(Label(text=lbl, font_size=sp(12), color=C['txt'],
                                 halign='left', size_hint_y=None, height=dp(20)))
            if key == 'category':
                sp = Spinner(text=default, values=FOOD_CATS, size_hint_y=None,
                             height=dp(36), font_size=sp(13),
                             background_normal='', background_color=C['card'])
                lay.add_widget(sp)
                fields[key] = sp
            else:
                inp = TextInput(text=default, hint_text=hint, size_hint_y=None,
                                height=dp(36), font_size=sp(13), multiline=False,
                                input_filter='float' if key not in ('name', 'unit') else None,
                                background_normal='', background_color=C['card'])
                lay.add_widget(inp)
                fields[key] = inp

        sv = ScrollView(size_hint_y=1)
        sv.add_widget(lay)

        def save(inst):
            nm = fields['name'].text.strip()
            if not nm:
                toast('Food name is required!')
                return
            try:
                vals = {k: float(fields[k].text or 0)
                        for k in ('cal', 'protein', 'carbs', 'fat', 'fiber', 'serving')}
                vals['serving'] = max(vals['serving'], 0.01)
            except ValueError:
                toast('Please enter valid numbers!')
                return

            if edit_name:
                dm.update_food(edit_name, nm, fields['category'].text,
                               vals['cal'], vals['protein'], vals['carbs'],
                               vals['fat'], vals['fiber'], vals['serving'],
                               fields['unit'].text.strip() or 'serving')
            else:
                dm.add_food(nm, fields['category'].text,
                            vals['cal'], vals['protein'], vals['carbs'],
                            vals['fat'], vals['fiber'], vals['serving'],
                            fields['unit'].text.strip() or 'serving')
            popup.dismiss()
            self._build()
            toast(f'{nm} saved!')

        btns = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        cancel_b = btn('Cancel', bg=C['txt2'], size_hint_x=0.4)
        save_b = btn('💾 Save', bg=C['sec'], size_hint_x=0.6)
        cancel_b.bind(on_release=lambda x: popup.dismiss())
        save_b.bind(on_release=save)
        btns.add_widget(cancel_b)
        btns.add_widget(save_b)

        content = BoxLayout(orientation='vertical', spacing=dp(4))
        content.add_widget(Label(text=title, font_size=sp(16), bold=True,
                                 color=C['pri'], size_hint_y=None, height=dp(32)))
        content.add_widget(sv)
        content.add_widget(btns)

        popup = Popup(title='', content=content, size_hint=(0.92, 0.88),
                      background='', separator_color=(0, 0, 0, 0))
        with popup.canvas.before:
            Color(*C['card'])
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(14)])
        popup.open()

    # ── Delete Confirmation ────────────────────────────────────────────────

    def _confirm_delete(self, name):
        ct = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(12))
        ct.add_widget(Label(text=f'Delete "{name}"?', font_size=sp(15), color=C['txt']))
        ct.add_widget(Label(
            text='This will also remove it from any future logging. Past diary entries are kept.',
            font_size=sp(11), color=C['txt2']))
        bb = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        cancel_b = btn('Cancel', bg=C['txt2'], size_hint_x=0.5)
        del_b = btn('Delete', bg=C['danger'], size_hint_x=0.5)
        bb.add_widget(cancel_b)
        bb.add_widget(del_b)

        p = Popup(title='', content=ct, size_hint=(0.75, 0.3),
                  background='', separator_color=(0, 0, 0, 0))
        del_b.bind(on_release=lambda x: (
            App.get_running_app().dm.delete_food(name), p.dismiss(),
            self._build(), toast('Deleted!')))
        cancel_b.bind(on_release=lambda x: p.dismiss())
        ct.add_widget(bb)
        p.open()
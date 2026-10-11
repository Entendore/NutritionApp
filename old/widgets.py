"""
NutriTrack — Reusable custom widgets and helper functions.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock

from constants import C


# ── Card Container ──────────────────────────────────────────────────────────

class Card(BoxLayout):
    def __init__(self, bg=C['card'], radius=dp(10), **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*bg)
            self._r = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=lambda i, v: setattr(self._r, 'pos', v),
                  size=lambda i, v: setattr(self._r, 'size', v))


# ── Progress Bar ────────────────────────────────────────────────────────────

class PBar(FloatLayout):
    progress = NumericProperty(0)
    max_val  = NumericProperty(100)
    bar_col  = ListProperty([0.3, 0.7, 0.3, 1])

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint_y = None
        self.height = dp(10)
        self.bind(size=self._draw, pos=self._draw,
                  progress=self._draw, max_val=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*C['div'])
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(5)])
            if self.max_val > 0:
                fw = max(self.width * min(self.progress / self.max_val, 1.0), 0)
                if fw > 0:
                    Color(*self.bar_col)
                    RoundedRectangle(pos=self.pos, size=(fw, self.height),
                                     radius=[dp(5)])


# ── Macro Nutrient Row ─────────────────────────────────────────────────────

class MacroRow(BoxLayout):
    def __init__(self, label, consumed, goal, color, **kw):
        super().__init__(**kw)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(30)
        self.padding = [dp(4), dp(1)]
        self.spacing = dp(6)

        lbl = Label(text=label, font_size=sp(12), bold=True, color=C['txt'],
                    size_hint_x=0.18, halign='right')
        lbl.bind(size=lbl.setter('text_size'))
        self.add_widget(lbl)

        self.add_widget(PBar(progress=consumed, max_val=max(goal, 1),
                             bar_col=color, size_hint_x=0.48))

        val = Label(text=f'{int(consumed)}/{int(goal)}g', font_size=sp(11),
                    color=C['txt2'], size_hint_x=0.34, halign='left')
        val.bind(size=val.setter('text_size'))
        self.add_widget(val)


# ── Helper: Styled Button ──────────────────────────────────────────────────

def btn(text, bg=C['pri'], fg=C['white'], fs=sp(14), **kw):
    return Button(text=text, font_size=fs, color=fg,
                  background_normal='', background_color=bg, **kw)


# ── Helper: Toast Notification ─────────────────────────────────────────────

def toast(msg):
    ct = BoxLayout(orientation='vertical', padding=dp(16))
    ct.add_widget(Label(text=msg, font_size=sp(14), color=C['txt']))
    p = Popup(title='', content=ct, size_hint=(0.7, 0.22),
              background='', separator_color=(0, 0, 0, 0))
    with p.canvas.before:
        Color(*C['card'])
        RoundedRectangle(pos=p.pos, size=p.size, radius=[dp(12)])
    p.open()
    Clock.schedule_once(lambda dt: p.dismiss(), 1.8)
#!/usr/bin/env python3
"""
NutriTrack — Local Nutrition Tracker
  • No APIs, No AI, All data in local JSON
  • Users build their own food database
  • Built-in nutrition education library
  • BMI & TDEE calculators

Usage:
    python app.py
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color          # ← THIS WAS MISSING

from constants import C
from data_manager import DataManager
from home_screen import HomeScreen
from foods_screen import FoodsScreen
from diary_screen import DiaryScreen
from education_screen import EducationScreen
from goals_screen import GoalsScreen, HistoryScreen
from widgets import btn


# ═══════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════

class NutriTrackApp(App):
    def build(self):
        self.dm = DataManager()
        self.viewing_date = self.dm.today_key()

        self.sm = ScreenManager()

        # Register screens
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(FoodsScreen(name='foods'))
        self.sm.add_widget(DiaryScreen(name='diary'))
        self.sm.add_widget(EducationScreen(name='education'))
        self.sm.add_widget(GoalsScreen(name='goals'))
        self.sm.add_widget(HistoryScreen(name='history'))

        # Root layout: screen + nav bar
        root = BoxLayout(orientation='vertical')

        # Screen area
        root.add_widget(self.sm)

        # Navigation bar
        navbar = BoxLayout(size_hint_y=None, height=dp(54), spacing=dp(2),
                           padding=[dp(2), dp(2), dp(2), dp(2)])
        with navbar.canvas.before:
            Color(*C['card'])

        nav_items = [
            ('🏠', 'Home',       'home'),
            ('📔', 'Diary',      'diary'),
            ('🍎', 'Foods',      'foods'),
            ('📚', 'Learn',      'education'),
            ('🎯', 'Goals',      'goals'),
            ('📊', 'History',    'history'),
        ]
        for icon, label, screen_name in nav_items:
            nb = btn(f'{icon}\n{label}', bg=C['pri'], fg=C['white'],
                     fs=sp(9), size_hint_x=1)
            nb.bind(on_release=lambda x, s=screen_name: self._nav(s))
            navbar.add_widget(nb)

        root.add_widget(navbar)
        return root

    def _nav(self, screen_name):
        self.sm.current = screen_name


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    NutriTrackApp().run()
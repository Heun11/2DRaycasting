import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
import random

from classes import Boundry, Player

class GameWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        Clock.schedule_interval(self.update,1/60)

        self.player = Player()
        self.walls = [Boundry(a=[500,200], b=[500,400]), Boundry(a=[600,200], b=[600,400])]

    def update(self,dt):
        # print(1/dt)
        self.canvas.clear()
        with self.canvas:
            for wall in self.walls:
                wall.show()
            
            self.player.cast(self.walls)
            self.player.update()

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.player.look(touch.pos)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.player.keys_down(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        self.player.keys_up(keycode[1])


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
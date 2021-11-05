import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Ellipse
from kivy.clock import Clock
import random

from classes import Boundry, Ray

class GameWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update,1/60)

        self.ray = Ray(pos=[300, 300], dir_=[1,0])
        self.walls = [Boundry(a=[500,200], b=[500,400]), Boundry(a=[400,200], b=[500,400])]

    def update(self,dt):
        # print(1/dt)
        self.canvas.clear()
        with self.canvas:
            self.ray.show()
            for wall in self.walls:
                wall.show()

            for wall in self.walls:
                pt = self.ray.cast(wall)
                if pt:
                    Ellipse(pos=pt, size=[10,10])

    def on_touch_down(self, touch):
        super().on_touch_down(touch)

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.ray.set_dir(touch.pos)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()
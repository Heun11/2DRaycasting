import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
import random, math

Window.size = [1024*1.5, 512*1.5]
PI = 3.14159265359

class Player:
    def __init__(self):
        self.pos = [100,100]
        self.size = [10,10]
        self.angle = 2*PI

        self.dx=math.cos(self.angle)*5
        self.dy=math.sin(self.angle)*5

        self.dir = {
            "w":False,
            "s":False,
            "a":False,
            "d":False,
        }
    
    def update(self):
        if self.dir["a"]:
            self.angle+=0.1
            if self.angle>2*PI:
                self.angle-=2*PI
            self.dx=math.cos(self.angle)*5
            self.dy=math.sin(self.angle)*5

        if self.dir["d"]:
            self.angle-=0.1
            if self.angle<0:
                self.angle+=2*PI
            self.dx=math.cos(self.angle)*5
            self.dy=math.sin(self.angle)*5

        if self.dir["s"]:
            self.pos[0]-=self.dx
            self.pos[1]-=self.dy 
            
        if self.dir["w"]:
            self.pos[0]+=self.dx
            self.pos[1]+=self.dy

        Line(points=[self.pos[0], self.pos[1], self.pos[0]+self.dx*5, self.pos[1]+self.dy*5], width=0.5)
        Rectangle(pos=[self.pos[0], self.pos[1]], size=self.size)

    def keys_down(self, key):
        if key == "w" or key == "up":
            self.dir["w"] = True
        if key == "s" or key == "down":
            self.dir["s"] = True

        if key == "a" or key == "left":
            self.dir["a"] = True
        if key == "d" or key == "right":
            self.dir["d"] = True

    def keys_up(self, key):
        if key == "w" or key == "up":
            self.dir["w"] = False
        if key == "s" or key == "down":
            self.dir["s"] = False

        if key == "a" or key == "left":
            self.dir["a"] = False
        if key == "d" or key == "right":
            self.dir["d"] = False


class GameWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        Clock.schedule_interval(self.update,1/60)

        self.player = Player()
        

    def update(self,dt):
        self.canvas.clear()
        with self.canvas:
            self.player.update()

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
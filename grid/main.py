from os import WIFCONTINUED
from types import CellType
import kivy
from kivy.app import App
from kivy.core import window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
import math

Window.size = [1280, 640]
CELL_SIZE = 64
# Window.size = [1024*1.5, 512*1.5]
# CELL_SIZE = 51.2*1.5
PI = 3.14159265359
MAP = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]
MAP.reverse()

class Player:
    def __init__(self):
        self.pos = [96,224]
        self.size = [10,10]
        self.angle = math.radians(60)
        self.rays = 1

        self.dx=math.cos(self.angle)*5
        self.dy=math.sin(self.angle)*5

        self.dir = {
            "w":False,
            "s":False,
            "a":False,
            "d":False,
        }

    def castRays(self):
        rayA = math.degrees(self.angle)+0.0001
        for i in range(self.rays):
            ptX = 0
            ptY = 0

            Ya = 0
            Xa = 0

            # Horizontal
            # if rayA<180 and rayA>0: # up
            #     ptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE+CELL_SIZE
            #     ptX = self.pos[0]+(self.pos[1]-ptY)/math.tan(math.radians(rayA))
            #     Ya=CELL_SIZE
            #     Xa=(CELL_SIZE/math.tan(math.radians(rayA)))

            # else: # down
            #     ptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE-1
            #     ptX = self.pos[0]+(self.pos[1]-ptY)/math.tan(math.radians(rayA))
            #     Ya=-CELL_SIZE
            #     Xa=-(CELL_SIZE/math.tan(math.radians(rayA)))


            #####################################################
            # https://permadi.com/1996/05/ray-casting-tutorial-7/
            #####################################################


            if rayA<180 and rayA>0: # up
                ptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE+CELL_SIZE
                ptX = self.pos[0]+(self.pos[1]-ptY)/math.tan(math.radians(rayA))

            else: # down
                ptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE-1
                ptX = self.pos[0]+(self.pos[1]-ptY)/math.tan(math.radians(rayA))

            Rectangle(pos=[ptX, ptY], size=[5,5])
            Line(points=[self.pos[0], self.pos[1], ptX, ptY], width=0.5)

            # Vertical
            if rayA>90 and rayA<270: # left
                ptX = math.floor(self.pos[0]/CELL_SIZE)*CELL_SIZE-1
                ptY = self.pos[1]+(self.pos[0]-ptX)*math.tan(math.radians(rayA))

            else: # right
                pass

            Rectangle(pos=[ptX, ptY], size=[5,5])

            # Line(points=[self.pos[0], self.pos[1], rayX, rayY], width=0.5)

    def update(self):
        if self.dir["a"]:
            self.angle+=0.07
            if self.angle>2*PI:
                self.angle-=2*PI
            self.dx=math.cos(self.angle)*5
            self.dy=math.sin(self.angle)*5

        if self.dir["d"]:
            self.angle-=0.07
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

        Color(0,1,0,1)

        self.castRays()
        Line(points=[self.pos[0], self.pos[1], self.pos[0]+self.dx*8, self.pos[1]+self.dy*8], width=0.5)
        Rectangle(pos=[self.pos[0], self.pos[1]], size=self.size)

        Color(1,1,1,1)

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
        # print(1/dt)
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1,0.3)
            Rectangle(size=Window.size)
            Color(1,1,1,1)

            for i in range(10):
                for j in range(10):
                    if MAP[i][j]==0:
                        Color(0.2,0.2,0.2,1)
                    elif MAP[i][j]==1:
                        Color(1,1,1,0.5)
                    Rectangle(pos=[CELL_SIZE*j, CELL_SIZE*i], size=[CELL_SIZE-1, CELL_SIZE-1])
                    Color(1,1,1,1)

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

class RayCastingApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    RayCastingApp().run()
from logging import disable
import kivy
from kivy.app import App
from kivy.core import window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
import math

CELL_SIZE = 64
Window.size = [CELL_SIZE*20, CELL_SIZE*10]
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
    [1,0,0,0,0,1,2,0,2,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]
MAP.reverse()

class Player:
    def __init__(self):
        self.pos = [96,224]
        self.size = [10,10]
        self.multSize = 2
        self.angle = math.radians(60)
        self.rays = 60
        self.fov = 60
        self.rayAdistance = self.fov/self.rays
        self.rayOffset = Window.size[0]*0.5

        self.dx=math.cos(self.angle)*5
        self.dy=math.sin(self.angle)*5

        self.dir = {
            "w":False,
            "s":False,
            "a":False,
            "d":False,
        }

    def castRays(self):
        rayA = math.degrees(self.angle)+0.0001-self.fov/2
        rayB = self.fov/2
        for i in range(self.rays):
            HptX = 0
            HptY = 0

            HYa = 0
            HXa = 0

            VptX = 0
            VptY = 0

            VYa = 0
            VXa = 0

            # Horizontal
            if rayA<180 and rayA>0: # up
                HptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE+CELL_SIZE
                HptX = self.pos[0]-(self.pos[1]-HptY)/math.tan(math.radians(rayA))
                HYa = CELL_SIZE
                HXa = CELL_SIZE/math.tan(math.radians(rayA))

            else: # down
                HptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE-1
                HptX = self.pos[0]-(self.pos[1]-HptY)/math.tan(math.radians(rayA))
                HYa = -CELL_SIZE
                HXa = -(CELL_SIZE/math.tan(math.radians(rayA)))

            try:
                wall = MAP[int(HptY/CELL_SIZE)][int(HptX/CELL_SIZE)]
                while wall == 0:
                    HptY+=HYa
                    HptX+=HXa
                    wall = MAP[int(HptY/CELL_SIZE)][int(HptX/CELL_SIZE)]

                a = abs(self.pos[0]-HptX)
                b = abs(self.pos[1]-HptY)
                Hdistance = math.sqrt(a**2+b**2)
            except:
                Hdistance = math.inf

            # Vertical
            if rayA>90 and rayA<270: # left
                VptX = math.floor(self.pos[0]/CELL_SIZE)*CELL_SIZE-1
                VptY = self.pos[1]-(self.pos[0]-VptX)*math.tan(math.radians(rayA))
                VXa = -CELL_SIZE
                VYa = -CELL_SIZE*math.tan(math.radians(rayA))

            else: # right
                VptX = math.floor(self.pos[0]/CELL_SIZE)*CELL_SIZE+CELL_SIZE
                VptY = self.pos[1]-(self.pos[0]-VptX)*math.tan(math.radians(rayA))
                VXa = CELL_SIZE
                VYa = CELL_SIZE*math.tan(math.radians(rayA))

            try:
                wall = MAP[int(VptY/CELL_SIZE)][int(VptX/CELL_SIZE)]
                while wall == 0:
                    VptY+=VYa
                    VptX+=VXa
                    wall = MAP[int(VptY/CELL_SIZE)][int(VptX/CELL_SIZE)]

                a = abs(self.pos[0]-VptX)
                b = abs(self.pos[1]-VptY)
                Vdistance = math.sqrt(a**2+b**2)
            except:
                Vdistance = math.inf

            if Vdistance<Hdistance: # V
                ptPos = [VptX, VptY]
                distance = Vdistance*math.cos(math.radians(rayB))
                wall = MAP[int(VptY/CELL_SIZE)][int(VptX/CELL_SIZE)]
            else: # H
                ptPos = [HptX, HptY]
                distance = Hdistance*math.cos(math.radians(rayB))
                wall = MAP[int(HptY/CELL_SIZE)][int(HptX/CELL_SIZE)]

            Line(points=[self.pos[0], self.pos[1], ptPos[0], ptPos[1]], width=0.5)

            size = [(Window.size[0]*0.5)/self.rays, CELL_SIZE/distance*200]
            pos = [self.rayOffset+(size[0]*i), Window.size[1]*0.5-size[1]*0.5]
            if wall==1:
                Color(1,0,0,1)
            elif wall==2:
                Color(0,1,0,1)
            Rectangle(size=size, pos=pos)
            Color(1,1,1,1)

            rayB-=self.rayAdistance
            rayA+=self.rayAdistance
            if rayA>360:
                rayA-=360

    def update(self):
        if self.dir["d"]:
            self.angle+=0.07
            if self.angle>2*PI:
                self.angle-=2*PI
            self.dx=math.cos(self.angle)*self.multSize
            self.dy=math.sin(self.angle)*self.multSize

        if self.dir["a"]:
            self.angle-=0.07
            if self.angle<0:
                self.angle+=2*PI
            self.dx=math.cos(self.angle)*self.multSize
            self.dy=math.sin(self.angle)*self.multSize

        if self.dir["s"]:
            self.pos[0]-=self.dx
            self.pos[1]-=self.dy 
            
        if self.dir["w"]:
            self.pos[0]+=self.dx
            self.pos[1]+=self.dy

        self.castRays()
        Rectangle(pos=[self.pos[0], self.pos[1]], size=self.size)
        Color(0,0,1,1)
        Line(points=[self.pos[0], self.pos[1], self.pos[0]+self.dx*5, self.pos[1]+self.dy*5], width=1.5)
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
            # Background
            Color(0.3,0.3,0.3,1)
            Rectangle(size=[Window.size[0]/2, Window.size[1]])
            Color(0.4,0.5,0.7,1)
            Rectangle(size=[Window.size[0]/2, Window.size[1]/2], pos=[Window.size[0]/2,Window.size[1]/2]) # sky
            Color(0.15,0.1,0.1,1)
            Rectangle(size=[Window.size[0]/2, Window.size[1]/2], pos=[Window.size[0]/2,0]) # ground

            for i in range(10):
                for j in range(10):
                    if MAP[i][j]==0:
                        Color(0.2,0.2,0.2,1)
                    elif MAP[i][j]==1:
                        Color(1,0,0,1)
                    elif MAP[i][j]==2:
                        Color(0,1,0,1)
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
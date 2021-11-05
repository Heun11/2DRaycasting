from kivy.graphics import Line, Rectangle
import math

##########################################################################################
# https://ncase.me/sight-and-light/
##########################################################################################
# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
##########################################################################################
# https://www.youtube.com/watch?v=TOEi6T2mtHo&t=0s
##########################################################################################

def normalize(v):
    mag=math.sqrt((v[0]**2)+(v[1]**2))
    return [v[0]/mag,v[1]/mag]

class Ray:
    def __init__(self, pos, dir_):
        self.pos = pos
        self.dir = dir_
    
    def show(self):
        Rectangle(pos=[self.pos[0], self.pos[1]], size=[10,10])
        # Line(points=[self.pos[0]+self.dir[0]*1000, self.pos[1]+self.dir[1]*1000, self.pos[0], self.pos[1]], width=0.5)
        Line(points=[self.pos[0]+self.dir[0]*100, self.pos[1]+self.dir[1]*100, self.pos[0], self.pos[1]], width=0.5)

    def set_dir(self, dir_):
        self.dir=[dir_[0]-self.pos[0], dir_[1]-self.pos[1]]
        self.dir=normalize(self.dir)

    def cast(self, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if den==0:
            return 
        
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/den

        if t>0 and t<1 and u>0:
            point = [(x1+t*(x2-x1)), (y1+t*(y2-y1))]
            return point
        else:
            return 

class Particle:
    def __init__(self):
        self.pos = [300,300]
        self.rays = []

class Boundry:
    def __init__(self, a=[0,0], b=[100,100]):
        self.a = a
        self.b = b

    def show(self):
        Line(points=[self.a[0], self.a[1], self.b[0], self.b[1]], width=1)
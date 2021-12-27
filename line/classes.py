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
    if mag!=0:
        return [v[0]/mag,v[1]/mag]
    return [0,0]

def find_lowest_size_between_points(pos, pts):
    sizes = []
    for pt in pts:
        sizes.append(math.sqrt(((pos[0]-pt[0])**2)+((pos[1]-pt[1])**2)))
    return pts[sizes.index(min(sizes))]

class Ray:
    def __init__(self, pos, dir_):
        self.pos = pos
        self.dir = dir_

    def show(self, pt):
        Line(points=[pt[0], pt[1], self.pos[0], self.pos[1]], width=0.5)
        Rectangle(pos=pt, size=[5,5])

    def set_dir(self, dir_):
        self.dir=[dir_[0]-self.pos[0], dir_[1]-self.pos[1]]
        self.dir=normalize(self.dir)
        # self.dir=dir_

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

class Player:
    def __init__(self):
        self.pos = [300,300]
        self.rays = [Ray(self.pos, [0,0])]

        self.dir = {
            "up":False,
            "down":False,
            "right":False,
            "left":False
        }

        self.look_dir = {
            "right":False,
            "left":False
        }

        self.vel = 3

    def update(self):
        x_v = 0
        y_v = 0

        if self.dir["up"]:
            y_v = self.vel

        if self.dir["down"]:
            y_v = -self.vel

        if self.dir["right"]:
            x_v = self.vel

        if self.dir["left"]:
            x_v = -self.vel

        self.pos[0]+=x_v
        self.pos[1]+=y_v

        Rectangle(pos=[self.pos[0], self.pos[1]], size=[10,10])

    def cast(self, walls):
        for ray in self.rays:
            pts = []
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    pts.append(pt)
            if len(pts)>0:
                ray.show(find_lowest_size_between_points(self.pos, pts))

    def look(self, pos):
        self.rays[0].set_dir(pos)

    def keys_down(self, key):
        if key == "w" or key == "up":
            self.dir["up"] = True
        if key == "s" or key == "down":
            self.dir["down"] = True
        if key == "a" or key == "left":
            self.dir["left"] = True
        if key == "d" or key == "right":
            self.dir["right"] = True

        if key == "e":
            self.look_dir["right"] = True
        if key == "q":
            self.look_dir["left"] = True

    def keys_up(self, key):
        if key == "w" or key == "up":
            self.dir["up"] = False
        if key == "s" or key == "down":
            self.dir["down"] = False
        if key == "a" or key == "left":
            self.dir["left"] = False
        if key == "d" or key == "right":
            self.dir["right"] = False

        if key == "e":
            self.look_dir["right"] = False
        if key == "q":
            self.look_dir["left"] = False

class Boundry:
    def __init__(self, a=[0,0], b=[100,100]):
        self.a = a
        self.b = b

    def show(self):
        Line(points=[self.a[0], self.a[1], self.b[0], self.b[1]], width=1)
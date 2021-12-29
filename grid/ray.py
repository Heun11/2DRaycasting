import pygame as p
import math

WindowSize = [1280, 640]
CELL_SIZE = 64
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

p.init()
screen = p.display.set_mode(WindowSize)
p.display.set_caption("Raycasting")
clock = p.time.Clock()

class Player:
    def __init__(self):
        self.pos = [300,300]
        self.size = [10,10]
        self.angle = 2*PI
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
        rayA = math.degrees(self.angle)
        for i in range(self.rays):
            ptX = 0
            ptY = 0

            Ya = 0
            Xa = 0

            # Horizontal
            if rayA<180 and rayA>0: # down
                print("down")

            else: # up
                ptY = math.floor(self.pos[1]/CELL_SIZE)*CELL_SIZE-1
                ptX = self.pos[0]+(self.pos[1]-ptY)/math.tan(math.radians(rayA))


            p.draw.rect(screen, (255,0,0), p.Rect([ptX, ptY], [5,5]))


    def update(self):
        if self.dir["d"]:
            self.angle+=0.07
            if self.angle>2*PI:
                self.angle-=2*PI
            self.dx=math.cos(self.angle)*5
            self.dy=math.sin(self.angle)*5

        if self.dir["a"]:
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

        self.castRays()

        p.draw.rect(screen, (0,255,0), p.Rect(self.pos, self.size))
        p.draw.line(screen, (255,255,0), self.pos, [self.pos[0]+self.dx*5, self.pos[1]+self.dy*5])

    def keys_down(self, key):
        if key == p.K_w:
            self.dir["w"] = True
        if key == p.K_s:
            self.dir["s"] = True
        if key == p.K_a:
            self.dir["a"] = True
        if key == p.K_d:
            self.dir["d"] = True

    def keys_up(self, key):
        if key == p.K_w:
            self.dir["w"] = False
        if key == p.K_s:
            self.dir["s"] = False
        if key == p.K_a:
            self.dir["a"] = False
        if key == p.K_d:
            self.dir["d"] = False

player = Player()

run = True
while run:
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                run = False

            player.keys_down(event.key)

        if event.type == p.KEYUP:
            player.keys_up(event.key)

    screen.fill((0,0,0))

    for i in range(10):
        for j in range(10):
            color = [80,80,80]
            if MAP[i][j]==1:
                color = [150,150,150]

            p.draw.rect(screen, color, p.Rect([j*CELL_SIZE, i*CELL_SIZE], [CELL_SIZE-1,CELL_SIZE-1]))    

    player.update()

    p.display.update()
    clock.tick(60)

p.quit()

from ggame import App, Sprite, Color, LineStyle, RectangleAsset, CircleAsset
from math import atan, sqrt, sin, cos, pi

black = Color(0x000000, 1.0)
blue = Color(0x0000ff, 1.0)

noline = LineStyle(0.0, black)

class Ball(Sprite):
    
    r = 30
    asset = CircleAsset(r, noline, blue)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.fxcenter = self.fycenter = 0.5
        self.velocity = (0,0)
        self.speed = 2
        Collisions.listenKeyEvent('keydown', 'left arrow', self.left)
        Collisions.listenKeyEvent('keyup', 'left arrow', self.right)
        Collisions.listenKeyEvent('keydown', 'right arrow', self.right)
        Collisions.listenKeyEvent('keyup', 'right arrow', self.left)
        Collisions.listenKeyEvent('keydown', 'up arrow', self.up)
        Collisions.listenKeyEvent('keyup', 'up arrow', self.down)
        Collisions.listenKeyEvent('keydown', 'down arrow', self.down)
        Collisions.listenKeyEvent('keyup', 'down arrow', self.up)
        #circle = Collisions.getSpritesbyClass(Circle)[0]
        #angle = atan((circle.y-self.y)/(self.x-circle.x))
        #if self.x < circle.x:
        #    angle += pi
        #print(angle)
        
    def left(self, event):
        if self.velocity[0] > -self.speed:
            self.velocity[0] -= self.speed
        
    def right(self, event):
        if self.velocity[0] < self.speed:
            self.velocity[0] += self.speed
            
    def up(self, event):
        if self.velocity[1] > -self.speed:
            self.velocity[1] -= self.speed
            
    def down(self, event):
        if self.velocity[1] < self.speed:
            self.velocity[1] += self.speed
        
    def step(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        rectangle = Collisions.getSpritesbyClass(Rectangle)[0]
        if rectangle.x-self.x == 30:
            print((rectangle.y-self.y)/(rectangle.x-self.x))
            print(self.x,self.y)
        circle = Collisions.getSpritesbyClass(Circle)[0]
        if sqrt((self.x-circle.x)**2+(self.y-circle.y)**2) <= 60:
            if self.x == circle.x:
                if self.y > circle.y:
                    angle = pi/2
                else:
                    angle = 3*pi/2
            else:
                angle = atan((circle.y-self.y)/(self.x-circle.x))
            if self.x < circle.x:
                angle += pi
            print(angle)
            #dist = 60-sqrt((self.x-circle.x)**2+(self.y-circle.y)**2)
            #self.x += dist*cos(angle)
            #self.y += dist*sin(angle)
            self.x = 60*cos(angle)+circle.x
            self.y = 60*sin(angle)+circle.x
        
class Rectangle(Sprite):
    
    asset = RectangleAsset(100, 200, noline, black)
    
    def __init__(self, position):
        super().__init__(Rectangle.asset, position)
        
class Circle(Sprite):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Circle.asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class Collisions(App):
    
    def __init__(self):
        super().__init__()
        Rectangle((750,200))
        Ball((500,300))
        Circle((250,300))
        #Ball((190,240))
        
    def step(self):
        self.getSpritesbyClass(Ball)[0].step()
        
Collisions().run()
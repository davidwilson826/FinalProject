from ggame import App, Sprite, Color, LineStyle, RectangleAsset, CircleAsset
from math import atan

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
        Rectangle = Collisions.getSpritesbyClass(Rectangle)[0]
        if atan((Rectangle.x-self.x)/(Rectangle.y-self.y)) == 30:
            print('hello')
        
class Rectangle(Sprite):
    
    asset = RectangleAsset(100, 200, noline, black)
    
    def __init__(self, position):
        super().__init__(Rectangle.asset, position)
        
class Collisions(App):
    
    def __init__(self):
        super().__init__()
        Ball((500,300))
        Rectangle((750,200))
        
    def step(self):
        self.getSpritesbyClass(Ball)[0].step()
        
Collisions().run()
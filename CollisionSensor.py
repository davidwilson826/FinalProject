from ggame import App, Sprite, Color, LineStyle, RectangleAsset, CircleAsset

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
        Collisions.listenKeyEvent('keydown', 'left arrow', self.left)
        Collisions.listenKeyEvent('keydown', 'right arrow', self.right)
        Collisions.listenKeyEvent('keydown', 'right arrow', self.right)
        Collisions.listenKeyEvent('keydown', 'right arrow', self.left)
        
    def left(self, event):
        self.velocity[0] -= 5
        
    def right(self, event):
        self.velocity[0] += 5
        
    def step(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
class Collisions(App):
    
    def __init__(self):
        super().__init__()
        Ball((200,200))
        
    def step(self):
        self.getSpritesbyClass(Ball)[0].step()
        
Collisions().run()
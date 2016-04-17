from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noline = LineStyle(0.0, black)

GRAVITY = 0.5

Floor = RectangleAsset(SCREEN_WIDTH, 10, noline, black)

class Ball(Sprite):

    asset = CircleAsset(30, noline, black)
  
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.velocity = (0,0)
        self.mag = 1
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        
    def right(self, event):
        self.velocity[0] += self.mag
        
    def left(self, event):
        self.velocity[0] -= self.mag
        
    def step(self):
        if self.y >= SCREEN_HEIGHT-35:
            self.velocity[1] *= -1
            self.velocity[1] -= GRAVITY
        self.velocity[1] += GRAVITY
        print(self.velocity)
        self.x += self.velocity[0]
        self.y += self.velocity[1]

class HeadSoccer(App):

    def __init__(self):
        super().__init__()
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        Sprite(Floor,(0,SCREEN_HEIGHT))
        
    def step(self):
        for x in self.getSpritesbyClass(Ball):
            x.step()
    
HeadSoccer().run()


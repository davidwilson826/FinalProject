from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noline = LineStyle(0.0, black)

GRAVITY = 0.5

Floor = RectangleAsset(SCREEN_WIDTH, 10, noline, black)

class PhysicsObject(Sprite):
  
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.velocity = [0,0]
        
    def step(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
class Player(PhysicsObject):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Player.asset, position)
        self.mag = 1
        self.speed = 5
        self.jumpForce = 15
        self.mass = 5
        HeadSoccer.listenKeyEvent('keydown', 'd', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'a', self.left)
        HeadSoccer.listenKeyEvent('keyup', 'd', self.stop)
        HeadSoccer.listenKeyEvent('keyup', 'a', self.stop)
        HeadSoccer.listenKeyEvent('keydown', 'w', self.jump)
        
    def right(self, event):
        self.velocity[0] = self.speed
        
    def left(self, event):
        self.velocity[0] = -self.speed
        
    def stop(self, event):
        self.velocity[0] = 0
        
    def jump(self, event):
        if self.y == SCREEN_HEIGHT:
            self.velocity[1] = -self.jumpForce
            
    def step(self):
        super().step()
        if self.y < SCREEN_HEIGHT:
            self.velocity[1] += GRAVITY
        elif self.y == SCREEN_HEIGHT:
            self.velocity[1] = 0
        
class Ball(PhysicsObject):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.mag = 1
        self.mass = 2
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        
    def right(self, event):
        self.velocity[0] += self.mag
        
    def left(self, event):
        self.velocity[0] -= self.mag
        
    def step(self):
        super().step()
        if self.y >= SCREEN_HEIGHT-30:
            self.velocity[1] *= -1
            self.velocity[1] -= GRAVITY
        self.velocity[1] += GRAVITY
        if len(self.collidingWithSprites(Player)) > 0:
            for x in self.collidingWithSprites(Player):
                self.velocity[0] += x.mass*x.velocity[0]/self.mass
                self.velocity[1] += x.mass*x.velocity[1]/self.mass

class HeadSoccer(App):

    def __init__(self):
        super().__init__()
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        Sprite(Floor,(0,SCREEN_HEIGHT))
        Player((SCREEN_WIDTH/2,SCREEN_HEIGHT))
        
    def classStep(self, sclass):
        for x in self.getSpritesbyClass(sclass):
            x.step()
        
    def step(self):
        self.classStep(Ball)
        self.classStep(Player)
    
HeadSoccer().run()
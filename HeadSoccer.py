from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset
from time import sleep, time

start = time()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)

noline = LineStyle(0.0, black)

GRAVITY = 0.5

Floor = RectangleAsset(SCREEN_WIDTH, 10, noline, black)

class Goal(Sprite):
    
    asset = RectangleAsset(50, 200, noline, black)
    
    def __init__(self, position):
        super().__init__(Goal.asset, position)
        self.ident = len(HeadSoccer.getSpritesbyClass(Goal))

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
        print(self.y)
        if self.y < SCREEN_HEIGHT:
            self.velocity[1] += GRAVITY
        elif self.y == SCREEN_HEIGHT:
            self.velocity[1] = 0
            
class PlayerCover(Sprite):
    
    asset = RectangleAsset(60, 30, noline, white)
    
    def __init__(self, position):
        super().__init__(PlayerCover.asset, position)
        
    def step(self):
        for x in HeadSoccer.getSpritesbyClass(Player):
            self.x = x.x-30
            self.y = x.y
        
class Ball(PhysicsObject):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.mag = 1
        self.mass = 2
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        self.scored = False
        
    def right(self, event):
        self.velocity[0] += self.mag
        
    def left(self, event):
        self.velocity[0] -= self.mag
        
    def score(self, Goal):
        print(Goal.ident)
        
    def step(self):
        super().step()
        if self.y >= SCREEN_HEIGHT-30:
            self.velocity[1] *= -1
            self.velocity[1] -= GRAVITY
        self.velocity[1] += GRAVITY
        if len(self.collidingWithSprites(Goal)) > 0:
            if self.y <= 230:
                self.velocity[1] *= -1
            elif self.scored == False:
                for x in self.collidingWithSprites(Goal):
                    self.score(x)
                self.scored = True
                ScoreText((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        if self.scored == True and time()-start >= 2:
            self.x = SCREEN_WIDTH/2
            self.y = SCREEN_HEIGHT/2
            self.velocity = [0,0]
            self.scored = False

class ScoreText(Sprite):
    
    asset = TextAsset('Goal!')
    
    def __init__(self, position):
        super().__init__(ScoreText.asset, position)
        #sleep(1)

class HeadSoccer(App):

    def __init__(self):
        super().__init__()
        #Player((SCREEN_WIDTH/2,SCREEN_HEIGHT))
        #PlayerCover((0,0))
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        Sprite(Floor,(0,SCREEN_HEIGHT))
        Goal((0,SCREEN_HEIGHT-200))
        Goal((SCREEN_WIDTH-50,SCREEN_HEIGHT-200))
        
    def classStep(self, sclass):
        for x in self.getSpritesbyClass(sclass):
            x.step()
        
    def step(self):
        self.classStep(Ball)
        self.classStep(Player)
        self.classStep(PlayerCover)
    
HeadSoccer().run()
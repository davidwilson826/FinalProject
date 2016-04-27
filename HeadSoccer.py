''' 
Head Soccer
Author: David Wilson
Credit: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
'''

from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset
from time import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)

noline = LineStyle(0.0, black)

def classDestroy(sclass):
    while len(HeadSoccer.getSpritesbyClass(sclass)) > 0:
        for x in HeadSoccer.getSpritesbyClass(sclass):
            x.destroy()

GRAVITY = 0.5

Floor = RectangleAsset(SCREEN_WIDTH, 10, noline, black)

class Goal(Sprite):
    
    asset = RectangleAsset(50, 200, noline, black)
    
    def __init__(self, position):
        super().__init__(Goal.asset, position)
        self.ident = len(HeadSoccer.getSpritesbyClass(Goal))-1

class PhysicsObject(Sprite):
  
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.velocity = [0,0]
        self.fxcenter = self.fycenter = 0.5
        self.circularCollisionModel()
        self.frameTime = [time(),time()]
        self.deltaTime = 0
        
    def step(self):
        self.frameTime[0] = self.frameTime[1]
        self.frameTime[1] = time()
        self.deltaTime = self.frameTime[1]-self.frameTime[0]
        self.x += self.velocity[0]*self.deltaTime
        self.y += self.velocity[1]*self.deltaTime
        
class Experiment(PhysicsObject):
    
    asset = CircleAsset(10, noline, black)
    
    def __init__(self, position):
        super().__init__(Experiment.asset, self)
        self.velocity = [5,0]
        
class Player(PhysicsObject):
    
    asset = CircleAsset(50, noline, black)
    
    def __init__(self, position):
        super().__init__(Player.asset, position)
        self.mag = 1
        self.speed = 5
        self.jumpForce = 15
        self.mass = 2
        HeadSoccer.listenKeyEvent('keydown', 'd', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'a', self.left)
        HeadSoccer.listenKeyEvent('keyup', 'd', self.stop)
        HeadSoccer.listenKeyEvent('keyup', 'a', self.stop)
        HeadSoccer.listenKeyEvent('keydown', 'w', self.jump)
        PlayerCover((0,0))
        
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
        elif self.y >= SCREEN_HEIGHT:
            self.velocity[1] = 0
            self.y = SCREEN_HEIGHT
            
class PlayerCover(Sprite):
    
    asset = RectangleAsset(100, 50, noline, white)
    
    def __init__(self, position):
        super().__init__(PlayerCover.asset, position)
        
    def step(self):
        for x in HeadSoccer.getSpritesbyClass(Player):
            self.x = x.x-50
            self.y = x.y
        
class Ball(PhysicsObject):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.mag = 1
        self.mass = 1
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        self.score = [0,0]
        self.scored = False
        self.velCollision = [0,0]
        self.collision = False
        self.scoreTime = 0
        
    def right(self, event):
        self.velocity[0] += self.mag
        
    def left(self, event):
        self.velocity[0] -= self.mag
        
    def bounce(self):
        self.velocity[1] *= -1
        self.velocity[1] -= GRAVITY
        
    def step(self):
        super().step()
        if self.y >= SCREEN_HEIGHT-30:
            self.bounce()
        self.velocity[1] += GRAVITY
        if len(self.collidingWithSprites(Player)) > 0:# and self.collision == False:
            colliding = self.collidingWithSprites(Player)[0]
            self.velCollision = self.velocity[:]
            for x in range(2):
                self.velocity[x] = (self.mass-colliding.mass)/(self.mass+colliding.mass)*(self.velCollision[x]-colliding.velocity[x])+colliding.velocity[x]
                colliding.velocity[x] = (2*self.mass)/(self.mass+colliding.mass)*(self.velCollision[x]-colliding.velocity[x])+colliding.velocity[x]
                print(self.velocity)
                print(colliding.velocity)
                self.collision = True
        if len(self.collidingWithSprites(Goal)) > 0:
            if self.y <= SCREEN_HEIGHT-230:
#                self.bounce()
                print('hello')
            elif self.scored == False:
                for x in self.collidingWithSprites(Goal):
                    HeadSoccer.getSpritesbyClass(ScoreText)[0].goal(x)
                self.scored = True
                self.scoreTime = time()
                HeadSoccer.getSpritesbyClass(ScoreText)[0].visible = True
        if self.scored == True and time()-self.scoreTime >= 2:
            self.velocity = [0,0]
            self.x = SCREEN_WIDTH/2
            self.y = SCREEN_HEIGHT/2
            self.scored = False

class ScoreText(Sprite):
    
    asset = TextAsset('Goal!')
    
    def __init__(self, position):
        super().__init__(ScoreText.asset, position)
        self.visible = False
        self.score = [0,0]
        self.placeScore()
        
    def goal(self, Goal):
        self.score[Goal.ident] += 1
        self.placeScore()
        
    def placeScore(self):
        classDestroy(ScoreNum)
        ScoreNum(TextAsset(self.score[0]), (SCREEN_WIDTH/8,SCREEN_HEIGHT/2))
        ScoreNum(TextAsset(self.score[1]), (SCREEN_WIDTH*(7/8),SCREEN_HEIGHT/2))
        
class ScoreNum(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class TimeText(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5

class HeadSoccer(App):

    def __init__(self):
        super().__init__()
        #Player((SCREEN_WIDTH/2,SCREEN_HEIGHT))
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        Sprite(Floor,(0,SCREEN_HEIGHT))
        Goal((0,SCREEN_HEIGHT-200))
        Goal((SCREEN_WIDTH-50,SCREEN_HEIGHT-200))
        ScoreText((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
#        self.getSpritesbyClass(ScoreText)[0].placeScore()
        self.start = time()
        self.elapsed = 0
        
    def classStep(self, sclass):
        for x in self.getSpritesbyClass(sclass):
            x.step()
            
    def timeGame(self):
        self.elapsed = time()-self.start
        classDestroy(TimeText)
        TimeText(TextAsset(str(int(self.elapsed//60))+':'+str(int(self.elapsed%60))),(SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
        
    def step(self):
        self.timeGame()
        self.classStep(Ball)
        self.classStep(Player)
        self.classStep(PlayerCover)
    
HeadSoccer().run()
''' 
Head Soccer
Author: David Wilson
Credit: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python,
https://www.mathsisfun.com/hexadecimal-decimal-colors.html
'''

#Delete frameRate?

from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset
from time import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
blue = Color(0x0000ff, 1.0)
beige = Color(0xF5F5DC, 1.0)

noline = LineStyle(0.0, black)
thinline = LineStyle(1.0, black)

def classDestroy(sclass):
    while len(HeadSoccer.getSpritesbyClass(sclass)) > 0:
        for x in HeadSoccer.getSpritesbyClass(sclass):
            x.destroy()

GRAVITY = 25

class Button(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5

class Border(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)

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
        
    def step(self):
        self.x += self.velocity[0]*deltaTime
        self.y += self.velocity[1]*deltaTime
        
class Experiment(PhysicsObject):
    
    asset = CircleAsset(10, noline, black)
    
    def __init__(self, position):
        super().__init__(Experiment.asset, self)
        self.velocity = [5,0]
        
class Player(PhysicsObject):
    
    asset = CircleAsset(50, noline, blue)
    
    def __init__(self, position):
        super().__init__(Player.asset, position)
        self.mag = 50
        self.speed = 200
        self.jumpForce = 500
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
        self.mag = 42
        self.mass = 1
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        self.score = [0,0]
        self.scored = False
        self.velCollision = [0,0]
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
        if len(self.collidingWithSprites(Player)) > 0:
            colliding = self.collidingWithSprites(Player)[0]
            self.velCollision = self.velocity[:]
            for x in range(2):
                self.velocity[x] = (self.mass-colliding.mass)/(self.mass+colliding.mass)*(self.velCollision[x]-colliding.velocity[x])+colliding.velocity[x]
                colliding.velocity[x] = (2*self.mass)/(self.mass+colliding.mass)*(self.velCollision[x]-colliding.velocity[x])+colliding.velocity[x]
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
            HeadSoccer.getSpritesbyClass(ScoreText)[0].visible = False
            self.scored = False

class ScoreText(Sprite):
    
    asset = TextAsset('Goal!')
    
    def __init__(self, position):
        super().__init__(ScoreText.asset, position)
        self.fxcenter = self.fycenter = 0.5
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
        self.width = 0.2*SCREEN_WIDTH
        self.height = 0.2*SCREEN_HEIGHT
        self.buttons = [((x%3+1)/4*SCREEN_WIDTH-self.width/2, 
        (x//3+1)/4*SCREEN_HEIGHT-self.height/2) for x in range(9)]
        for x in self.buttons:
            Button(RectangleAsset(self.width, self.height, thinline, beige), (x[0],x[1]))
        self.listenMouseEvent('mousedown', self.buttonClick)
        self.start = 0
        self.go = False
        self.frameTime = 0
        self.deltaTime = 0
        self.frameTimes = []
        self.listenKeyEvent('keydown', 'z', self.frameRate)
        
    def frameRate(self, event):
        print(1/(sum(self.frameTimes)/len(self.frameTimes)))
        
    def buttonClick(self, event):
        for x in self.buttons:
            if x[0] <= event.x <= x[0]+self.width and x[1] <= event.y <= x[1]+self.height:
                print(self.buttons.index(x))
                self.prepGame()
        
    def prepGame(self):
        self.unlistenMouseEvent('mousedown', self.buttonClick)
        classDestroy(Button)
        Player((SCREEN_WIDTH/2,SCREEN_HEIGHT))
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        for x in [(0,0,10,SCREEN_HEIGHT), (SCREEN_WIDTH-5,0,10,SCREEN_HEIGHT), 
        (0,SCREEN_HEIGHT-5,SCREEN_WIDTH+5,10), (0,0,SCREEN_WIDTH+5,10)]:
            Border(RectangleAsset(x[2], x[3], noline, black), (x[0],x[1]))
        Goal((0,SCREEN_HEIGHT-200))
        Goal((SCREEN_WIDTH-50,SCREEN_HEIGHT-200))
        ScoreText((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.start = time()
        self.timeGame()
        self.frameTime = time()
        self.go = True
            
    def timeGame(self):
        elapsed = time()-self.start
        seconds = elapsed%60
        if seconds < 10:
            placeholder = ':0'
        else:
            placeholder = ':'
        TimeText(TextAsset(str(int(elapsed//60))+placeholder+str(int(seconds))), 
        (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
        
    def step(self):
        if self.go == True:
            self.getSpritesbyClass(TimeText)[0].destroy()
            self.timeGame()
            global deltaTime
            deltaTime = time()-self.frameTime
            self.frameTimes.append(deltaTime)
            self.frameTime = time()
            for x in [Ball, Player, PlayerCover]:
                for y in self.getSpritesbyClass(x):
                    y.step()
    
HeadSoccer().run()

''' 
Head Soccer
Author: David Wilson
Credit: http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python,
https://www.mathsisfun.com/hexadecimal-decimal-colors.html, http://brythonserver.github.io/ggame/
'''

#White block behind text sprites

from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset
from time import time

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
beige = Color(0xF5F5DC, 1.0)

blue = Color(0x0000ff, 1.0)
green = Color(0x00ff00, 1.0)
red = Color(0xff0000, 1.0)

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
        self.fxcenter = self.fycenter = 0.5
        self.velocity = [0,0]
        self.circularCollisionModel()
        
    def step(self):
        self.x += self.velocity[0]*deltaTime
        self.y += self.velocity[1]*deltaTime
        
class Player(PhysicsObject):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.mag = 50
        self.speed = 200
        self.jumpForce = 500
        self.mass = 2
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
        if self.x <= 25 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.x >= SCREEN_WIDTH-25 and self.velocity[0] > 0:
            self.velocity[0] = 0
        super().step()
        if self.y < SCREEN_HEIGHT:
            self.velocity[1] += GRAVITY
        elif self.y >= SCREEN_HEIGHT:
            self.velocity[1] = 0
            self.y = SCREEN_HEIGHT
            
class Player1(Player):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        HeadSoccer.listenKeyEvent('keydown', 'a', self.left)
        HeadSoccer.listenKeyEvent('keydown', 'd', self.right)
        HeadSoccer.listenKeyEvent('keyup', 'a', self.stop)
        HeadSoccer.listenKeyEvent('keyup', 'd', self.stop)
        HeadSoccer.listenKeyEvent('keydown', 'w', self.jump)
        
class Player2(Player):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        HeadSoccer.listenKeyEvent('keydown', 'left arrow', self.left)
        HeadSoccer.listenKeyEvent('keydown', 'right arrow', self.right)
        HeadSoccer.listenKeyEvent('keyup', 'left arrow', self.stop)
        HeadSoccer.listenKeyEvent('keyup', 'right arrow', self.stop)
        HeadSoccer.listenKeyEvent('keydown', 'up arrow', self.jump)
        
class PlayerCover(Sprite):
    
    asset = RectangleAsset(102, 52, noline, white)
    
    def __init__(self, position):
        super().__init__(PlayerCover.asset, position)
        self.follow = Player1
        
    def step(self):
        for x in HeadSoccer.getSpritesbyClass(self.follow):
            self.x = x.x-51
            self.y = x.y
        
class Ball(PhysicsObject):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball.asset, position)
        self.mag = 42
        self.mass = 1
        HeadSoccer.listenKeyEvent('keydown', 'p', self.right)
        HeadSoccer.listenKeyEvent('keydown', 'i', self.left)
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
#        self.velocity[1] += 50
        
    def step(self):
        super().step()
        if self.y >= SCREEN_HEIGHT-30:
            self.bounce()
        if self.x <= 30 or self.x >= SCREEN_WIDTH-30:
            self.velocity[0] *= -1
        self.velocity[1] += GRAVITY
        for x in [Player1, Player2]:
            if len(self.collidingWithSprites(x)) > 0:
                colliding = self.collidingWithSprites(x)[0]
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
            for x in [Player1, Player2]:
                player = HeadSoccer.getSpritesbyClass(x)[0]
                player.x = SCREEN_WIDTH/4
                player.y = SCREEN_HEIGHT
                player.velocity = [0,0]
            player.x *= 3
            HeadSoccer.getSpritesbyClass(ScoreText)[0].visible = False
            self.scored = False

class ScoreText(Sprite):
    
    asset = TextAsset('Goal!')
    
    def __init__(self, position):
        super().__init__(ScoreText.asset, position)
        self.fxcenter = self.fycenter = 0.5
        self.visible = False
        global score
        score = [0,0]
        self.placeScore()
        
    def goal(self, Goal):
        score[Goal.ident] += 1
        self.placeScore()
        
    def placeScore(self):
        classDestroy(ScoreNum)
        ScoreNum(TextAsset(score[0]), (SCREEN_WIDTH/8,SCREEN_HEIGHT/2))
        ScoreNum(TextAsset(score[1]), (SCREEN_WIDTH*(7/8),SCREEN_HEIGHT/2))
        
class TextSprite(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
class TitleText(TextSprite):
    pass
        
class IntroText(TextSprite):
    pass
        
class ScoreNum(TextSprite):
    pass
        
class TimeText(TextSprite):
    pass
        
class TimeUpText(TextSprite):
    pass

class HeadSoccer(App):

    def __init__(self):
        super().__init__()
        self.width = 0.2*SCREEN_WIDTH
        self.height = 0.2*SCREEN_HEIGHT
        self.buttoncolors = [blue, red, green]*3
        self.buttons = [((x%3+1)/4*SCREEN_WIDTH-self.width/2, 
        (x//3+1)/4*SCREEN_HEIGHT-self.height/2, self.buttoncolors[x]) for x in range(9)]
        self.start = 0
        self.go = False
        self.frameTime = 0
        self.deltaTime = 0
        self.gameTime = 60
        TitleText(TextAsset('Head Soccer!', width=SCREEN_WIDTH, style='50pt Helvetica'), 
        (SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        self.listenMouseEvent('mousedown', self.placeButtonsEvent)
        self.intro = True
        self.transparency = 1
        self.direction = 0
        self.playercolors = []
    
    def placeButtonsEvent(self, event):
        self.unlistenMouseEvent('mousedown', self.placeButtonsEvent)
        self.intro = False
        self.getSpritesbyClass(TitleText)[0].destroy()
        self.getSpritesbyClass(IntroText)[0].destroy()
        self.placeButtons()
    
    def placeButtons(self):
        for x in self.buttons:
            Button(RectangleAsset(self.width, self.height, thinline, x[2]), (x[0],x[1]))
        self.listenMouseEvent('mousedown', self.buttonClick)
        
    def buttonClick(self, event):
        for x in self.buttons:
            if x[0] <= event.x <= x[0]+self.width and x[1] <= event.y <= x[1]+self.height:
                self.playercolors.append(x[2])
                if len(self.playercolors) == 2:
                    self.prepGame(self.playercolors)
        
    def prepGame(self, colors):
        self.unlistenMouseEvent('mousedown', self.buttonClick)
        classDestroy(Button)
        Player1(CircleAsset(50, thinline, colors[0]), (SCREEN_WIDTH/4,SCREEN_HEIGHT))
        Player2(CircleAsset(50, thinline, colors[1]), (SCREEN_WIDTH*3/4,SCREEN_HEIGHT))
        self.getSpritesbyClass(PlayerCover)[1].follow = Player2
        Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        for x in [(0,0,10,SCREEN_HEIGHT), (SCREEN_WIDTH-5,0,10,SCREEN_HEIGHT), 
        (0,SCREEN_HEIGHT-5,SCREEN_WIDTH+5,10), (0,0,SCREEN_WIDTH+5,10)]:
            Border(RectangleAsset(x[2], x[3], noline, black), (x[0],x[1]))
        Goal((SCREEN_WIDTH-50,SCREEN_HEIGHT-200))
        Goal((0,SCREEN_HEIGHT-200))
        ScoreText((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.start = time()
        self.timeGame()
        self.frameTime = time()
        self.go = True
            
    def timeGame(self):
        remaining = self.gameTime-time()+self.start
        if remaining < 0:
            remaining = 0
            if score[0] > score[1]:
                winner = 'Player 1 wins!'
            elif score[1] > score[0]:
                winner = 'Player 2 wins!'
            else:
                winner = "It's a draw!"
            TimeUpText(TextAsset("Time's Up! "+winner, width=SCREEN_WIDTH), (SCREEN_WIDTH/2,SCREEN_HEIGHT/6))
            TimeUpText(TextAsset("Press Space to Restart", width=SCREEN_WIDTH), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.getSpritesbyClass(ScoreText)[0].destroy()
            self.go = False
            self.listenKeyEvent('keydown', 'space', self.restart)
        seconds = remaining%60
        if seconds < 10:
            placeholder = ':0'
        else:
            placeholder = ':'
        TimeText(TextAsset(str(int(remaining//60))+placeholder+str(int(seconds))), 
        (SCREEN_WIDTH/2,SCREEN_HEIGHT/4))
        
    def restart(self, event):
        self.unlistenKeyEvent('keydown', 'space', self.restart)
        for x in [Ball, Player1, Player2, PlayerCover, Goal, Border, TimeUpText, TimeText, ScoreNum]:
            classDestroy(x)
        self.playercolors = []
        self.placeButtons()
        
    def step(self):
        if self.intro == True:
            classDestroy(IntroText)
            IntroText(TextAsset('Click to Continue', width=SCREEN_WIDTH, style='20pt Helvetica',
            fill=Color(0x000000, self.transparency)), (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            if self.transparency == 1:
                self.direction = -0.01
            elif self.transparency == 0:
                self.direction = 0.01
            self.transparency += self.direction
            self.transparency = round(self.transparency, 2)
        if self.go == True:
            self.getSpritesbyClass(TimeText)[0].destroy()
            self.timeGame()
            global deltaTime
            deltaTime = time()-self.frameTime
            self.frameTime = time()
            for x in [Ball, Player1, Player2, PlayerCover]:
                for y in self.getSpritesbyClass(x):
                    y.step()
    
HeadSoccer().run()

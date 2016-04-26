from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)
white = Color(0x0000ff, 1.0)

noline = LineStyle(0.0, black)

def classDestroy(sclass):
    while len(Test.getSpritesbyClass(sclass)) > 0:
        for x in Test.getSpritesbyClass(sclass):
            x.destroy()

class Ball(Sprite):
    
    def __init__(self, asset, position):
        super().__init__(asset, position)
        self.fxcenter = self.fycenter = 0.5
        
    def step(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #print(self.velocity,end=', ')
        
class Ball1(Ball):
    
    asset = CircleAsset(30, noline, black)
    
    def __init__(self, position):
        super().__init__(Ball1.asset, position)
        self.velocity = [5,0]
        self.mass = 5
        self.collision = False
        self.velCollision = [0,0]
        
    def step(self):
        super().step()
        if len(self.collidingWithSprites(Ball2)) > 0 and self.collision == False:
            colliding = self.collidingWithSprites(Ball2)[0]
            self.velCollision = self.velocity[:]
            self.velocity[0] = (self.mass-colliding.mass)/(self.mass+colliding.mass)*(self.velCollision[0]-colliding.velocity[0])+colliding.velocity[0]
            colliding.velocity[0] = (2*self.mass)/(self.mass+colliding.mass)*(self.velCollision[0]-colliding.velocity[0])+colliding.velocity[0]
            print(self.velocity)
            print(colliding.velocity)
            self.collision = True
        
class Ball2(Ball):
    
    asset = CircleAsset(30, noline, white)
    
    def __init__(self, position):
        super().__init__(Ball2.asset, position)
        self.velocity = [2,0]
        self.mass = 5
        
class Test(App):
    
    def __init__(self):
        super().__init__()
        Ball1((30,SCREEN_HEIGHT/2))
        #Ball2((SCREEN_WIDTH-30,SCREEN_HEIGHT/2))
        Ball2((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        self.go = False
        self.listenKeyEvent('keydown', 'space', self.start)
        
    def start(self, event):
        self.go = True
        
    def step(self):
        if self.go == True:
            for x in [Ball1, Ball2]:
                for y in self.getSpritesbyClass(x):
                    y.step()
                
Test().run()
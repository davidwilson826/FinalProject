from ggame import App, Sprite, TextAsset, Color

class TextSprite(Sprite):
    pass

class Transparency(App):
    
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.transparency = 1
        TextSprite(TextAsset('Click to Continue', fill=Color(0x000000, self.transparency), 
        width=500), (200,200))
        
    def step(self):
        self.getSpritesbyClass(TextSprite)[0].destroy()
        TextSprite(TextAsset('Click to Continue', fill=Color(0x000000, self.transparency), 
        width=500), (200,200))
        if self.transparency == 1:
            self.direction = -0.1
        elif self.transparency == 0:
            self.direction = 0.1
        self.transparency += self.direction
        self.transparency = round(self.transparency, 1)
        #print(self.transparency)
        
Transparency().run()
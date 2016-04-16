from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noline = LineStyle(0.0, black)

Floor = RectangleAsset(SCREEN_WIDTH, 10, noline, black)

class Ball(Sprite):

  asset = CircleAsset(30, noline, black)
  
  def __init__(self, position):
    super().__init__(Ball.asset, position)

class BallBounce(App):

  def __init__(self):
    super().__init__()
    Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    Sprite(Floor,(0,SCREEN_HEIGHT))
    
BallBounce().run()

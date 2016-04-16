from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)

noline = LineStyle(0.0, black)

Floor = Sprite(RectangleAsset(10, 10, noline, black))

class Ball(Sprite):

  asset = CircleAsset(10, noline, black)
  
  def __init__(self, position):
    super().__init__(Ball.asset, position)

class BallBounce(App):

  def __init__(self):
    super().__init__()
    Ball((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    Floor((0,SCREEN_HEIGHT))
    
BallBounce().run()

from ggame import App, Sprite, CircleAsset, RectangleAsset, Color, LineStyle, TextAsset

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)

noline = LineStyle(0.0, black)

def classDestroy(sclass):
    while len(HeadSoccer.getSpritesbyClass(sclass)) > 0:
        for x in HeadSoccer.getSpritesbyClass(sclass):
            x.destroy()

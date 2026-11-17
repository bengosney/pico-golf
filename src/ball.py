from actor import Actor
from equipment import ball_golf


class Ball(Actor):
    def __init__(self, x, y=None):
        art = ball_golf
        y = y or -art.FRAME_HEIGHT
        super().__init__(art, x, y)
        self.vx = .75
        self.bounce = .5
        self.friction = .01

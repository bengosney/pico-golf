from actor import Actor
from equipment import ball_golf


class Ball(Actor):
    def __init__(self, x, y=None):
        art = ball_golf
        y = y or -art.FRAME_HEIGHT
        self.velocity = 0
        super().__init__(art, x, y)

    def move(self):
        pass

    def update(self):
        self.move()
        return super().update()
from actor import Actor
from equipment import ball_golf


class Ball(Actor):
    def __init__(self, x):
        art = ball_golf
        super().__init__(art, x)

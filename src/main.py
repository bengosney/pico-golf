import math

import noise

HILL_WIDTH = 0.5  # smaller makes broader hills
HILL_HEIGHT = 20


def circle_height(x):
    angle = 2 * math.pi * x / 119
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return int(60 + value * HILL_HEIGHT)


noise.seed(42)
heights = [circle_height(x) for x in range(119)]
heights.append(heights[0])

sprites = Buffer(128, 128)
with open("tileset.16bpp", "rb") as h:
    h.readinto(sprites)
spritesheet(sprites)


def update(tick):
    pass


def draw(tick):
    pen(0, 0, 0)
    clear()
    pen(15, 15, 15)
    for x in range(120):
        vline(x, heights[x], 120 - heights[x])

    sprite(0, 0, 0)

    text(str(heights[0]), 20, 0)

start()

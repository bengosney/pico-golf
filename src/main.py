import math

import noise

SCREEN_SIZE = 120
SPRITE_SIZE = 8
CELLS = SPRITE_SIZE // 8  # sprite() counts in 8x8 cells
COLUMNS = SCREEN_SIZE // SPRITE_SIZE

HILL_WIDTH = 0.25  # smaller makes broader hills
HILL_HEIGHT = 20


def circle_height(column):
    angle = 2 * math.pi * column / (COLUMNS - 1)
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return int(60 + value * HILL_HEIGHT) // SPRITE_SIZE * SPRITE_SIZE


noise.seed(42)
heights = [circle_height(column) for column in range(COLUMNS - 1)]
heights.append(heights[0])

sprites = Buffer(128, 128)
with open("tileset.16bpp", "rb") as h:
    h.readinto(sprites)
spritesheet(sprites)


def tile(n, x, y):
    per_row = 128 // SPRITE_SIZE
    index = (n % per_row) * CELLS + (n // per_row) * CELLS * 16
    sprite(index, x, y, CELLS, CELLS)


def update(tick):
    pass


def draw(tick):
    pen(0, 0, 0)
    clear()
    pen(15, 15, 15)
    for column, height in enumerate(heights):
        frect(column * SPRITE_SIZE, height, SPRITE_SIZE, SCREEN_SIZE - height)

    sprite(0, 0, 0)

    text(str(heights[0]), 20, 0)

    for column, height in enumerate(heights):
        tile(1, column * SPRITE_SIZE, height)

start()

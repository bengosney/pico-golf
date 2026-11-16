import math

import noise

SCREEN_SIZE = 120
SPRITE_SIZE = 8
COLUMNS = SCREEN_SIZE // SPRITE_SIZE
LEVEL_SIZE = COLUMNS * 10
LEVEL_WIDTH = LEVEL_SIZE * SPRITE_SIZE
VERTICAL_OFFSET = (3 * SPRITE_SIZE)

HILL_WIDTH = 1.0  # smaller makes broader hills
HILL_HEIGHT = 20


def circle_height(column, vertical_offset = VERTICAL_OFFSET):
    angle = 2 * math.pi * column / (LEVEL_SIZE - 1)
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return (int(60 + value * HILL_HEIGHT) // SPRITE_SIZE * SPRITE_SIZE) + vertical_offset


noise.seed(42)
heights = [circle_height(column) for column in range(LEVEL_SIZE - 1)]
heights.append(heights[0])


def ground_at(x, width):
    """Return the highest ground under a span of pixels starting at this x."""
    first = int(x // SPRITE_SIZE)
    last = int((x + width - 1) // SPRITE_SIZE)
    return min(heights[column % LEVEL_SIZE] for column in range(first, last + 1))

import math

import noise

SCREEN_SIZE = 120
SPRITE_SIZE = 8
CELLS = SPRITE_SIZE // 8  # sprite() counts in 8x8 cells
COLUMNS = SCREEN_SIZE // SPRITE_SIZE
LEVEL_SIZE = COLUMNS * 10
VERTICAL_OFFSET = (3 * SPRITE_SIZE)

HILL_WIDTH = 0.10  # smaller makes broader hills
HILL_HEIGHT = 20


def circle_height(column, vertical_offset = VERTICAL_OFFSET):
    angle = 2 * math.pi * column / (COLUMNS - 1)
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return (int(60 + value * HILL_HEIGHT) // SPRITE_SIZE * SPRITE_SIZE) + vertical_offset 


noise.seed(42)
heights = [circle_height(column) for column in range(LEVEL_SIZE)]
heights.append(heights[0])

def load_tileset(name:str) -> Buffer:
    tileset = Buffer(128, 128)
    with open("tileset.16bpp", "rb") as h:
        h.readinto(tileset)
    return tileset

level_tiles = load_tileset("tileset.16bpp")
spritesheet(level_tiles)

camera_x = 0

def tile(n, x, y):
    per_row = 128 // SPRITE_SIZE
    index = (n % per_row) * CELLS + (n // per_row) * CELLS * 16
    sprite(index, x, y, CELLS, CELLS)


def create_strip() -> Buffer:
    column_strip = Buffer(SPRITE_SIZE, SCREEN_SIZE)
    target(column_strip)
    clip()
    tile(1, 0, 0)
    for strip_y in range(SPRITE_SIZE, SCREEN_SIZE, SPRITE_SIZE):
        tile(0, 0, strip_y)
    target()
    clip()

    return column_strip

column_strip = create_strip()

def update(tick):
    global camera_x

    if button(LEFT):
        camera_x = max(0, camera_x - 1)
    if button(RIGHT):
        camera_x += 1

def draw(tick):
    pen(0, 0, 0)
    clear()
    pen(15, 15, 15)

    offset_x = camera_x % SPRITE_SIZE

    for column in range(COLUMNS + 1):
        height_index = (column + (camera_x // SPRITE_SIZE)) % COLUMNS
        height = heights[height_index]
        x = column * SPRITE_SIZE - offset_x
        crop = max(0, -x)
        blit(column_strip, crop, 0, SPRITE_SIZE - crop, SCREEN_SIZE - height, x + crop, height)

start()

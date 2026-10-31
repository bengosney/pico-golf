import math

import adventurer
import noise

SCREEN_SIZE = 120
SPRITE_SIZE = 8
CELLS = SPRITE_SIZE // 8  # sprite() counts in 8x8 cells
COLUMNS = SCREEN_SIZE // SPRITE_SIZE
LEVEL_SIZE = COLUMNS * 10
VERTICAL_OFFSET = (3 * SPRITE_SIZE)

HILL_WIDTH = 1.0  # smaller makes broader hills
HILL_HEIGHT = 20

CHAR_SCREEN_CENTER = (SCREEN_SIZE // 2) - adventurer.FRAME_WIDTH
CHAR_COLUMN = CHAR_SCREEN_CENTER // SPRITE_SIZE


def circle_height(column, vertical_offset = VERTICAL_OFFSET):
    angle = 2 * math.pi * column / (LEVEL_SIZE - 1)
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return (int(60 + value * HILL_HEIGHT) // SPRITE_SIZE * SPRITE_SIZE) + vertical_offset 


noise.seed(42)
heights = [circle_height(column) for column in range(LEVEL_SIZE - 1)]
heights.append(heights[0])

def load_tileset(name:str) -> Buffer:
    tileset = Buffer(128, 128)
    with open(name, "rb") as h:
        h.readinto(tileset)
    return tileset

level_tiles = load_tileset("tileset.16bpp")
spritesheet(level_tiles)

character_tiles = load_tileset("adventurer.16bpp")

camera_x = 0

char_y = adventurer.FRAME_HEIGHT

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
    global camera_x, char_y

    scroll_speed = 3

    if button(LEFT):
        camera_x -= scroll_speed
    if button(RIGHT):
        camera_x += scroll_speed

    column = CHAR_COLUMN
    height_index = (column + (camera_x // SPRITE_SIZE)) % LEVEL_SIZE
    height = heights[height_index]
    char_y = height - adventurer.FRAME_HEIGHT

def draw(tick):
    pen(7, 10, 12)
    clear()
    pen(15, 15, 15)

    offset_x = camera_x % SPRITE_SIZE

    ## Level
    spritesheet(level_tiles)
    for column in range(COLUMNS + 1):
        height_index = (column + (camera_x // SPRITE_SIZE)) % LEVEL_SIZE
        height = heights[height_index]
        x = column * SPRITE_SIZE - offset_x
        crop = max(0, -x)
        blit(column_strip, crop, 0, SPRITE_SIZE - crop, SCREEN_SIZE - height, x + crop, height)

    ## Character
    spritesheet(character_tiles)
    frames = adventurer.ACTIONS["walk"]
    frame = frames[tick // 8 % len(frames)]
    sprite(frame, CHAR_SCREEN_CENTER, char_y, adventurer.CELLS_WIDE, adventurer.CELLS_HIGH)

start()

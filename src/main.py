import math

import adventurer
import noise
from debug import debug, render_debug

SCREEN_SIZE = 120
SPRITE_SIZE = 8
CELLS = SPRITE_SIZE // 8  # sprite() counts in 8x8 cells
COLUMNS = SCREEN_SIZE // SPRITE_SIZE
LEVEL_SIZE = COLUMNS * 10
VERTICAL_OFFSET = (3 * SPRITE_SIZE)

HILL_WIDTH = 1.0  # smaller makes broader hills
HILL_HEIGHT = 20

GRAVITY = 1
CHAR_SCREEN_CENTER = (SCREEN_SIZE // 2) - adventurer.FRAME_WIDTH
CHAR_SPEED = 3
CHAR_JUMP = -(GRAVITY * 5)
CHAR_FOOT_INSET = 3  # the frame is wider than the character's feet
MAX_STEP_UP = SPRITE_SIZE // 2

def circle_height(column, vertical_offset = VERTICAL_OFFSET):
    angle = 2 * math.pi * column / (LEVEL_SIZE - 1)
    value = noise.noise2(HILL_WIDTH * math.cos(angle), HILL_WIDTH * math.sin(angle))
    return (int(60 + value * HILL_HEIGHT) // SPRITE_SIZE * SPRITE_SIZE) + vertical_offset 


noise.seed(42)
heights = [circle_height(column) for column in range(LEVEL_SIZE - 1)]
heights.append(heights[0])


def ground_at(char_left):
    """Return the highest ground under the feet of a character at this x."""
    first = (char_left + CHAR_FOOT_INSET) // SPRITE_SIZE
    last = (char_left + adventurer.FRAME_WIDTH - CHAR_FOOT_INSET - 1) // SPRITE_SIZE
    return min(heights[column % LEVEL_SIZE] for column in range(first, last + 1))

def is_on_ground(char_left) -> bool:
    ground = ground_at(char_left)
    feet = char_y + adventurer.FRAME_HEIGHT
    return feet == ground

def load_tileset(name:str) -> Buffer:
    tileset = Buffer(128, 128)
    with open(name, "rb") as h:
        h.readinto(tileset)
    return tileset

level_tiles = load_tileset("tileset.16bpp")
spritesheet(level_tiles)

character_tiles = load_tileset("adventurer.16bpp")

char_x = CHAR_SCREEN_CENTER
char_y = ground_at(char_x) - adventurer.FRAME_HEIGHT
char_vertical_velocity = 0
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
    global camera_x, char_x, char_y, char_vertical_velocity

    new_x = char_x
    if button(LEFT):
        new_x -= CHAR_SPEED
    if button(RIGHT):
        new_x += CHAR_SPEED

    if pressed(A) and is_on_ground(char_x):
        char_vertical_velocity += CHAR_JUMP

    feet = char_y + adventurer.FRAME_HEIGHT
    if feet - ground_at(new_x) <= MAX_STEP_UP:
        char_x = new_x

    ground = ground_at(char_x)
    feet = min(feet + char_vertical_velocity, ground)
    char_vertical_velocity += GRAVITY

    if feet == ground:
        char_vertical_velocity = 0
    char_y = feet - adventurer.FRAME_HEIGHT

    camera_x = char_x - CHAR_SCREEN_CENTER


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

    render_debug()

start()

import adventurer
from actor import GRAVITY, Actor, load_sheet
from debug import debug, render_debug
from level import COLUMNS, LEVEL_SIZE, SCREEN_SIZE, SPRITE_SIZE, heights

CELLS = SPRITE_SIZE // 8  # sprite() counts in 8x8 cells

CHAR_SCREEN_CENTER = (SCREEN_SIZE // 2) - adventurer.FRAME_WIDTH
CHAR_SPEED = 3
CHAR_JUMP = -(GRAVITY * 5)
CHAR_FOOT_INSET = 3  # the frame is wider than the character's feet

level_tiles = load_sheet("tileset.16bpp")
spritesheet(level_tiles)

player = Actor(adventurer, CHAR_SCREEN_CENTER, action="walk", foot_inset=CHAR_FOOT_INSET)
actors = [player]
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

    distance = 0
    if button(LEFT):
        distance -= CHAR_SPEED
    if button(RIGHT):
        distance += CHAR_SPEED

    if pressed(A):
        player.jump(CHAR_JUMP)
    player.move(distance)
    if distance:
        player.blit_flags = distance < 0

    for actor in actors:
        actor.update()

    camera_x = player.x - CHAR_SCREEN_CENTER


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

    ## Actors
    for actor in actors:
        actor.draw(tick, camera_x)

    render_debug()

start()

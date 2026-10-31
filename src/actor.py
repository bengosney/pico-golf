from level import LEVEL_WIDTH, SCREEN_SIZE, SPRITE_SIZE, ground_at

GRAVITY = 1
MAX_STEP_UP = SPRITE_SIZE // 2
TICKS_PER_FRAME = 8

sheets = {}


def load_sheet(name: str, width: int = 128, height: int = 128) -> Buffer:
    """Load a sprite sheet, sharing it between everything that draws from it."""
    if name not in sheets:
        sheets[name] = Buffer(width, height)
        with open(name, "rb") as h:
            h.readinto(sheets[name])
    return sheets[name]


class Actor:
    """A sprite standing in the level, drawn from a module made by tools/character.py.

    Call update() each tick to give it gravity and collision, or leave it out
    for scenery that stays where it was put.
    """

    def __init__(self, art, x, action="idle", foot_inset=0):
        self.art = art
        self.sheet = load_sheet(art.SHEET, art.SHEET_WIDTH, art.SHEET_HEIGHT)
        self.action = action
        self.blit_flags = 0
        self.foot_inset = foot_inset  # for frames wider than the character's feet
        self.foot_width = art.FRAME_WIDTH - 2 * foot_inset
        self.x = x
        self.y = ground_at(x + foot_inset, self.foot_width) - art.FRAME_HEIGHT
        self.vertical_velocity = 0
        self.last_on_ground = 0

    def is_on_ground(self) -> bool:
        return self.last_on_ground == 0

    def jump(self, velocity):
        if self.last_on_ground < 5 and self.vertical_velocity >= 0:
            self.vertical_velocity = velocity

    def move(self, distance):
        new_x = self.x + distance
        feet = self.y + self.art.FRAME_HEIGHT
        if feet - ground_at(new_x + self.foot_inset, self.foot_width) <= MAX_STEP_UP:
            self.x = new_x

        if distance > 0:
            self.blit_flags |= HFLIP
        if distance < 0:
            self.blit_flags &= ~HFLIP

        if self.is_on_ground():
            if distance == 0:
                self.action = "idle"
            else:
                self.action = "walk"

        if self.vertical_velocity < 0:
            self.action = "jump"


    def update(self):
        ground = ground_at(self.x + self.foot_inset, self.foot_width)
        feet = min(self.y + self.art.FRAME_HEIGHT + self.vertical_velocity, ground)
        self.vertical_velocity += GRAVITY

        if feet == ground:
            self.vertical_velocity = 0
            self.last_on_ground = 0
        else:
            self.last_on_ground += 1

        self.y = feet - self.art.FRAME_HEIGHT

    def draw(self, tick, camera_x):
        art = self.art
        x = (self.x - camera_x) % LEVEL_WIDTH
        if x > LEVEL_WIDTH - art.FRAME_WIDTH:
            x -= LEVEL_WIDTH
        if x >= SCREEN_SIZE:
            return

        frames = art.ACTIONS[self.action]
        frame = frames[tick // TICKS_PER_FRAME % len(frames)]
        per_row = art.SHEET_WIDTH // 8
        sheet_x = frame % per_row * 8
        sheet_y = frame // per_row * 8

        crop_left = max(0, -x)
        crop_right = max(0, x + art.FRAME_WIDTH - SCREEN_SIZE)
        crop_top = max(0, -self.y)
        width = art.FRAME_WIDTH - crop_left - crop_right
        height = art.FRAME_HEIGHT - crop_top
        blit(
            self.sheet,
            sheet_x + (crop_right if self.blit_flags else crop_left),
            sheet_y + crop_top,
            width,
            height,
            x + crop_left,
            self.y + crop_top,
            width,
            height,
            self.blit_flags,
        )

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
        self.foot_inset = foot_inset  # for frames wider than the character's feet
        self.foot_width = art.FRAME_WIDTH - 2 * foot_inset
        self.x = x
        self.y = ground_at(x + foot_inset, self.foot_width) - art.FRAME_HEIGHT
        self.vertical_velocity = 0

    def is_on_ground(self) -> bool:
        ground = ground_at(self.x + self.foot_inset, self.foot_width)
        return self.y + self.art.FRAME_HEIGHT == ground

    def jump(self, velocity):
        if self.is_on_ground():
            self.vertical_velocity += velocity

    def move(self, distance):
        new_x = self.x + distance
        feet = self.y + self.art.FRAME_HEIGHT
        if feet - ground_at(new_x + self.foot_inset, self.foot_width) <= MAX_STEP_UP:
            self.x = new_x

    def update(self):
        ground = ground_at(self.x + self.foot_inset, self.foot_width)
        feet = min(self.y + self.art.FRAME_HEIGHT + self.vertical_velocity, ground)
        self.vertical_velocity += GRAVITY

        if feet == ground:
            self.vertical_velocity = 0
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

        # blit draws too much when it clips the left or top edge, so crop here
        crop_x = max(0, -x)
        crop_y = max(0, -self.y)
        blit(
            self.sheet,
            sheet_x + crop_x,
            sheet_y + crop_y,
            art.FRAME_WIDTH - crop_x,
            art.FRAME_HEIGHT - crop_y,
            x + crop_x,
            self.y + crop_y,
        )

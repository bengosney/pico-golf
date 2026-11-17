from actor import Actor
from level import ground_at


class Player(Actor):
    """An actor that walks and jumps, picking its animation from what it's doing."""

    def __init__(self, art, x, action="idle", foot_inset=0):
        self.action = action
        self.foot_inset = foot_inset  # for frames wider than the character's feet
        self.foot_width = art.FRAME_WIDTH - 2 * foot_inset
        super().__init__(art, x)  # places the player using ground_under

    def ground_under(self, x):
        return ground_at(x + self.foot_inset, self.foot_width)

    def current_frames(self):
        return self.art.ACTIONS[self.action]

    def jump(self, velocity):
        if self.last_on_ground < 5 and self.vy >= 0:
            self.vy = velocity

    def move(self, distance):
        self.step(distance)

        if distance > 0:
            self.blit_flags |= HFLIP
        if distance < 0:
            self.blit_flags &= ~HFLIP

        if self.is_on_ground():
            if distance == 0:
                self.action = "idle"
            else:
                self.action = "walk"

        if self.vy < 0:
            self.action = "jump"

# PicoSystem firmware globals, which boot.py copies into builtins.
# Based on Pimoroni's picosystem.py (MIT), https://github.com/pimoroni/picosystem
# with the names and signatures it is missing added from the firmware source.

from typing import overload

COPY: int
ALPHA: int
MASK: int

UP: int
DOWN: int
LEFT: int
RIGHT: int
A: int
B: int
X: int
Y: int

class Buffer:
    def __buffer__(self, flags: int, /) -> memoryview: ...
    def __init__(self, w: int, h: int):
        """Create a new Buffer."""

class Voice:
    def __init__(
        self,
        attack: int = 100,
        decay: int = 50,
        sustain: int = 80,
        release: int = 100,
        bend: int = 0,
        bend_ms: int = 0,
        reverb: int = 0,
        noise: int = 0,
        distort: int = 0,
    ):
        """Create a new Voice."""

    def play(self, note: int, duration: int = 500, volume: int = 100):
        """Play a note."""

    def envelope(
        self, attack: int = -1, decay: int = -1, sustain: int = -1, release: int = -1
    ):
        """Change envelope parameters."""

    def effects(self, reverb: int = -1, noise: int = -1, distort: int = -1):
        """Change effect parameters."""

    def bend(self, frequency: int, duration: int = 100):
        """Change pitch-bend parameters."""

def init():
    """Initialize PicoSystem.

    Done automatically at boot. Don't call!

    """

def _logo():
    """Render 1-bit centered logo in pen colour."""

def start():
    """Start PicoSystem main loop.

    Make sure you have defined:

    def update(tick):
        pass

    def draw(tick):
        pass

    """

def quit():
    """Break out of PicoSystem main loop."""

def flip():
    """Flip buffer to screen."""

def stats() -> tuple[int, int, int, int, int]:
    """Get system stats.

    Returns a tuple:
        FPS
        Idle time (us)
        Tick time (us)
        Update time (us)
        Draw time (us)

    """

def clear():
    """Clear buffer to pen colour."""

@overload
def pen():
    """Reset pen."""

@overload
def pen(rgba: int):
    """Set pen to 16-bit colour.

    :param rgba: 16-bit colour value: 0xARGB.

    """

@overload
def pen(r: int, g: int, b: int):
    """Set pen colour - rgb.

    :param r: Red (0 to 15).
    :param g: Green (0 to 15).
    :param b: Blue (0 to 15).

    """

@overload
def pen(r: int, g: int, b: int, a: int):
    """Set pen colour - rgba.

    :param r: Red (0 to 15).
    :param g: Green (0 to 15).
    :param b: Blue (0 to 15).
    :param a: Alpha (0 to 15).

    """

@overload
def alpha() -> None:
    """Reset global alpha

    Resets to full alpha: 15

    """

@overload
def alpha(a: int) -> None:
    """Set global alpha.

    :param a: Alpha (0 to 15)

    """

@overload
def clip() -> None:
    """Clear clip rectangle."""

@overload
def clip(x: int, y: int, w: int, h: int) -> None:
    """Set clip rectangle.

    Call with no arguments to reset.

    """

@overload
def blend() -> None:
    """Clear blend mode."""

@overload
def blend(mode: int) -> None:
    """Set blend mode.

    One of: ALPHA, COPY, MASK

    Call with no arguments to reset.

    """

@overload
def target() -> None:
    """Reset draw target."""

@overload
def target(buffer: Buffer) -> None:
    """Set draw target."""

@overload
def camera() -> None:
    """Reset camera."""

@overload
def camera(x: int, y: int) -> None:
    """Set camera to x,y."""

@overload
def cursor() -> None:
    """Reset text cursor."""

@overload
def cursor(x: int, y: int) -> None:
    """Set text cursor."""

@overload
def spritesheet() -> None:
    """Reset spritesheet to default."""

@overload
def spritesheet(spritesheet: Buffer) -> None:
    """Set spritesheet."""

def pixel(x: int, y: int) -> None:
    """Set a single pixel."""

def line(x: int, y: int, x2: int, y2: int) -> None:
    """Draw an arbitrary line.

    :param x: Start x-position.
    :param y: Start y-position.
    :param x2: End x-position.
    :param y2: End x-position.

    """

def hline(x: int, y: int, length) -> None:
    """Draw a fast horizontal line.

    Draws a fast horizontal line, starting from
    point x,y and running for length pixels.

    """

def vline(x: int, y: int, length) -> None:
    """Draw a fast vertical line.

    Draws a fast vertical line, starting form
    point x,y and running for length pixels.

    """

def rect(x: int, y: int, w, h) -> None:
    """Draw a rectangle."""

def frect(x: int, y: int, w, h) -> None:
    """Draw a filled rectangle."""

def circle(x: int, y: int, r: int) -> None:
    """Draw a circle."""

def fcircle(x: int, y: int, r: int) -> None:
    """Draw a filled circle."""

def ellipse(x: int, y: int, rx: int, ry: int) -> None:
    """Draw an ellipse."""

def fellipse(x: int, y: int, rx: int, ry: int) -> None:
    """Draw a filled ellipse."""

@overload
def poly(points: list[tuple[int, int]]) -> None:
    """Draw a polygon."""

@overload
def poly(*args: tuple[int, int]) -> None:
    """Draw a polygon."""

@overload
def fpoly(points: list[tuple[int, int]]) -> None:
    """Draw a filled polygon."""

@overload
def fpoly(*args: tuple[int, int]) -> None:
    """Draw a filled polygon."""

@overload
def blit(buffer: Buffer, x: int, y: int, w: int, h: int, dx: int, dy: int) -> None:
    """Blit a buffer to the screen: 1:1.

    :param x: Source x-position.
    :param y: Source y-position.
    :param w: Source width.
    :param h: Source height.
    :param dx: Destination x-position.
    :param dy: Destination y-position.

    """

@overload
def blit(
    buffer: Buffer, x: int, y: int, w: int, h: int, dx: int, dy: int, dw: int, dh: int
) -> None:
    """Blit a buffer to the screen: stretched.

    :param x: Source x-position.
    :param y: Source y-position.
    :param w: Source width.
    :param h: Source height.
    :param dx: Destination x-position.
    :param dy: Destination y-position.
    :param dx: Destination width.
    :param dy: Destination height.

    """

@overload
def blit(
    buffer: Buffer,
    x: int,
    y: int,
    w: int,
    h: int,
    dx: int,
    dy: int,
    dw: int,
    dh: int,
    flags: int,
) -> None:
    """Blit part of a Buffer, flags can be HFLIP and/or VFLIP."""

@overload
def sprite(index: int, x: int, y: int) -> None:
    """Draw a sprite at x,y.

    :param index: sprite index (sprites numbered 0 to 255)
    :param x: x-position.
    :param y: y-position.

    """

@overload
def sprite(index: int, x: int, y: int, cx: int, cy: int) -> None:
    """Draw a group of sprites at x,y.

    Provide a destination width and height

    :param index: sprite index (sprites numbered 0 to 255)
    :param x: x-position.
    :param y: y-position.
    :param cx: count of sprites along x axis.
    :param cy: count of sprites along y axis.

    """

@overload
def sprite(index: int, x: int, y: int, cx: int, cy: int, dw: int, dh: int) -> None:
    """Draw a group of sprites at x,y.

    Provide a destination width and height

    :param index: sprite index (sprites numbered 0 to 255)
    :param x: x-position.
    :param y: y-position.
    :param cx: count of sprites along x axis.
    :param cy: count of sprites along y axis.
    :param dw: destination width.
    :param dw: destination height.

    """

@overload
def sprite(
    index: int, x: int, y: int, cx: int, cy: int, dw: int, dh: int, flags: int
) -> None:
    """Draw a scaled sprite, flags can be HFLIP and/or VFLIP."""

@overload
def text(text: str) -> None:
    """Draw text.

    :param text: Text to draw.

    """

@overload
def text(text: str, wrap: int) -> None:
    """Draw text.

    :param text: Text to draw.
    :param wrap: Width to wrap text.

    """

@overload
def text(text: str, x: int, y: int) -> None:
    """Draw text at x, y.

    :param text: Text to draw.
    :param x: x-position.
    :param y: y-position.

    """

@overload
def text(text: str, x: int, y: int, wrap: int) -> None:
    """Draw text at x, y.

    :param text: Text to draw.
    :param x: x-position.
    :param y: y-position.
    :param wrap: Width to wrap text.

    """

@overload
def measure(text: str) -> tuple[int, int]:
    """Measure text."""

@overload
def measure(text: str, wrap: int) -> tuple[int, int]:
    """Measure text, wrapped to "wrap" pixels."""

def rgb(r: int, g: int, b: int, a: int = 15) -> int:
    """Build RGB colour."""

def hsv(h: float, s: float, v: float, a: float = 1.0) -> int:
    """Convert HSV to RGB.

    :param h: Hue (0.0 to 1.0)
    :param s: Saturation (0.0 to 1.0)
    :param v: Value (0.0 to 1.0)

    """

def intersects(x, y, w, h, cx, cy, cw, ch):
    """Check if two rectangles intersect."""

def intersection(x, y, w, h, cx, cy, cw, ch):
    """Get the intersection of two rectangles.

    Returns: tuple: x, y, w, h

    """

def contains(x, y, cx, cy, cw, ch):
    """Check if rectangle contains point."""

def pressed(button: int) -> bool:
    """Check if a button has been pressed."""

def button(button: int) -> bool:
    """Check if a button is presed."""

def battery() -> int:
    """Get battery voltage."""

def led(r: int, g: int, b: int):
    """Set the user LED.

    :param r: Red (0 to 15).
    :param g: Green (0 to 15).
    :param b: Blue (0 to 15).

    """

def backlight(brightness):
    """Set the display backlight.

    :param brightness: Brightness (0 to 100).

    """

def play(voice: Voice, duration: int = 500, volume: int = 100):
    """Play a Voice."""

HFLIP: int
VFLIP: int
PEN: int
DARKEN: int
LIGHTEN: int
ADD: int
SUBTRACT: int
MULTIPLY: int
DISSOLVE: int
CHERRY: int
APPLE: int
BANANA: int
ORANGE: int
AUBERGINE: int
CARROT: int
POTATO: int
LEAF: int
PARSNIP: int
MEAT: int
BEAN: int
RADISH: int
STRAWBERRY: int
PUMPKIN: int
CUCUMBER: int
SALT1: int
SWORD1: int
SWORD2: int
SWORD3: int
AXE1: int
DAGGER: int
MACE1: int
BOW: int
ARROW1: int
ARROW2: int
ARROW3: int
TRIDENT1: int
SPEAR: int
TRIDENT2: int
MACHINEGUN: int
PISTOL: int
SHOTGUN: int
GEM1: int
GEM2: int
GEM3: int
GEM4: int
GEM5: int
GEM6: int
AMULET: int
FOLDER: int
COIN1: int
SKULL: int
TICK: int
CROSS: int
IDOL1: int
IDOL2: int
IDOL3: int
IDOL4: int
SWEETCORN: int
BROCCOLI: int
BISCUIT: int
BERRIES: int
SCEPTRE: int
FIRE: int
LASERGUN1: int
LASERGUN2: int
HELMET1: int
HELMET2: int
HELMET3: int
HELMET4: int
__1: int
__2: int
__3: int
__4: int
HEART1: int
SLIME: int
COIN2: int
SWORD4: int
SWORD5: int
__5: int
DYNAMITE: int
MEDPACK: int
GOGGLES: int
HELMET5: int
BOMB: int
OILCAN: int
SHIRT1: int
SHIRT2: int
SPEECH: int
DREAM: int
HEART2: int
HEART3: int
HEART4: int
__6: int
TORCH: int
ICE: int
__7: int
__8: int
__9: int
__10: int
UPARROW: int
RING1: int
RING2: int
RING3: int
RING4: int
__11: int
TOKEN: int
VIAL1: int
VIAL2: int
RING5: int
RING6: int
BLOCK1: int
BLOCK2: int
BLOCK3: int
BLOCK4: int
BLOCK5: int
BLOCK6: int
BLOCK7: int
BLOCK8: int
BLOCK9: int
SHIELD1: int
SACK: int
BUTTON: int
VIAL3: int
VIAL4: int
TOOTH: int
BONE: int
HALFBLOCK1: int
HALFBLOCK2: int
HALFBLOCK3: int
HALFBLOCK4: int
HALFBLOCK5: int
HALFBLOCK6: int
HALFBLOCK7: int
HALFBLOCK8: int
HALFBLOCK9: int
SHIELD2: int
SHIELD3: int
FLOWER1: int
FLOWER2: int
FLOWER3: int
FLOWER4: int
STAFF1: int
STAFF2: int
STAFF3: int
STICK1: int
SPIKEBALL: int
MACE2: int
AXE2: int
__12: int
SWORD6: int
SWORD7: int
SWORD8: int
CROWN1: int
GOLD: int
GEM7: int
GEM8: int
GEM9: int
AXE3: int
MUSHROOM: int
SALT2: int
STICK2: int
VIAL5: int
VIAL6: int
DOT: int
HELMET6: int
SWORD9: int
SWORD10: int
SWORD11: int
CROWN2: int

_F2 = 0.3660254
_G2 = 0.21132487
_G2_2 = 2 * _G2 - 1
_SCALE = 99.0
_D = 0.70710678

_GRAD_X = (1.0, -1.0, 0.0, 0.0, _D, -_D, _D, -_D)
_GRAD_Y = (0.0, 0.0, 1.0, -1.0, _D, _D, -_D, -_D)

_perm = bytearray(512)


def seed(n=0):
    """Shuffle the gradients. The same seed always gives the same noise."""
    for i in range(256):
        _perm[i] = i

    state = (n & 0xFFFF) ^ 0xACE1 or 1
    for i in range(255, 0, -1):
        state ^= (state << 7) & 0xFFFF
        state ^= state >> 9
        state ^= (state << 8) & 0xFFFF
        j = state % (i + 1)
        _perm[i], _perm[j] = _perm[j], _perm[i]

    for i in range(256):
        _perm[i + 256] = _perm[i]


def noise2(x, y):
    """Return 2D simplex noise at x, y, from -1.0 to 1.0.

    Features are about one unit wide, so scale x and y to change their size.
    """
    s = (x + y) * _F2
    xs = x + s
    ys = y + s
    i = int(xs)
    if xs < i:
        i -= 1
    j = int(ys)
    if ys < j:
        j -= 1

    t = (i + j) * _G2
    x0 = x - i + t
    y0 = y - j + t

    if x0 > y0:
        i1 = 1
        j1 = 0
    else:
        i1 = 0
        j1 = 1

    x1 = x0 - i1 + _G2
    y1 = y0 - j1 + _G2
    x2 = x0 + _G2_2
    y2 = y0 + _G2_2

    ii = i & 255
    jj = j & 255
    n = 0.0

    a = 0.5 - x0 * x0 - y0 * y0
    if a > 0:
        g = _perm[ii + _perm[jj]] & 7
        a *= a
        n += a * a * (_GRAD_X[g] * x0 + _GRAD_Y[g] * y0)

    a = 0.5 - x1 * x1 - y1 * y1
    if a > 0:
        g = _perm[ii + i1 + _perm[jj + j1]] & 7
        a *= a
        n += a * a * (_GRAD_X[g] * x1 + _GRAD_Y[g] * y1)

    a = 0.5 - x2 * x2 - y2 * y2
    if a > 0:
        g = _perm[ii + 1 + _perm[jj + 1]] & 7
        a *= a
        n += a * a * (_GRAD_X[g] * x2 + _GRAD_Y[g] * y2)

    return n * _SCALE


seed()

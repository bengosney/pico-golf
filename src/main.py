import noise

noise.seed(42)
heights = [int(60 + noise.noise2(x * 0.05, 0) * 30) for x in range(120)]

def setup():
    pass

def update(tick):
    pass

def draw(tick):
    pen(0, 0, 0)
    clear()
    pen(15, 15, 15)
    for x in range(120):
        vline(x, heights[x], 120 - heights[x])

setup()
start()

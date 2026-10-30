def setup():
    pass


def update(tick):
    pass


def draw(tick):
    pen(0, 0, 0)
    clear()
    pen(15, 15, 15)
    text("Hello World!", 0, 0)
    text(str(tick), 0, 20)


setup()
start()

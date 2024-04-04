class Arena:
    def __init__(self, position, size):
        (x, y) = position
        (width, height) = size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x, y, width, height)

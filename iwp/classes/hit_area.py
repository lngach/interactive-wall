from . import movie_data


class HitArea(MovieData):
    active = None
    top = None
    bottom = None
    left = None
    right = None

    def __init__(self, *args, **kwargs):
        top = args[0] or kwargs.get("top")
        bottom = args[1] or kwargs.get("bottom")
        left = args[2] or kwargs.get("left")
        right = args[3] or kwargs.get("right")
        movie = args[4] or kwargs.get("movie")
        if movie != None and top != None and bottom != None and left != None and right != None:
            self.init(top, bottom, left, right, movie)
        elif top != None and bottom != None and left != None and right != None:
            self.init(top, bottom, left, right, '')
        else:
            self.init(0.0, 0.0, 0.0, 0.0, '')

    def init(self, top, bottom, left, right, movie):
        self.init(m)
        self.active = True
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def is_active(self):
        super().is_active() and self.active

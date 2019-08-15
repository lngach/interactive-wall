from . import iw


def index(request):
    return iw.InteractiveWall.run()

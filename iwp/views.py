from django.http import HttpResponse
from .iw import InteractiveWall


def index(request):
    iw = InteractiveWall()
    iw.run()
    return HttpResponse("hihi")

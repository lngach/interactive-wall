from . import movie_data


class WaitMovieData(MovieData):

    wait_time = None

    def __init__(self, *args, **kwargs):
        time = args[0] or kwargs.get("time")
        movie = args[1] or kwargs.get("movie")
        if time == None and movie == None:
            self.init(0, '')
        else:
            self.init(time, movie)

    def init(self, time, movie):
        self.init(movie)

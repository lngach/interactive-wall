class MovieData():
    movieId = None

    def __init__(self, *args, **kwargs):
        movie = args[0] or kwargs.get("movie")
        if movie == None:
            self.init("")
        else:
            self.init(movie)

    def init(self, movie):
        self.movieId = movie

    def is_active(self):
        return len(self.movieId) > 0

    def movie_status_key(self):
        if (self.is_active()):
            return self.movieId + '_status'
        return None

    def movie_start_key(self):
        if (self.is_active()):
            return self.movieId + '_play'
        return None

    def movie_stop_key(self):
        if (self.is_active()):
            return self.movieId + '_stop'
        return None

    def movie_pause_key(self):
        if (self.is_active()):
            return self.movieId + '_pause'
        return None

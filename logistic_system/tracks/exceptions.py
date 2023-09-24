class TrackNotFoundError(Exception):
    def __init__(self, *args):
        """Raise exception if track not found."""
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'TrackNotFoundError ({self.message})'
        return 'TrackNotFoundError has been raised.'

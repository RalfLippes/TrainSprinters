class Connection:
    """
    Contains all the aspects of a connection, including start station, end station
    and the duration of riding the connection.
    """
    def __init__(self, start_station, end_station, duration):
        self.start_station = start_station
        self.end_station = end_station
        self.duration = duration

    def __hash__(self):
        """Unique hash to compare uniqueness in sets"""
        return hash((self.start_station, self.end_station, self.duration))

    def __eq__(self, other):
        """
        Two connections are equal if they have the same start station,
        end station, and duration.
        """
        return (self.start_station == other.start_station and
                self.end_station == other.end_station and
                self.duration == other.duration)

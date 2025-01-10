class Connection:
    """
    Contains all the aspects of a connection, including start station, end station
    and the duration of riding the connection.
    """
    def __init__(self, start_station, end_station, duration):
        self.start_station = start_station
        self.end_station = end_station
        self.duration = duration

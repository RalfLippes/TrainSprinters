class Station:
    """
    Initializes a trajectory which will store connection objects. Contains a function
    to add a connection to the list of connections.
    """
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def distance(self, station_2):
        """
        Finds the distance between the current station and station_2 object.
        """
        x1 = self.x
        y1 = self.y
        x2 = station_2.x
        y2 = station_2.y
        euclidean_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return euclidean_distance

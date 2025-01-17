class Trajectory:
    """
    Initializes a trajectory which will store connection objects. Contains a function
    to add a connection to the list of connections.
    """
    def __init__(self):
        self.connection_list = []

    def add_connection(self, connection_object):
        """Manually add a connection object to the connection list"""
        self.connection_list.append(connection_object)

    def keep_connections(self, index):
        """Keeps all connections up to and including the given index"""
        self.connection_list = self.connection_list[:index + 1]

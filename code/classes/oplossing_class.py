from code.other_functions.calculate_score import calculate_score

class Solution:
    """
    Initializes a solution which will store trajectory objects. Contains a function
    to add a trajectory to the list of trajectories.
    """
    def __init__(self):
        self.solution = []

    def add_trajectory(self, trajectory):
        self.solution.append(trajectory)

    def calculate_solution_score(self, original_connection_dict):
        """Calculates the score of this schedule"""
        connection_set = set()
        duration = 0
        trajectory_amount = len(self.solution)

        for trajectory in self.solution:
            for connection in trajectory.connection_list:
                if connection.start_station + '-' + connection.end_station in original_connection_dict:
                    connection_key = f"{connection.start_station}-{connection.end_station}"
                    connection_set.add(connection_key)
                duration += connection.duration
        connections = len(connection_set)

        return calculate_score(connections, trajectory_amount,
            duration, total_connections = 28)

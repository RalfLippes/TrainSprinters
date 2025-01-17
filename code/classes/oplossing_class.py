

class Solution:
    """
    Initializes a solution which will store trajectory objects. Contains a function
    to add a trajectory to the list of trajectories.
    """
    def __init__(self):
        self.solution = []

    def add_trajectory(self, trajectory):
        self.solution.append(trajectory)

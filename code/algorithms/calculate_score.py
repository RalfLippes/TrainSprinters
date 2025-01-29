
def calculate_score(connections, trajectory_amount, duration, total_connections):
    """
    Calculates the quality of the itinerary. Outputs an integer score.
    """
    p = connections / total_connections
    return p * 10000 - (trajectory_amount * 100 + duration)

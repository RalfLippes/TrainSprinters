import pandas as pd
import math
import random
import copy
from code.classes.traject_class import Trajectory
"""
Algorithm that tries to minimize the distance between the current station and
the station where a connection begins that has not been ridden yet using
simulated annealing. Punishes riding connections that have already been ridden.
"""

def load_station_location_data(station_locations):
    """
    Uses a station csv file to create a dictionary of stations with their
    coordinates as values.
    """
    stations = pd.read_csv(station_locations)
    coordinates_stations = {}

    for index, row in stations.iterrows():
        #save the name of the station name and its coordinates in a dictionary
        coordinates_stations[row.iloc[0]]= [row.iloc[1], row.iloc[2]]

    return coordinates_stations

def annealing_cost_function(coordinates_stations, current_station, step_station,
    destination, full_connection_dict, penalty_weight, total_duration, max_duration):
    """
    Calculates the cost of riding a connection. Checks the distance, and penalizes
    for the duration of the connection.
    Cost function is euclidean distance + penalty weight * 1 if connection has
    already been ridden and    distance + penalty weight * 0 if connection is still
    needed. Returns the cost.
    """
    # check if total duration goes over max duration
    if total_duration + full_connection_dict[current_station + '-' + step_station].duration > max_duration:
        return math.inf

    # get both station objects
    station_1 = coordinates_stations[step_station]
    station_2 = coordinates_stations[destination]

    # calculate euclidean distance
    euclidean_distance = math.sqrt((station_2.x - station_1.x) ** 2 + (station_2.y - station_1.y) ** 2)

    duration = full_connection_dict[current_station + '-' + step_station].duration

    # calculate outcome of cost function
    cost = euclidean_distance + penalty_weight * duration

    return cost

def accept_solution(old_cost, new_cost, temperature):
    """
    Takes the cost of the old step and the cost of the new step, as well as the
    current temperature. Decides if the new step will be accepted by using the
    simulated annealing criterion. Returns true or false according to acceptance.
    """
    cost_difference = new_cost - old_cost

    # if new solution is better, always accept
    if cost_difference < 0:
        return True

    # if the new solution is worse, accept with a probability
    else:
        # Calculate the acceptance criterion
        criterion = math.exp(-cost_difference / temperature)

        # accept only if criterion is larger than random number between 0-1
        return random.random() < criterion

def find_nearest_connection(coordinates_stations, current_station, needed_connections_dict):
    """
    Finds the nearest connection in needed_connections_dict hat has not been ridden.
    Uses current station to calculate distances. Returns the closest 'new' connection
    as an object.
    """
    x1, y1 = current_station.x, current_station.y
    closest_distance = math.inf
    closest_connection = None

    # check which needed connection is closest to current station
    for connection in needed_connections_dict:
        x2 = coordinates_stations[needed_connections_dict[connection].start_station].x
        y2 = coordinates_stations[needed_connections_dict[connection].start_station].y
        euclidean_distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # check if better than current best, then save distance and connection object
        if euclidean_distance < closest_distance:
            closest_distance = euclidean_distance
            closest_connection = needed_connections_dict[connection]

    return closest_connection

def trim_trajectory(trajectory, needed_connections_dict):
    """
    Trims the trajectory list by removing all connections after the last one
    that exists in needed_connections_dict.
    Takes a trajectory list of connection objects and a dictionary with
    'station1-station2' as keys and connection objects as values. Returns list of
    trimmed connection objects.
    """
    last_valid_index = -1
    # iterate backwards through the trajectory to find the last valid connection
    for index in range(len(trajectory.connection_list) - 1, -1, -1):
        connection = trajectory.connection_list[index]
        key = f"{connection.start_station}-{connection.end_station}"

        if key in needed_connections_dict:
            # keep track of the last valid index
            last_valid_index = index
            break

    if last_valid_index != -1:
        trajectory.keep_connections(last_valid_index)

    return trajectory

def create_annealing_steps_trajectory(coordinates_stations, needed_connections_dict,
    possible_connections_dict, full_connection_dict, penalty_weight, max_duration, max_connections):
    """
    Creates a trajectory using simulated annealing.
    """
    total_duration = 0
    trajectory = Trajectory()
    new_needed_connections_dict = copy.deepcopy(needed_connections_dict)
    temperature = max_connections

    # choose first connection at random and add information to the list
    current_connection = needed_connections_dict[random.choice(list(new_needed_connections_dict))]
    trajectory.add_connection(current_connection)
    total_duration += current_connection.duration
    current_station = coordinates_stations[current_connection.end_station]
    new_needed_connections_dict.pop(current_connection.start_station + '-' + current_connection.end_station)

    # repeat until the trajectory is complete (temperature is 0)
    while temperature != 0 and len(new_needed_connections_dict) > 0:
        nearest_connection = find_nearest_connection(coordinates_stations,
            current_station, new_needed_connections_dict)
        at_destination = False

        # if not, loop this until we are at the nearest connection
        while not at_destination:
            possible_connections = possible_connections_dict[current_station.name]

            # check if the current station is already at the start of the nearest connection
            if current_station.name == nearest_connection.start_station:
                # if it is, directly add that connection
                if total_duration + nearest_connection.duration <= 120:
                    total_duration += nearest_connection.duration
                    new_needed_connections_dict.pop(current_station.name + '-' + nearest_connection.end_station)
                    current_station = coordinates_stations[nearest_connection.end_station]
                    current_connection = nearest_connection
                    if not trajectory.connection_list or trajectory.connection_list[-1].end_station != nearest_connection.end_station:
                        trajectory.add_connection(nearest_connection)

                    # we are at the destination and temperature can be decreased
                    at_destination = True
                    temperature -= 1
                    break

                # if this goes over time limit, stop searching
                else:
                    return trajectory, new_needed_connections_dict

            # check if a direct connection to nearest connection start station is possible
            connection_key = current_station.name + '-' + nearest_connection.start_station
            if connection_key in full_connection_dict:
                # update current station and connection if we can get there on time
                if total_duration + full_connection_dict[connection_key].duration <= 120:
                    total_duration += full_connection_dict[connection_key].duration
                    if connection_key in new_needed_connections_dict:
                        new_needed_connections_dict.pop(connection_key)
                    current_station = coordinates_stations[nearest_connection.start_station]
                    current_connection = full_connection_dict[connection_key] # Use the correct connection object
                    trajectory.add_connection(current_connection)

                    # we are at destination, temperature can be decreased
                    at_destination = True
                    temperature -= 1
                    break

                # if this goes over time limit, stop searching
                else:
                    return trajectory, new_needed_connections_dict

            # variable to check if any routes are accepted
            accepted_any = False

            # if we need to travel further, shuffle possible connections and loop over them
            random.shuffle(possible_connections)

            for random_station in possible_connections:
                if random_station == current_station.name:
                    continue

                # ensure connection exists before getting cost
                connection_key = current_station.name + '-' + random_station
                if connection_key not in full_connection_dict:
                    continue

                # calculate costs of current station and given step
                current_cost = annealing_cost_function(coordinates_stations,
                    current_connection.start_station, current_station.name,
                    nearest_connection.start_station, full_connection_dict,
                    penalty_weight, total_duration, max_duration)
                station_cost = annealing_cost_function(coordinates_stations,
                    current_station.name, random_station,
                    nearest_connection.start_station, full_connection_dict,
                    penalty_weight, total_duration, max_duration)

                # check if new step will be accepted
                if temperature == 0:
                    acceptance = False
                else:
                    acceptance = accept_solution(current_cost, station_cost, temperature)

                # continue if it is not accepted
                if not acceptance:
                    continue

                accepted_any = True

                # if accepted check duration and add all relevant info to the variables
                connection_to_add = full_connection_dict[connection_key]

                if total_duration + connection_to_add.duration <= 120:
                    total_duration += connection_to_add.duration
                    if connection_key in new_needed_connections_dict:
                        new_needed_connections_dict.pop(connection_key)

                    # update current station and connection
                    current_station = coordinates_stations[random_station]
                    current_connection = connection_to_add

                    # add connection and reduce temperature
                    trajectory.add_connection(connection_to_add)
                    temperature -= 1

                break
            # if no connections were accepted, trajectory is done
            if not accepted_any:
                temperature = 0
                break

    # remove stations after last needed station (since those aren't necessary)
    trajectory = trim_trajectory(trajectory, needed_connections_dict)

    return trajectory, new_needed_connections_dict

def create_dataframe_annealing(trajectories, trajectory_amount,
    needed_connections_dict, total_connections = 28):

    # create empty dataframe to store data in
    dataframe = pd.DataFrame(columns=['train', 'stations'])
    total_duration = 0
    row_index = 0

    # create right amount of trajectories
    for trajectory in trajectories:
        #trajectory = object.connection_list
        station_list = []
        iteration = 0

        # skip iteration if trajectory is empty
        if len(trajectory.connection_list) == 0:
            continue

        # make list of stations from objects in list
        for iteration, item in enumerate(trajectory.connection_list):

            # append start and end station for first station in trajectory
            if iteration == 0:
                station_list.append(item.start_station)
                station_list.append(item.end_station)

            # otherwise add only end station
            else:
                station_list.append(item.end_station)

            # add duration of connection to total
            total_duration += item.duration

            iteration += 1

        # fill in dataframe with correct data
        stations_string = f"[{', '.join(station_list)}]"
        dataframe.loc[row_index, 'stations'] = stations_string
        dataframe.loc[row_index, 'train'] = 'train_' + str(row_index + 1)

        row_index += 1

    # calculate the number of original connections ridden
    connection_number = total_connections - len(needed_connections_dict)

    # calculate itinerary score and put into dataframe
    score = calculate_score(connection_number, trajectory_amount, total_duration, total_connections)
    dataframe.loc[row_index, 'train'] = 'score'
    dataframe.loc[row_index, 'stations'] = score

    return dataframe, connection_number

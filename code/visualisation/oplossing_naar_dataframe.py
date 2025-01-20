import pandas as pd

def create_dataframe_from_solution(solution, original_connection_dict):
    """
    Creates dataframe in correct format from solution object.
    """
    score = solution.calculate_solution_score(original_connection_dict)
    dataframe = pd.DataFrame(columns = ['train', 'stations'])
    row_index = 0

    for trajectory in solution.solution:
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

            iteration += 1

        # fill in dataframe with correct data
        stations_string = f"[{', '.join(station_list)}]"
        dataframe.loc[row_index, 'stations'] = stations_string
        dataframe.loc[row_index, 'train'] = 'train_' + str(row_index + 1)

        row_index += 1

    dataframe.loc[row_index, 'train'] = 'score'
    dataframe.loc[row_index, 'stations'] = score

    return dataframe

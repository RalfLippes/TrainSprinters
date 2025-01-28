import argparse

def create_arg_parser():
    """Creates and configures the argument parser."""
    parser = argparse.ArgumentParser(
        description = "Runs schedule optimization algorithms."
    )

    # Positional argument for data
    parser.add_argument(
        "holland_nationaal",
        choices = ["holland", "nationaal"],
        help = "Use data from 'holland' (Noord- and Zuid-Holland) or 'nationaal'.",
    )

    # Optional argument for algorithm
    parser.add_argument(
        "run_algorithm",
        choices = ["baseline", "simulated_annealing", "annealing_steps", "greedy", "n_deep",
            "hill_climber","hill_climber2", "temp_cool", "find_iteration"],
        default = "baseline",
        help = "The algorithm to run (default: simulated_annealing).",
    )

    # Optional argument for time limit
    parser.add_argument(
        "--time",
        type = float,
        default=60.0,  # Default time of 60 seconds
        help = "Time limit for the algorithm in seconds (default: 60).",
    )

    # Optional flag for plotting
    parser.add_argument(
        "--plot_scores",
        action = "store_true",
        help = "Enable plotting of the found scores.",
    )

    # optional arguments for algorithms
    parser.add_argument(
        "--hill_climber_args",
        choices = ["greedy", "baseline", "annealing_steps"],
        help = "What algorithm to use for starting hill climber",
    )

    return parser

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="laundromatic",
        description="Find the best outdoor clothes-drying window based on the weather forecast.",
    )

    location = parser.add_argument_group("Location")
    location.add_argument(
        "--location",
        type=str,
        default=None,
        help="Location name (e.g. 'London'). Overrides lat/lon if provided.",
    )
    location.add_argument("--lat", type=float, default=51.51, help="Latitude. Default: 51.51.")
    location.add_argument("--lon", type=float, default=0.13, help="Longitude. Default: 0.13.")

    model = parser.add_argument_group("Drying model options")
    model.add_argument("--days", type=int, default=7, help="Forecast duration (days, 1-16). Default: 7.")
    model.add_argument(
        "--latest-end-hour",
        type=int,
        default=20,
        help="Latest acceptable finish time (hour, 0–23). Default: 20.",
    )
    model.add_argument(
        "--earliest-start-hour",
        type=int,
        default=8,
        help="Earliest acceptable start time (hour, 0–23). Default: 8.",
    )
    model.add_argument(
        "--required-drying",
        type=float,
        default=1.0,
        help="Target drying level (default: 1.0, fully dry).",
    )
    model.add_argument(
        "--precipitation-probability-threshold",
        type=float,
        default=0.2,
        help="Maximum precipitation probability for an hour to be considered 'dry'. Default: 0.2.",
    )
    model.add_argument(
        "--max-duration-hours",
        type=int,
        default=8,
        help="Maximum window length in hours. Default: 8.",
    )

    output = parser.add_argument_group("Output options")
    output.add_argument(
        "--show-all",
        action="store_true",
        help="Show all eligible drying windows",
    )

    args, _ = parser.parse_known_args()
    return args
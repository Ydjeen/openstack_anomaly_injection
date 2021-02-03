import argparse

# Sub-anomaly arguments
default_args = argparse.ArgumentParser(add_help=False)
default_args.add_argument("-t", "--duration", help="Duration of the anomaly. Eg. [1s, 10m, 2h]", type=str,
                          required=True, dest="param_duration")
default_args.add_argument("-d", "--delay", dest="param_delay",
                          help="Wait before injecting anomaly. Eg. [1s, 10m, 2h]", type=str)
default_args.add_argument('--config-path', help='Path to config file', metavar='[path]',
                          dest="config_path", action='store')
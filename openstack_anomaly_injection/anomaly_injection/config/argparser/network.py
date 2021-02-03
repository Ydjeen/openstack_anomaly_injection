import argparse
from .default import default_args

# Network Parser
network_parser = argparse.ArgumentParser(add_help=False, parents=[default_args])


sub_net_p = network_parser.add_subparsers(dest="anomaly_name")

# define new anomalies here


# define params for anomalies here

import argparse
from .default import default_args

# Network Parser
network_parser = argparse.ArgumentParser(add_help=False)

sub_net_p = network_parser.add_subparsers(dest="anomaly_name")

# define new anomalies here
tc_anom = sub_net_p.add_parser("tc", parents=[default_args])

tc_anom.add_argument("--tcconfig", dest="param_tcconfig", type=str, required=True,
                     help="String containing tcconfig params. "
                          "Eg. \"eth0 --rate 100Kbps\". Ignore the \"tcset\" command as it is"
                          "implemented along with the \"tcdel\" command. ")
# define params for anomalies here

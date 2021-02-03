import argparse
from .default import default_args

system_parser = argparse.ArgumentParser(add_help=False)
sub_sys_p = system_parser.add_subparsers(dest="anomaly_name")

# define new anomalies here
# <var_name> = sub_sys_p.add_parser(<anomaly_name>, parents=[sub_a_args])

pause_anom = sub_sys_p.add_parser("pause", parents=[default_args])

# define params for anomalies here
# <var_name>.add_argument()

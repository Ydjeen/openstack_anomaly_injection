import argparse
from .default import default_args

# Stress Parser
stress_parser = argparse.ArgumentParser(add_help=False)
sub_stress = stress_parser.add_subparsers(dest="anomaly_name")

# define new anomalies here
# <var_name> = sub_sys_p.add_parser(<anomaly_name>, parents=[default_args])
stress_ng_anom = sub_stress.add_parser("stress-ng", parents=[default_args])

# define params for anomalies here
# <var_name>.add_argument()
stress_ng_anom.add_argument("--stressors", type=str, required=True, dest="param_stressors",
                            help="String containing stress-ng params. "
                                 "Eg. \"--cpu 2\". Avoid using '-t' in the stressors string. Instead use the duration"
                                 " parameter of the anomaly to specify duration ")

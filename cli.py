import argparse
import json
import anomaly_injection.node_control.config.argparser as node_argparser
import anomaly_injection.config.argparser.argparser as anomaly_argparser
from anomaly_injection.main import main as run_anomaly
from anomaly_injection.node_control.main import main as run_admin

# Main parser
# Anomaly commands
conf_file_parser = argparse.ArgumentParser(add_help=False)
conf_file_parser.add_argument('--config_file', help='Path to config file', metavar='[path]',
                              dest="config_file")

parser = argparse.ArgumentParser(description='Chaos toolkit', parents=[conf_file_parser])

# Main subparsers
main_commands = parser.add_subparsers(help='Desired action to perform', dest='action')
admin = node_argparser.get_parser(main_commands)
anomaly_inject = anomaly_argparser.get_parser(main_commands)

if __name__ == "__main__":
    args = parser.parse_args()
    if not args.target:
        parser.print_help()
    else:
        if args.action == 'admin':
            run_admin(args)
        else:
            run_anomaly(args)

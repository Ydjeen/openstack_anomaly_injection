import argparse
import json
import sys
import anomaly_injection.node_control.config.argparser as node_argparser
import anomaly_injection.config.argparser.argparser as anomaly_argparser
from anomaly_injection.main import main as run_anomaly
from anomaly_injection.node_control.main import main as run_admin
from anomaly_injection.config.loggers import log_info, set_debug

# Main parser
# Anomaly commands
conf_file_parser = argparse.ArgumentParser(add_help=False)
conf_file_parser.add_argument('--config_file', help='Path to config file', metavar='[path]',
                              dest="config_file")

parser = argparse.ArgumentParser(description='Chaos toolkit', parents=[conf_file_parser])

parser.add_argument("--debug", help="Run command in debug mode", dest="debug", action='store_true')
# Main subparsers
main_commands = parser.add_subparsers(help='Desired action to perform', dest='action')
admin = node_argparser.get_parser(main_commands)
anomaly_inject = anomaly_argparser.get_parser(main_commands)


def main():
    args = parser.parse_args()

    _debug = args.debug or False
    set_debug(_debug)

    _action = vars(args).get("action")
    if not _action:
        parser.print_help()
    else:
        try:
            if args.action == 'admin':
                run_admin(args)
            else:
                run_anomaly(args)
        except Exception as e:
            log_info.info(e)
            sys.exit(e)


if __name__ == "__main__":
    main()

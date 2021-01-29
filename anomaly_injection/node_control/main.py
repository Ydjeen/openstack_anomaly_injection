import sys
from .connection import CloudConnection
from .config import get_parser, parse_arguments, cfg_path
import json
from .config.loggers import log_info, set_debug


def main(args):
    _debug = args.debug or False
    print(_debug)
    set_debug(_debug)

    path = vars(args).get('config_path', None)
    if not path:
        path = f"{cfg_path}/cloud_config.json"
    cfg = json.load(open(path, 'r'))
    if not args.target:
        get_parser().print_help()
    else:
        try:
            args = parse_arguments(args)
            conn = CloudConnection(cfg)
            result = conn.perform_action(args['action'], args['target'])
            sys.exit(result)
        except Exception as e:
            log_info.info(e)
            sys.exit(e)

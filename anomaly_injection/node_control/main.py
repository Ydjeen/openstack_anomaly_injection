from .connection import CloudConnection
from .config import get_parser, parse_arguments, cfg_path
from .config.loggers import log_info
import json


def main(args):
    path = vars(args).get('config_path', None)
    if not path:
        path = f"{cfg_path}/cloud_config.json"
    cfg = json.load(open(path, 'r'))
    args = parse_arguments(args)
    conn = CloudConnection(cfg)
    result = conn.perform_action(args['action'], args['target'])
    print(result)

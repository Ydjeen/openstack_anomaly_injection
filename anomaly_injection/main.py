from .config import get_parser, parse_arguments, cfg_path
import json
from .injector import AnomalyInjector

parser = get_parser()


def main(args):
    path = vars(args).get('config_path', None)
    if not path:
        path = f"{cfg_path}/cloud_config.json"
    cfg = json.load(open(path, 'r'))
    args = parse_arguments(args)
    injector = AnomalyInjector(cfg, args)
    injector.run()

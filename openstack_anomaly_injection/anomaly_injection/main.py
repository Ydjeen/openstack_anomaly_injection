from .config import get_parser, parse_arguments, cfg_path
import json
import traceback
import sys
from .injector import AnomalyInjector
from .config.loggers import log_info, log_debug, set_debug

parser = get_parser()


def main(args):
    _debug = args.debug or False
    set_debug(_debug)
    path = vars(args).get('config_file', None)
    if not path:
        path = f"{cfg_path}/cloud_config.json"
    cfg = json.load(open(path, 'r'))
    if not args.target:
        get_parser().print_help()
    else:
        try:
            args = parse_arguments(args)
            injector = AnomalyInjector(cfg, args)
            injector.run()
        except Exception as e:
            if _debug:
                log_debug.debug(traceback.format_exc())
            log_info.info(e)
            sys.exit(e)

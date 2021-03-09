import argparse

import logging

log_debug = logging.getLogger("debugLog")

_available_commands = ["list"]


def get_parser(parent=None):
    # Anomaly commands
    conf_file_parser = argparse.ArgumentParser(add_help=False)
    conf_file_parser.add_argument('--config_file', '--config_path', help='Path to config file', metavar='[path]',
                                  dest="config_file")

    if not parent:
        admin = argparse.ArgumentParser(description='Deployment control', prog='deployment control',
                                        parents=[conf_file_parser])
        admin.add_argument("--debug", help="Run command in debug mode", dest="debug", action='store_true')

    else:
        admin = parent.add_parser('admin', help='Deployment control')

    # Admin commands
    admin_parser = argparse.ArgumentParser(add_help=False)
    admin_parser.add_argument("list", help="List %(prog)ss")
    admin_parser.add_argument('--host', help='Hostname or ip of target', metavar='[hostname]',
                              dest='target_host', default='all')
    admin_parser.add_argument('--config-path', help='Path to config file', metavar='[path]',
                              dest="config_path", action='store')
    # add more admin commands here

    # Admin parser
    admin_subcommands = admin.add_subparsers(dest="target")
    admin_container = admin_subcommands.add_parser('container', prog='Container', parents=[admin_parser])
    admin_node = admin_subcommands.add_parser('node', prog='Node', parents=[admin_parser])
    admin_network = admin_subcommands.add_parser('network', prog='Network', parents=[admin_parser])
    admin_network.add_argument('--interface', help='Name of interface', type=str, metavar='[NAME]',
                               dest="target_interface")

    admin_deployment = admin_subcommands.add_parser('deployment', prog='Deployment', parents=[admin_parser])

    if parent:
        return parent
    else:
        return admin


def parse_arguments(args):
    args = vars(args)
    unpacked = unpack_targets(args)
    unpacked.update(unpack_params(args))
    log_debug.debug("Unpacked arguments" + str(unpacked))
    return unpacked


def unpack_targets(args):
    _unpacked = dict()
    for arg in args:
        if "target" in arg and args[arg]:
            param_split = arg.split("_")
            if len(param_split) > 1:
                _unpacked[param_split[1]] = args[arg]
            else:
                _unpacked[arg] = args[arg]
    return {"target": _unpacked}


def unpack_params(args):
    _unpacked = dict()
    for arg in args:
        if arg in _available_commands:
            return {"action": arg}

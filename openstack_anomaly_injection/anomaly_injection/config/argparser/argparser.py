import argparse
import logging
from .system import system_parser
from .network import network_parser
from .stress import stress_parser

log_debug = logging.getLogger("debugLog")


def get_parser(parent=None):
    # connection with main parser
    if not parent:
        anomaly_inject = argparse.ArgumentParser(description='Anomaly Injection', prog='anomaly')
        anomaly_inject.add_argument("--debug", help="Run command in debug mode", dest="debug", action='store_true')

    else:
        anomaly_inject = parent.add_parser('anomaly', help='Anomaly Injection')

    # Anomaly commands
    anomaly_parser = argparse.ArgumentParser(add_help=False)
    anomaly_parser.add_argument('--host', help='Hostname or ip of target', metavar='[hostname]', dest="target_host")

    # Anomaly parsers
    anomaly_subcommands = anomaly_inject.add_subparsers(dest="target")
    anomaly_container = anomaly_subcommands.add_parser('container', prog='container',
                                                       parents=[anomaly_parser],
                                                       usage=f"{anomaly_inject.prog} %(prog)s",
                                                       description="Container anomaly injector, "
                                                                   "must specify host and name or id")

    anomaly_node = anomaly_subcommands.add_parser('node', prog='node', usage=f"{anomaly_inject.prog} %(prog)s",
                                                  parents=[anomaly_parser],
                                                  description="Node anomaly injector, "
                                                              "must specify host and name or id")

    anomaly_network = anomaly_subcommands.add_parser('network', prog='network', usage=f"{anomaly_inject.prog} %(prog)s",
                                                     parents=[anomaly_parser],
                                                     description="Network anomaly injector, "
                                                                 "must specify host and name or id")

    anomaly_deployment = anomaly_subcommands.add_parser('deployment', prog='deployment',
                                                        usage=f"{anomaly_inject.prog} %(prog)s",
                                                        parents=[anomaly_parser],
                                                        description="Deployment anomaly injector, "
                                                                    "must specify host and name or id")

    # Container Anomaly
    a_c_group = anomaly_container.add_mutually_exclusive_group(required=True)
    a_c_group.add_argument('--name', '-n', help='Name of container', type=str, metavar='[name]', dest="target_name")
    a_c_group.add_argument('--id', help='Container ID', type=str, metavar='[id]', dest="target_id")
    cont_anomalies = anomaly_container.add_subparsers(dest="anomaly_type")
    cont_system = cont_anomalies.add_parser("system", parents=[system_parser])
    cont_net = cont_anomalies.add_parser("network", parents=[network_parser])
    cont_stress = cont_anomalies.add_parser("stress", parents=[stress_parser])

    # Node Anomaly
    node_anomalies = anomaly_node.add_subparsers(dest="anomaly_type")
    node_system = node_anomalies.add_parser("system", parents=[system_parser])
    node_net = node_anomalies.add_parser("network", parents=[network_parser])
    node_stress = node_anomalies.add_parser("stress", parents=[stress_parser], )

    # Deployment Anomaly
    dep_anomalies = anomaly_deployment.add_subparsers(dest="anomaly_type")
    dep_system = dep_anomalies.add_parser("system", parents=[system_parser])
    dep_stress = dep_anomalies.add_parser("stress", parents=[stress_parser])
    dep_net = dep_anomalies.add_parser("network", parents=[network_parser])

    # Network Anomaly
    net_anomalies = anomaly_network.add_subparsers()
    net_stress = net_anomalies.add_parser("stress", parents=[stress_parser])
    net_system = net_anomalies.add_parser("system", parents=[network_parser])
    net_net = net_anomalies.add_parser("network", parents=[system_parser])

    if parent:
        return parent
    else:
        return anomaly_inject


def parse_arguments(args):
    args = vars(args)
    unpacked = unpack_targets(args)
    unpacked.update(unpack_params(args))
    unpacked['name'] = args.get('anomaly_name', args['anomaly_type'])
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
        if "param" in arg and args[arg]:
            param_split = arg.split("_")
            if len(param_split) > 1:
                _unpacked[param_split[1]] = args[arg]
            else:
                _unpacked[arg] = args[arg]
    return {"params": _unpacked}

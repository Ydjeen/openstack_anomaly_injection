from rally.common import logging
from rally import consts
from rally.task import hook
import os
import sys
import json

sys.path.append(os.getcwd())

from anomaly_injection.injector import AnomalyInjector
from anomaly_injection.config.loggers import log_info, log_debug


@hook.configure(name="fault_injection")
class FaultInjectionHook(hook.HookAction):
    """Performs fault injection."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "target":
                {"type": "object",
                 "properties":
                     {
                         "target": {"type": "string"},
                         "host": {"type": "string"},
                         "id": {"type": "string"},
                         "name": {"type": "string"},
                         "interface": {"type": "string"}

                     }
                 },
            "params": {
                "type": "object",
                "properties": {
                    "duration": {"type": "string"},
                }
            },
            "anomaly": {
                "type": "string",

            },
            "config": {
                "type": "object",
                "properties": {
                    "ansible": {
                        "type": "object",
                        "properties": {
                            "ansible_user": {
                                "type": "string"
                            },
                            "private_key_file": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "ansible_user",
                            "private_key_file"
                        ]
                    },
                    "hosts": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 1,
                        "uniqueItems": True
                    }
                },
                "required": [
                    "ansible",
                    "hosts"
                ]
            }
        }

    }

    def run(self):

        log_debug.debug("Injecting fault: %s" + str(self.config))
        try:
            from anomaly_injection.config.loggers import set_debug
            _debug = self.config.get('debug', False)
            set_debug(_debug)

            cfg = self._init_cfg(self.config)
            self.config['name'] = self.config['anomaly']

            injector = AnomalyInjector(cfg, self.config)
            injector.run()

            self.set_status(consts.HookStatus.SUCCESS)
        except Exception as e:
            import traceback
            self.set_status(consts.HookStatus.FAILED)
            self.set_error(exception_name=type(e),
                           description='Fault injection failure',
                           details=str(e))

    def _init_cfg(self, args):
        cfg = args.get("config", None)
        if not cfg:
            from anomaly_injection.config import cfg_path
            path = args.get('config_path', None)
            if not path:
                path = f"{cfg_path}/cloud_config.json"
            cfg = json.load(open(path, 'r'))
        else:
            cfg = json.loads(str(cfg))
        return cfg

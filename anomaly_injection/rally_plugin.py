from rally.common import logging
from rally import consts
from rally.task import hook
import os
import sys
import json

sys.path.append(os.getcwd())

from anomaly_injection.injector import AnomalyInjector
from anomaly_injection.config.loggers import log_info, log_debug


@hook.configure(name="fault_injection2")
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
                         "name": {"type": "string"}

                     }
                 },
            "params": {
                "type": "object",
                "properties": {
                    "duration": {"type": "string"},
                }
            },
            "name": {
                "type": "string",

            }

        }}

    def run(self):

        log_debug.debug("Injecting fault: %s" + str(self.config))
        try:
            from anomaly_injection.config import cfg_path
            log_debug.debug(type(self.config))
            path = self.config.get('config_path', None)
            if not path:
                path = f"{cfg_path}/cloud_config.json"

            cfg = json.load(open(path, 'r'))

            injector = AnomalyInjector(cfg, self.config)

            injector.run()

            self.set_status(consts.HookStatus.SUCCESS)
        except Exception as e:
            self.set_status(consts.HookStatus.FAILED)
            self.set_error(exception_name=type(e),
                           description='Fault injection failure',
                           details=str(e))

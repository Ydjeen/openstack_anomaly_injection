from rally.common import logging
from rally import consts
from rally.task import hook

from .anomaly_injection.injector import AnomalyInjector
from .anomaly_injection.config.loggers import log_info, log_debug


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
                         "host": {"type": "string"},
                         "id": {"type": "string"},
                         "name": {"type": "string"}

                     }
                 },
            "stress": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "params": {"type": "object"}
                }
            },
            "network": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "params": {"type": "object"}
                }
            },
            "system": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "params": {"type": "object"}
                }
            },
        }}

    def run(self):

        log_debug.debug("Injecting fault: %s", self.config["action"])
        try:

            self.set_status(consts.HookStatus.SUCCESS)
        except Exception as e:
            self.set_status(consts.HookStatus.FAILED)
            self.set_error(exception_name=type(e),
                           description='Fault injection failure',
                           details=str(e))

from .AnomalyInjector import AnomalyInjector
from rally.common import logging
from rally import consts
from rally.task import hook

LOG = logging.getLogger(__name__)


@hook.configure(name="fault_injection")
class FaultInjectionHook(hook.Hook):
    """Performs fault injection."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "action": {"type": "string"},
        },
        "required": [
            "action",
        ],
        "additionalProperties": False,
    }

    def run(self):
        LOG.debug("Injecting fault: %s", self.config["action"])
        injector = AnomalyInjector(**self.config)

        try:
            injector.connect()
            injector.run()

            self.set_status(consts.HookStatus.SUCCESS)
        except Exception as e:
            self.set_status(consts.HookStatus.FAILED)
            self.set_error(exception_name=type(e),
                           description='Fault injection failure',
                           details=str(e))

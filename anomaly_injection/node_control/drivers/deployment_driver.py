import logging
from .base_driver import BaseDriver

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class DeploymentDriver(BaseDriver):
    pass

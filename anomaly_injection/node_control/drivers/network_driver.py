from .base_driver import BaseDriver
import logging

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')


class NetworkDriver(BaseDriver):
    pass

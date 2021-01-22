import logging.config
import os

DEBUG = True

if not os.path.isdir("logs"):
    os.makedirs("logs")
dir = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(os.path.join(dir, 'logs.ini'))
if not DEBUG:
    logging.Logger.manager.loggerDict['debuggerLog'].handlers.pop()
else:
    debug_fmt = logging.Logger.manager.loggerDict['debuggerLog'].handlers[-1].formatter
    logging.Logger.manager.loggerDict['infoLog'].handlers[-1].formatter = debug_fmt

log_info = logging.getLogger('infoLog')
log_error = logging.getLogger('errorLog')
log_debug = logging.getLogger('debuggerLog')
log_status = logging.getLogger('statusLog')
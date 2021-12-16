from datetime import datetime

#
# класс, использующийся для логгирования сообщений разного уровня (debug, info, error)
#


class Logger:
    def __init__(self, debug_enabled):
        self.debug_enabled = debug_enabled

    def log(self, prefix, msg, debug=False):
        if (not debug) or (debug and self.debug_enabled):
            self.print_formatted(prefix, msg)

    def debug(self, msg):
        self.log('DEBUG', msg, debug=True)

    def info(self, msg):
        self.log('INFO', msg)

    def error(self, msg):
        self.log('ERROR', msg)

    def print_formatted(self, prefix, msg):
        print(f'{datetime.now()}: [{prefix}] {msg}')

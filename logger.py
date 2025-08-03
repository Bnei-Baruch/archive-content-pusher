import logging


class Logger:
    def __init__(self):
        self._logger = logging.getLogger('wp-autpost')
        self._logger.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(module)s] - %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    @property
    def logger(self):
        return self._logger


import logging
import os
import datetime


class MyLogger:
    _logger = None

    def __new__(cls, *args, **kwargs):
        dirname = "./logs"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        if cls._logger is not None:
            return cls._logger
            
        cls._logger = logging.getLogger("archangel")
        logging.basicConfig(
            filename=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log',
            filemode='w',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )

        return cls._logger

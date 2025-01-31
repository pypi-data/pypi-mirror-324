import logging
import os
import re

def never_throw(f,*args,default=None,**kwargs):
    try:
        return f(*args,**kwargs)
    except:
        return default

class MyFormatter(logging.Formatter):
    log_format = 'Run %(run_number)s | %(asctime)s | %(filename)s:%(lineno)d:%(function)s | %(levelname)s | %(message)s'
    run_number=None
    def __init__(self):
        super().__init__(MyFormatter.log_format)

    def format(self, record):
        record.run_number = self.run_number
        record.filename = os.path.basename(record.pathname)
        record.function = record.funcName
        record.lineno = record.lineno
        return super().format(record)

#add logging to file 
def start_logging(log_file, console_log_level=logging.INFO):
    logger = logging.getLogger(__name__) 
    logger.setLevel(logging.DEBUG)  # Set the logger level to DEBUG
        # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # Create a file handler for all levels (including DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(MyFormatter())
    logger.addHandler(file_handler)
    logger.propagate = False 
    # Create a stream handler with configurable level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    #console_handler.setFormatter(MyFormatter())
    logger.addHandler(console_handler)
    
    last_run_number = 0
    if log_file and MyFormatter.run_number is None:
        if os.path.exists(log_file):
            for line in open(log_file):
                 last_run_number = max(last_run_number, never_throw(lambda: int(re.search('Run (\d+) \|', line).group(1)), default=0))

        last_run_number += 1
        MyFormatter.run_number = last_run_number
    return logger

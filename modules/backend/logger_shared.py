import logging
import os

logger = logging.getLogger("worker")
logger.setLevel("INFO")
logpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "flask.log"))

fh = logging.FileHandler(logpath, mode='a')
ch = logging.StreamHandler()

formatter = logging.Formatter(f"%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

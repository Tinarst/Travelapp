import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s-%(levelname)s-%(message)s",
    filename = "logs.log",
    filemode = "a"
)

logger = logging.getLogger()
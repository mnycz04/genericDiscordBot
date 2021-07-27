import configparser
import logging
import os

import praw

default_log_format = logging.Formatter(
    "[%(name)s - %(levelname)s - %(asctime)s]: %(message)s",
    datefmt="%a %d-%b-%Y %H:%M:%S")



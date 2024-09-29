import logging
import sys
from os import path, makedirs
from logging.handlers import RotatingFileHandler
from hashlib import md5


def check_direxists(fname):
    """ Checks if a given directory exists
    Return:
        True if directory exists, False if not"""
    if fname is None:
        return False
    if not path.exists(fname):
        return False
    return path.isdir(fname)


def check_fileexists(fname: str):
    """ Checks if a given file exists
    Return:
        True if file exists, False if not"""
    if fname is None:
        return False
    if not path.exists(fname):
        return False
    return path.isfile(fname)


def generate_file_md5(filename: str, blocksize=2**20):
    """Generate md5 checksum of file"""
    md = md5()
    memv = memoryview(bytearray(128*1024))
    with open(filename, 'rb', buffering=0) as file:
        for item in iter(lambda: file.readinto(memv), 0):
            md.update(memv[:item])
    return md.hexdigest()


def setup_logger():
    """ Create logger, it is important to note that prints are not written to the logfile! """
    cfd = path.dirname(path.realpath(__file__))
    log_folder = path.join(cfd, "logs")
    if not check_direxists(log_folder):
        makedirs(log_folder)

    log_file = log_folder + "/logs.txt"
    log_format = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    # Roratingfile handler: 1MB/logfile and keep last 2 files
    handlers = [RotatingFileHandler(log_file, 'a', 1000000, 1), logging.StreamHandler(sys.stdout)]#, logging.StreamHandler()
    logging.basicConfig(format=log_format, level=logging.INFO, handlers=handlers)

    with open(log_file, 'a') as f:
        f.write("\n\n")
        f.write("New session")
        f.write("\n\n")

# __init__.py


from twisted.python import log
from twisted.python import logfile


# TODO: upcase?
filename = "twistd.log"
directory = "."

daily = False

K = 1024
M = 1024 * K

rotate_size = 100 * M
max_files = 10


def logger():
    if daily:
        lf = logfile.DailyLogFile(filename, directory)
    else:
        lf = logfile.LogFile(filename, directory,
                             rotateLength=rotate_size,
                             maxRotatedFiles=max_files)

    observer = log.FileLogObserver(lf).emit
    return observer

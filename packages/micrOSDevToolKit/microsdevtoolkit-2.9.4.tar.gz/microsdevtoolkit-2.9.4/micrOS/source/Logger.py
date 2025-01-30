"""
Module is responsible for System and User logging
- built-in log rotation

Designed by Marcell Ban aka BxNxM
"""
from time import localtime
from os import listdir, remove
from re import match

#############################################
#        LOGGING WITH DATA ROTATION         #
#############################################


def logger(data, f_name, limit):
    """
    Create generic logger function
    - implements log line rotation
    - automatic time stump
    :param data: input string data to log
    :param f_name: file name to use
    :param limit: line limit for log rotation
    return write verdict - true / false
    INFO: hardcoded max data number = 30
    """
    def _logger(_data, _f_name, _limit, f_mode='r+'):
        _limit = 30 if _limit > 30 else _limit
        # [1] GET TIME STUMP
        ts_buff = [str(k) for k in localtime()]
        ts = ".".join(ts_buff[0:3]) + "-" + ":".join(ts_buff[3:6])
        # [2] OPEN FILE - WRITE DATA WITH TS
        with open(_f_name, f_mode) as f:
            _data = f"{ts} {_data}\n"
            # read file lines and filter by time stump chunks (hack for replace truncate)
            lines = [_l for _l in f.readlines() if '-' in _l and '.' in _l]
            # get file params
            lines_len = len(lines)
            lines.append(_data)
            f.seek(0)
            # line data rotate
            if lines_len >= _limit:
                lines = lines[-_limit:]
                lines_str = ''.join(lines)
            else:
                lines_str = ''.join(lines)
            # write file
            f.write(lines_str)

    # Run logger
    try:
        # There is file - append 'r+'
        _logger(data, f_name, limit)
    except:
        try:
            # There is no file - create 'a+'
            _logger(data, f_name, limit, 'a+')
        except:
            return False
    return True


def log_get(f_name, msgobj=None):
    """
    Get and stream (ver osocket/stdout) .log file's content and count "critical" errors
    - critical error tag in log line: [ERR]
    """
    err_cnt = 0
    try:
        if msgobj is not None:
            msgobj(f_name)
        with open(f_name, 'r') as f:
            eline = f.readline().strip()
            while eline:
                # GET error from log line (tag: [ERR])
                err_cnt += 1 if "[ERR]" in eline else 0
                # GIVE BACK .log file contents
                if msgobj is not None:
                    msgobj(f"\t{eline}")
                eline = f.readline().strip()
    except:
        pass
    return err_cnt


def syslog(data=None, msgobj=None):
    if data is None:
        err_cnt = sum([log_get(f, msgobj) for f in listdir() if f.endswith(".sys.log")])
        return err_cnt

    _match = match(r"^\[([^\[\]]+)\]", data)
    log_lvl = _match.group(1).lower() if _match else 'user'
    f_name = f"{log_lvl}.sys.log" if log_lvl in ("err", "warn", "boot") else 'user.sys.log'
    return logger(data, f_name, limit=4)


def log_clean(msgobj=None):
    to_del = [file for file in listdir() if file.endswith('.log')]
    for _del in to_del:
        if msgobj is not None:
            msgobj(f" Delete: {_del}")
        remove(_del)

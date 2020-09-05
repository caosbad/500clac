
import numpy as np
import time
from datetime import datetime

def compare_time(time1,time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
    if len(time2) > 11:
        e_time = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    else:
        e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))

    result =int(s_time) - int(e_time)
    return result

def nat_check(nat):
    return nat == np.datetime64('NaT')

def convert_date(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    date_str = date.strftime('%Y-%m-%d')
    return date_str


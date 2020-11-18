
import numpy as np
import time
# from datetime import datetime
from datetime import date, timedelta, datetime

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

def stringfy_date(date):
    return date.strftime('%Y-%m-%d')

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def iter_weekday(start, end, weekday=2):
    '''Yield all of a particular weekday in a date range.'''
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    date = start + timedelta((weekday - start.weekday()) % 7)
    while date < end:
        yield date
        date += timedelta(7)
    return date

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


def addDay(d):
    d = datetime.strptime(d, '%Y-%m-%d')
    return stringfy_date(d + timedelta(days=1))

def getDateRange(file):
    map = {
        '2007-07-01':'2006-07-03*2007-07-02',
        '2008-01-01':'2007-01-04*2008-01-02',
        '2008-06-30':'2007-07-02*2008-07-01',
        '2009-01-04':'2008-01-07*2009-01-05',
        '2009-06-30':'2008-07-01*2009-07-01',
        '2010-01-03':'2009-01-05*2010-01-04',
        '2010-06-30':'2009-07-01*2010-07-01',
        '2011-01-03':'2010-07-01*2011-01-04',
        '2011-06-30':'2010-07-01*2011-07-01',
        '2012-01-03':'2011-01-04*2012-01-04',
        '2012-07-01':'2011-07-04*2012-07-02',
        '2013-01-03':'2012-01-04*2013-01-04',
        '2013-06-30':'2012-07-02*2013-07-01',
        '2013-12-15':'2012-12-17*2013-12-16',
        '2014-06-15':'2013-06-17*2014-06-16',
        '2014-12-14':'2013-12-16*2014-12-15',
        '2015-06-14':'2014-06-16*2015-06-15',
        '2015-12-13':'2014-12-15*2015-12-14',
        '2016-06-12':'2015-06-15*2016-06-13',
        '2016-12-11':'2015-12-14*2016-12-12',
        '2017-06-11':'2016-06-13*2017-06-12',
        '2017-12-10':'2016-12-12*2017-12-11',
        '2018-06-10':'2017-06-12*2018-06-11',
        '2018-12-16':'2017-12-18*2018-12-17',
        '2019-06-16':'2018-06-19*2019-06-17',
        '2019-12-15':'2018-12-17*2019-12-16',
        '2020-06-14':'2019-0617*2020-06-15'
    }

    return map[file]
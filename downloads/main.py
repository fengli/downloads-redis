from datetime import timedelta, datetime

import pytz
from pytz import timezone

import redis


class Download (object):
    def __init__ (self, modelname='item', redisaddr="localhost", db=5, cache=True):
        self.r = redis.StrictRedis (redisaddr, db=db)
        self.cache = cache
        self.modelname = modelname

    def incr (self, pk):
        self._incr (pk, today ())

    def delete_all_keys (self):
        for key in self.r.keys ('%s:downloads:*'%self.modelname ):
            self.r.delete (key)

    def most_downloads_today (self, n=50):
        items = self.r.zrevrange (self.today_key (), 0, n-1, withscores=True)
        return items

    def most_downloads_all_time (self, n=50):
        items = self.r.zrevrange (self.all_time_period_key(), 0, n-1, withscores=True)
        return items

    def most_downloads_in_past_week (self, n=50):
        return self.most_downloads_in_date_range (ndays_later(-6), ndays_later (1), n)

    def most_downloads_in_past_month (self, n=50):
        return self.most_downloads_in_date_range (ndays_later(-30), ndays_later (1), n)

    def most_downloads_in_past_week_complex (self, n=50):
        downloads = self.most_downloads_in_date_range (ndays_later(-6), ndays_later (1), n)
        pks = zip (*downloads)[0]
        history_7_days = [self.recent_history_in_past_week (pk) for pk in pks]
        return zip (zip(*downloads)[0], zip(*downloads)[1], history_7_days)
    
    def most_downloads_in_past_month_complex (self, n=50):
        downloads = self.most_downloads_in_date_range (ndays_later(-30), ndays_later (1), n)
        pks = zip (*downloads)[0]
        history_7_days = [self.recent_history_in_past_week (pk) for pk in pks]
        return zip (zip(*downloads)[0], zip(*downloads)[1], history_7_days)

    def recent_history_in_past_week (self, pk):
        return self.recent_history_in_time_period (pk, ndays_later (-6), ndays_later (1))

    def recent_history_in_time_period (self, pk, start, end):
        dates = date_range (start, end)
        dates = [date.strftime ("%Y-%m-%d") for date in dates]
        return zip (dates, self.r.hmget (self.history_key (pk), dates))
    
    def most_downloads_in_date_range (self, start, end, n=50):
        date_range_k = self.date_range_key (start, end)
        if self.cache and self.r.exists (date_range_k):
            return self.r.zrevrange (date_range_k, 0, n-1, withscores=True)
        dates = date_range (start, end)
        datekeys = map (self.date_key, dates)
        self.r.zunionstore (date_range_k, datekeys)
        self.r.expire (date_range_k, 5*60)
        return self.r.zrevrange (date_range_k, 0, n-1, withscores=True)
    
    def item_key (self, pk):
        return '%s:downloads:item:%s'% (self.modelname, pk)

    def date_key (self, date):
        return '%s:downloads:date:%s' % (self.modelname, date.strftime ("%Y-%m-%d"))

    def today_key (self):
        return self.date_key (today ())

    def history_key (self, pk):
        return '%s:downloads:history:%s'% (self.modelname, pk)

    def date_range_key (self, start, end):
        return '%s:downloads:daterange:%s:%s' % (self.modelname, start.strftime ("%Y-%m-%d"),end.strftime ("%Y-%m-%d"))

    def all_time_period_key (self):
        return '%s:downloads:all'%self.modelname

    def _incr (self, pk, date):
        self.r.incr (self.item_key (pk))
        if not self.r.exists (self.date_key (date)):
            self.r.zincrby (self.date_key (date), pk, 1)            
            self.r.expire (self.date_key (date), 31*24*60*60)
        else:
            self.r.zincrby (self.date_key (date), pk, 1)            
        self.r.zincrby (self.all_time_period_key (), pk, 1)
        self.r.hincrby (self.history_key (pk), date.strftime ("%Y-%m-%d"), 1)

def today (tzone='Asia/Chongqing'):
    return ndays_later (0)

def ndays_later (n, tzone='Asia/Chongqing'):
    tz_cn=timezone(tzone)
    date = (datetime.now(tz_cn)+timedelta(n))
    return date

def date_range (start, end):
    ret=[]
    for n in range (int ((end-start).days)):
        ret.append (start+timedelta(n))
    return ret

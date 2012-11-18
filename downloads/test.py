#-*-coding:utf-8-*-

from main import *
import os
import unittest
from datetime import datetime

class testDownload (unittest.TestCase):
    def setUp (self):
        self.d=Download ()
        self.d.delete_all_keys ()
        for i in xrange (3):
            self.d.incr ('1')        

        self.d.incr ('2')
        self.d.incr ('3')

        for i in xrange (5):
            self.d._incr ('2', ndays_later (-5))

        for i in xrange (10):
            self.d._incr ('5', ndays_later (-22))


    def test_most_downloads_today (self):
        downloads = self.d.most_downloads_today ()
        self.assertEqual (downloads, [('1',3.0), ('3',1.0), ('2',1.0)])

    def test_most_downloads_all_time (self):
        downloads = self.d.most_downloads_all_time ()
        self.assertEqual (downloads, [('5', 10.0), ('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_past_week (self):
        downloads = self.d.most_downloads_in_past_week ()
        self.assertEqual (downloads, [('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_past_month (self):
        downloads = self.d.most_downloads_in_past_month ()
        self.assertEqual (downloads, [('5', 10.0), ('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_past_week_complex (self):
        downloads = self.d.most_downloads_in_past_week_complex ()
        self.assertEqual (downloads[0][2][1][1], '5')
        self.assertEqual (downloads[1][2][6][1], '3')
        self.assertEqual (downloads[2][2][6][1], '1')
        # self.assertEqual (downloads,   [('2',6.0,[('2012-11-11', None),
        #                                           ('2012-11-12', '5'),
        #                                           ('2012-11-13', None),
        #                                           ('2012-11-14', None),
        #                                           ('2012-11-15', None),
        #                                           ('2012-11-16', None),
        #                                           ('2012-11-17', '1')]),
        #                                 ('1',3.0,[('2012-11-11', None), 
        #                                           ('2012-11-12', None), 
        #                                           ('2012-11-13', None), 
        #                                           ('2012-11-14', None), 
        #                                           ('2012-11-15', None), 
        #                                           ('2012-11-16', None), 
        #                                           ('2012-11-17', '3')]),
        #                                 ('3', 1.0,[('2012-11-11', None),
        #                                            ('2012-11-12', None),
        #                                            ('2012-11-13', None),
        #                                            ('2012-11-14', None),
        #                                            ('2012-11-15', None),
        #                                            ('2012-11-16', None),
        #                                            ('2012-11-17', '1')])])

    def test_most_downloads_in_date_range (self):
        downloads = self.d.most_downloads_in_date_range (ndays_later (-6), ndays_later (-2))
        self.assertEqual (downloads, [('2', 5.0)])

    def test_recent_history_in_time_period (self):
        downloads = self.d.recent_history_in_past_week ('2')
        self.assertEqual (downloads[1][1],'5')
        self.assertEqual (downloads[6][1],'1')
        # self.assertEqual (downloads,
        #                   [('2012-11-11', None),
        #                   ('2012-11-12', '5'),
        #                   ('2012-11-13', None),
        #                   ('2012-11-14', None),
        #                   ('2012-11-15', None),
        #                   ('2012-11-16', None),
        #                   ('2012-11-17', '1')])


#-*-coding:utf-8-*-

from main import *
import os
import unittest

class testDownload (unittest.TestCase):
    def setUp (self):
        self.d=Download ()
        self.d.delete_all_keys ()
        for i in xrange (3):
            self.d.incr ('1')        

        self.d.incr ('2')
        self.d.incr ('3')

        for i in xrange (5):
            self.d._incr ('2', ndays_later (5))

        for i in xrange (10):
            self.d._incr ('5', ndays_later (22))


    def test_most_downloads_today (self):
        downloads = self.d.most_downloads_today ()
        self.assertEqual (downloads, [('1',3.0), ('3',1.0), ('2',1.0)])

    def test_most_downloads_all_time (self):
        downloads = self.d.most_downloads_all_time ()
        self.assertEqual (downloads, [('5', 10.0), ('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_one_week (self):
        downloads = self.d.most_downloads_in_one_week ()
        self.assertEqual (downloads, [('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_one_month (self):
        downloads = self.d.most_downloads_in_one_month ()
        self.assertEqual (downloads, [('5', 10.0), ('2', 6.0), ('1', 3.0), ('3', 1.0)])

    def test_most_downloads_in_date_range (self):
        downloads = self.d.most_downloads_in_date_range (ndays_later (2), ndays_later (6))
        self.assertEqual (downloads, [('2', 5.0)])
        


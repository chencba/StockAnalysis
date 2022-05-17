
import unittest

import commandline_menu
import datetime as dt


class DateTester(unittest.TestCase):
        
    def test_date_checker(self):
        date_checker = commandline_menu.Main_Menu()
        start_date, end_date = date_checker.check_date(dt.datetime(2000,1,1), dt.datetime(2010,2,1))
        self.assertEqual(start_date, dt.datetime(2000,1,1))
        self.assertEqual(end_date, dt.datetime(2010,2,1))
        
        
if __name__ == '__main__':
    unittest.main()
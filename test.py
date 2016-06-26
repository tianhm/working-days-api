import unittest
from populate import get_connection, init_db, populate
from server import app, calculate_period
import datetime
import json


class TestPopulateDates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = get_connection()
        cls.cur = cls.conn.cursor()
        init_db(cls.cur)
        populate(cls.cur)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.cur.close()
        cls.conn.close()

    def test_xmas(self):
        self.cur.execute("""SELECT flags FROM holidays WHERE day = '2015-12-25'::date """)
        result = self.cur.fetchone()[0]
        self.assertEqual(result['xmas_ending_2nd'], True)

    def test_query(self):
        self.assertEqual(calculate_period(self.cur, {
                               'start_date': '2015-12-01',
                               'amount': 25,
                               'units': 'working_days',
                               'direction': 'positive',
                               'scheme': 'high_court'})['result'], '2016-01-27')
        self.assertEqual(calculate_period(self.cur, {
                               'start_date': '2001-10-1',
                               'amount': 10,
                               'units': 'working_days',
                               'direction': 'positive',
                               'scheme': 'high_court'})['result'], '2001-10-15')

        self.assertEqual(calculate_period(self.cur, {
                               'start_date': '2015-12-01',
                               'amount': 1,
                               'units': 'weeks',
                               'direction': 'positive',
                               'scheme': 'high_court'})['result'], '2015-12-08')
        self.assertEqual(calculate_period(self.cur, {
                               'start_date': '2015-12-01',
                               'amount': 1,
                               'units': 'months',
                               'direction': 'positive',
                               'scheme': 'high_court'})['result'], '2016-01-18')
        self.assertEqual(calculate_period(self.cur, {
                               'start_date': '2015-12-01',
                               'amount': 2,
                               'units': 'years',
                               'direction': 'positive',
                               'scheme': 'high_court'})['result'], '2017-12-01')


if __name__ == '__main__':
    unittest.main()
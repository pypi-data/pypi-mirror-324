from datetime import timedelta
import unittest
from scp_api_client.api_client import ScpApiClient
import os


API_KEY =  os.getenv('API_KEY', 'test_key')

class TestSCPClient(unittest.TestCase):

    def setUp(self):
        self.client:ScpApiClient = ScpApiClient(api_key=API_KEY)
        print(f"Client environment: {self.client.environment}")
        print(f"Client base_url: {self.client.base_url}")

    def test_init(self):
        self.assertEqual(self.client.api_key, API_KEY)

    def test_headers(self):
        headers = self.client._headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['X-Api-Key'], API_KEY)

    def test_list_all_sources(self):
        sources = self.client.list_all_sources()
        self.assertIsInstance(sources, list)

    def test_trigger_sync(self):
        from datetime import datetime
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        response = self.client.trigger_sync(start_date=start_date, end_date=end_date)
        print(response)
        self.assertEqual(response['errResults'], [])

    def test_list_waybills(self):
        from datetime import datetime
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now()
        waybills = self.client.list_waybills(start_time=start_date, end_time=end_date)
        self.assertIsInstance(waybills, list)
        self.assertGreater(len(waybills), 0)

if __name__ == '__main__':
    unittest.main()

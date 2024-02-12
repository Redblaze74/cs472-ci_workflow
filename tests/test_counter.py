"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter Tests"""
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)
    
    def test_update_a_counter(self):
        """It should update the counter"""
        # 1. Create
        result = self.client.post('/counters/updateCount')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # 2. Ensure Success
        baseline = self.client.get('/counters/updateCount')
        self.assertEqual(baseline.status_code, status.HTTP_200_OK)
        # 3. Check counter value as baseline
        baselineValue = baseline.json['updateCount']
        # 4. Call to Update counter
        update = self.client.put('/counters/updateCount')
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        # 5. Ensure Success
        update = self.client.get('counters/updateCount')
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        # 6. Check counter value is one more than baseline
        update = update.json['updateCount']
        self.assertEqual(update, baselineValue + 1)

    def test_read_a_counter(self):
        """It should read the counter value"""
        result = self.client.post('counters/readCount')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        read = self.client.get('/counters/readCount')
        self.assertEqual(read.status_code, status.HTTP_200_OK)
        value = read.json['readCount']
        self.assertEqual(value, 0)

    def test_read_a_counter_no_name(self):
        """It should attempt to read a counter that does not exist"""
        result = self.client.get('/counters/falseCount')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_a_counter_no_name(self):
        """It should attempt to update a counter that does not exist"""
        result = self.client.put('/counters/falseCount')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

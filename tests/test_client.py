import importlib.util
import pathlib
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'examples/python'))
import soldfetch_client
spec=importlib.util.spec_from_file_location('pagination',pathlib.Path(__file__).resolve().parents[1]/'examples/python/03_pagination.py')
pagination=importlib.util.module_from_spec(spec);spec.loader.exec_module(pagination)
class ClientTests(unittest.TestCase):
    def test_repeated_page_stops(self):
        calls=[]
        def request(path,params):
            calls.append(params)
            return {'items':[{'itemId':'123456789'}],'hasNextPage':True}
        self.assertEqual(len(list(pagination.collect(request,5))),1)
        self.assertEqual(len(calls),2)
        self.assertEqual([p['count'] for p in calls],[20,20])
    def test_last_page_stops(self):
        calls=[]
        def request(path,params):
            calls.append(params);return {'items':[{'itemId':'123456789'}],'hasNextPage':False}
        self.assertEqual(len(list(pagination.collect(request,5))),1);self.assertEqual(len(calls),1)
    def test_destinations_rejected(self):
        for path in ['https://evil.example/','//evil.example/','/v1/item/../usage']:
            with self.assertRaises(ValueError):soldfetch_client.get(path,key='test-only')
    def test_bool_encoding_and_no_redirect(self):
        opener=unittest.mock.MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value=b'{"items":[]}'
        with patch('urllib.request.build_opener',return_value=opener):
            soldfetch_client.get('/v1/scrape',{'sold':False,'keyword':'a & b'},key='test-only',idempotency_key='one')
        req=opener.open.call_args.args[0]
        self.assertIn('sold=false',req.full_url);self.assertNotIn('test-only',req.full_url)
        self.assertIsNone(soldfetch_client.NoRedirect().redirect_request(None,None,302,'',{},'https://evil.example'))
if __name__=='__main__':unittest.main()

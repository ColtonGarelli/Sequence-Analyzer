import unittest
import sys
sys.path.append('/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzer2.1')
import DatabaseAPIs

# test sending request, checking request,
# receiving request, converting to object


class UniProtTester(unittest.TestCase):

    def test_create_url_test(self):
        # test querystring creator
        test_database = DatabaseAPIs.UniProtDatabase()
        query_string = "insulin"
        query = test_database.create_request_url(query_string, "protein names, organism")

        self.assertEqual(query, "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&reviewed=true&"
                                "keywords=keywordsearch&protein=protein%20name&seqLength=10000")

    def test_send_request_test(self):
        # second is actual
        self.assertEqual(True, False)

    def test_update_job_list_test(self):
        self.assertEqual(True, False)

    def test_check_status_test(self):
        self.assertEqual(True, False)

    def test_update_stored_data_test(self):
        self.assertEqual(True, False)

    def test_export_stored_data_test(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

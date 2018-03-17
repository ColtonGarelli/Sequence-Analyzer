import unittest
import RunExperiment


class TestRunExperiment(unittest.TestCase):

    test_experiment1 = RunExperiment.RunExperiment()
    test_experiment2 = RunExperiment.RunExperiment()
    test_experiment3 = RunExperiment.RunExperiment()

    test_file_in = "/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzer2.1/Tests/TestSpreadsheetIn"

    # pretest: should take file in. Have hardcoded list for each test case
    def test_input_spreadsheet(self):
        self.assertEqual(True, True)

    def test_output_spreadsheet(self):
        self.assertEqual(True, True)

    def test_analyze_group(self):
        self.assertEqual(True, True)


class TestSequenceGroups(unittest.TestCase):

    # appends sequences to SequenceGroup
    def test_populate_group_list(self):
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()

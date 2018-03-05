import unittest
import sys
sys.path.append('/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzerProject/Source')
from SecondaryBias import SequenceBias


class BiasFinderTest(unittest.TestCase):
    primary_test = SequenceBias()
    test_one_away = SequenceBias()
    test_two_away = SequenceBias()
    test_three_away = SequenceBias()

    key1 = "I"
    test_one_away.sequence_in = "IKAAESFLPSPVLRTDVMFLVPALKYNPLHRLLIQILGGHETMIQIGHAETATVKFEERLV" \
                "ERIFDKRAGTSSLILIQIDYDEIQIWPGYSILRLGMPEKDEIQIAIITEMKRGAPHIQIQILDFGPA" \
                "ISFKESWLDCVMGNCYNDIASEIKVRGSDLNKVGVRARKECGVATSPINAFINRLLSA" \
                "TYSVGVNFLAVIQISTGIDKVHTNYDKA"

    key2 = "C"
    test_two_away.sequence_in = "TTNIISELRCTQTCGNAMDNWMGEVLDGTPAFHFGVHCGDTAGPASKRFLLVCLEFSLR" \
                "GYDLLVRLLLIKDEDANDVHCNQKCSQCCQKCMAHLALGPVTCSSSFNVHYSPGIGAL" \
                "WACIQTCEIDYCIQPCKACVQSCEERSLKVIKADGITAKSFAPMPNGAVDPSTVEYMV" \
                "KTLIVCLQTCYDENRTVRRFPEKAL"

    key3 = "S"
    test_three_away.sequence_in = "YPSSALQGGSMSRFLSPTMLRVRASLGFLGINLLPWTLFVIAALPSKSDAQLSSTQPLSAMGME" \
                "FIRANTESEINFVDKIHYAYHNLVVDPRKVDSEIAKERCKLLKSIVQVGSVTFATVPGDS" \
                "YIGISSRSLMFVSEKNTGRELGNKCSAEQDDSSDQKNSGTAECGKLYSYEQWESTREGVDIIR" \
                "KKTAVTHSNRQIPSVADHPLFLADAHEG"

    sequence1 = "QQQQQQQQQQQQQQQQQQ"
    sequence2 = "GWEQEWGGWEQEWGGWEQEWGGWEQEWG"
    sequence3 = "VTVQRSNFHQQKIRPQQPLGDKAHLLM"
    sequence4 = "CQQVKQDSHCCLQQQSTQLFQQQSERSQEIQMADIQTQ"
    sequence5 = "GQNQRWWYVTVQRSNFHQQKIRPQQPLGDKAHLLMQQMGGQQRAFYMPEQTQCFEYRI" \
                "DQCVWQEGFQEQAHAWPNVQKECQQVKQDSHCCLQQQSTLFQQQSERSQEIQMADIQTQ"
    sequence6 = "ADSFEWASDF"
    sequence7 = "WPNVQKECQQVKQDSHCCLQQQSTLFQ"
    sequence8 = "GVMWHDGTWDSAQHHFRQTY"
    sequence9 = "GQNQRWWYVTVQRSNFHQQKIRPQQPLGDKAHLLMQQMGGQQRAFYMPEQTQCFEYRI" \
                "DQCVWQEGFQEQAHAWPNVQKECQQVKQDSHCCLQQQSTLFQQQSERSQEIQMADIQ" \
                "TQCIGQNHQGVMWHDGTWDSAQHHFRQTYQYWWTPQLFVPYQDNRQAMNCQKLQAEVQ" \
                "SISQNTQKMPFPNQYQQKMDIKQIQQC"
    sequence10 = "VTVQRSNFHQQKIRPQQPLGDKAHLLM"

    seq_list = [sequence1, sequence2, sequence3, sequence4, sequence5,
                sequence6, sequence7, sequence8, sequence9, sequence10]

    list_q_content = [12, 4, 5, 10, 28, 0, 7, 1, 47]

    assertKey = ["list of integers of expected one_away, two_away vals"]

    # def run_pre_bias_test(self):
    #     self.primary_test.primary_bias = "Q"
    #     self.primary_test.sequence_len = len(self.primary_test.sequence_in)
    #     self.primary_test.find_primary_bias()
    #     self.primary_test.Q_content = len(self.primary_test.Q_index)
    #     self.primary_test.secondary_bias_finder()
    #
    # def test_find_primary_bias(self):
    #     for i in range(0, 9):
    #         self.primary_test.sequence_in = self.seq_list[i]
    #         self.run_pre_bias_test()
    #         self.assertEqual(BiasFinderTest.list_q_content[i], self.primary_test.Q_content)
    #         self.primary_test.Q_index = []

    def run_pre_sec_bias1_test(self):
        self.test_one_away.primary_bias = "Q"
        self.test_one_away.sequence_len = len(self.test_one_away.sequence_in)
        self.test_one_away.Q_index = []
        self.test_one_away.find_primary_bias()
        self.test_one_away.Q_content = len(self.test_one_away.Q_index)
        self.test_one_away.secondary_bias_finder()

    def run_pre_sec_bias2_test(self):
        self.test_two_away.primary_bias = "Q"
        self.test_two_away.sequence_len = len(self.test_two_away.sequence_in)
        self.test_two_away.Q_index = []
        self.test_two_away.find_primary_bias()
        self.test_two_away.Q_content = len(self.test_two_away.Q_index)
        self.test_two_away.secondary_bias_finder()

    def run_pre_sec_bias3_test(self):
        self.test_three_away.primary_bias = "Q"
        self.test_three_away.sequence_len = len(self.test_three_away.sequence_in)
        self.test_three_away.Q_index = []
        self.test_three_away.three_away = [0]*20
        self.test_three_away.find_primary_bias()
        self.test_three_away.Q_content = len(self.test_three_away.Q_index)
        self.test_three_away.secondary_bias_finder()

    def test_secondary_bias_finder(self):
        keylist = ["I", "C", "S"]

        self.run_pre_sec_bias1_test()
        self.assertEqual(2, self.test_one_away.one_away[7] / self.test_one_away.Q_content)

        self.run_pre_sec_bias2_test()
        self.assertEqual(2, self.test_two_away.two_away[1] / self.test_two_away.Q_content)

        self.run_pre_sec_bias3_test()
        threeaway = self.test_three_away.three_away[15]
        self.assertEqual(2, (threeaway / self.test_three_away.Q_content))
    '''
    Write tests for both functions. Tests to make sure nothing but one of the 20 a.a.
    get past checkaa

    write test for secondary bias.

    '''
    # def test_check_if_first_bias(self):
    #     self.assertFalse(False, False)
    #
    # def test_calculate_biases(self):
    #     self.assertFalse(False)


class CheckAATests(unittest.TestCase):
    # tests for checkaaentry method

    seq_1 = SequenceBias()
    seq_1.sequence_in = "SAQHHFRQTYQYWWTPQLFVPYQDNRQAMNCQKLQAEVQSISQNTQKMPFPNQYQQKMDIKQIQQC"
    seq_2 = SequenceBias()
    seq_2.sequence_in = "1"
    seq_3 = SequenceBias()
    seq_3.sequence_in = "1QCVWQEGFQEQAHA"
    seq_4 = SequenceBias()
    seq_4.sequence_in = "CCLQQQSTLFQQQSERSQEIQM3"
    seq_5 = SequenceBias()
    seq_5.sequence_in = "123453F13423"
    seq_6 = SequenceBias()
    seq_6.sequence_in = "ADSFEW@ASDF"
    seq_7 = SequenceBias()
    seq_7.sequence_in = "WPNVQKECQQVKQDSHCCLQQQSTLFQ*"
    seq_8 = SequenceBias()
    seq_8.sequence_in = "*GVMWHDGTWDSAQHHFRQTY"
    seq_9 = SequenceBias()
    seq_9.sequence_in = "ASSD SDS"
    seq_10 = SequenceBias()
    seq_10.sequence_in = "JJJJJJJJJJJ"
    seq_11 = SequenceBias()
    seq_11.sequence_in = "GQNQRWWYVTVQRSNFHQQKIRPQQPLGDKAHLLMQQMGGQQRAFYMPEQTQCFEYRI" \
                         "DQCVWQEGFQEQAHAWPNVQKECQQVKQDSHCCLQQQSTLFQQQSERSQEIQMADIQTQ" \
                         "CIGQNHQGVMWHDGTWDXSAQHHFRQTYQYWWTPQLFVPYQDNRQAMNCQKLQAEVQSIS" \
                         "QNTQKMPFPNQYQQKMDIKQIQQC"

    def test_check_aa_entry_pass(self):
        post_test = SequenceBias()
        for i in range(10):
            post_test.sequence_in = BiasFinderTest.seq_list[i]
            self.assertTrue(SequenceBias.check_aa_entry(post_test, post_test.sequence_in))

    def test_check_aa_entry(self):
        self.assertTrue(SequenceBias.check_aa_entry(self.seq_1, self.seq_1.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_2, self.seq_2.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_3, self.seq_3.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_4, self.seq_4.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_5, self.seq_5.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_6, self.seq_6.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_7, self.seq_7.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_8, self.seq_8.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_9, self.seq_9.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_10, self.seq_10.sequence_in))
        self.assertFalse(SequenceBias.check_aa_entry(self.seq_11, self.seq_11.sequence_in))


if __name__ == '__main__':

    unittest.main()

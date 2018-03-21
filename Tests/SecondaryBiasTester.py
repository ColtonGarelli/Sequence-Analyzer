import unittest
import sys

import SecondaryBiasFinder
from SecondaryBiasFinder import SecondaryBias, Sequence
from Operation import Director, AnalysisImpl


class BiasFinderTest(unittest.TestCase):
    primary_test = SecondaryBias()
    test_one_away = SecondaryBias()
    test_two_away = SecondaryBias()
    test_three_away = SecondaryBias()

    key1 = "I"
    test_one_away.sequence = "IKAAESFLPSPVLRTDVMFLVPALKYNPLHRLLIQILGGHETMIQIGHAETATVKFEERLV" \
                "ERIFDKRAGTSSLILIQIDYDEIQIWPGYSILRLGMPEKDEIQIAIITEMKRGAPHIQIQILDFGPA" \
                "ISFKESWLDCVMGNCYNDIASEIKVRGSDLNKVGVRARKECGVATSPINAFINRLLSA" \
                "TYSVGVNFLAVIQISTGIDKVHTNYDKA"

    key2 = "C"
    test_two_away.sequence = "TTNIISELRCTQTCGNAMDNWMGEVLDGTPAFHFGVHCGDTAGPASKRFLLVCLEFSLR" \
                             "GYDLLVRLLLIKDEDANDVHCNQKCSQCCQKCMAHLALGPVTCSSSFNVHYSPGIGAL" \
                             "WACIQTCEIDYCIQPCKACVQSCEERSLKVIKADGITAKSFAPMPNGAVDPSTVEYMV" \
                             "KTLIVCLQTCYDENRTVRRFPEKAL"

    key3 = "S"
    test_three_away.sequence = "YPSSALQGGSMSRFLSPTMLRVRASLGFLGINLLPWTLFVIAALPSKSDAQLSSTQPLSAMGME" \
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

    def run_pre_sec_bias1_test(self):
        self.test_one_away.primary_bias = "Q"
        self.test_one_away.sequence_len = len(self.test_one_away.sequence)
        self.test_one_away.Q_index = []
        self.test_one_away.find_primary_bias()
        self.test_one_away.Q_content = len(self.test_one_away.Q_index)
        self.test_one_away.secondary_bias_finder()

    def run_pre_sec_bias2_test(self):
        self.test_two_away.primary_bias = "Q"
        self.test_two_away.sequence_len = len(self.test_two_away.sequence)
        self.test_two_away.Q_index = []
        self.test_two_away.find_primary_bias()
        self.test_two_away.Q_content = len(self.test_two_away.Q_index)
        self.test_two_away.secondary_bias_finder()

    def run_pre_sec_bias3_test(self):
        self.test_three_away.primary_bias = "Q"
        self.test_three_away.sequence_len = len(self.test_three_away.sequence)
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


class SequenceBiasIOTests(unittest.TestCase):

    def test_file_to_seqbias(self):
        seq_list = ["IKAAESFLPSPVLRTDVMFLVPALKYNPLHRLLIQILGGHETMIQIGHAETATVKFEERLVERIFDKRAGTSSLILIQIDYDEIQIWPGYSILRLGMPEKDEIQIAIITEMKRGAPHIQIQILDFGPAISFKESWLDCVMGNCYNDIASEIKVRGSDLNKVGVRARKECGVATSPINAFINRLLSATYSVGVNFLAVIQISTGIDKVHTNYDKA",
                    "TTNIISELRCTQTCGNAMDNWMGEVLDGTPAFHFGVHCGDTAGPASKRFLLVCLEFSLRGYDLLVRLLLIKDEDANDVHCNQKCSQCCQKCMAHLALGPVTCSSSFNVHYSPGIGALWACIQTCEIDYCIQPCKACVQSCEERSLKVIKADGITAKSFAPMPNGAVDPSTVEYMVKTLIVCLQTCYDENRTVRRFPEKAL",
                    "YPSSALQGGSMSRFLSPTMLRVRASLGFLGINLLPWTLFVIAALPSKSDAQLSSTQPLSAMGMEFIRANTESEINFVDKIHYAYHNLVVDPRKVDSEIAKERCKLLKSIVQVGSVTFATVPGDSYIGISSRSLMFVSEKNTGRELGNKCSAEQDDSSDQKNSGTAECGKLYSYEQWESTREGVDIIRKKTAVTHSNRQIPSVADHPLFLADAHEG"]

        path_in = "/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzer2.1/Tests/SequenceBiasIOTestFile"
        analysis = AnalysisImpl(path_in)
        director = Director()
        processed = director.run_analysis(analysis)
        for i in range(len(analysis.seq_list)):
            check_seq = analysis.seq_list[i]
            self.assertEqual(seq_list[i], check_seq.sequence)

    def test_seqbias_to_file(self):
        list_q_content = [12, 4, 5, 10, 28, 0, 7, 1, 47]
        # one_away I = 16
        # two_away C =
        seq_list = ["IKAAESFLPSPVLRTDVMFLVPALKYNPLHRLLIQILGGHETMIQIGHAETATVKFEERLVERIFDKRAGTSSLILIQIDYDEIQIWPGYSILRLGMPEKDEIQIAIITEMKRGAPHIQIQILDFGPAISFKESWLDCVMGNCYNDIASEIKVRGSDLNKVGVRARKECGVATSPINAFINRLLSATYSVGVNFLAVIQISTGIDKVHTNYDKA",
                    "TTNIISELRCTQTCGNAMDNWMGEVLDGTPAFHFGVHCGDTAGPASKRFLLVCLEFSLRGYDLLVRLLLIKDEDANDVHCNQKCSQCCQKCMAHLALGPVTCSSSFNVHYSPGIGALWACIQTCEIDYCIQPCKACVQSCEERSLKVIKADGITAKSFAPMPNGAVDPSTVEYMVKTLIVCLQTCYDENRTVRRFPEKAL",
                    "YPSSALQGGSMSRFLSPTMLRVRASLGFLGINLLPWTLFVIAALPSKSDAQLSSTQPLSAMGMEFIRANTESEINFVDKIHYAYHNLVVDPRKVDSEIAKERCKLLKSIVQVGSVTFATVPGDSYIGISSRSLMFVSEKNTGRELGNKCSAEQDDSSDQKNSGTAECGKLYSYEQWESTREGVDIIRKKTAVTHSNRQIPSVADHPLFLADAHEG"]

        seq_objs = []
        # test file in by checking read_file strings are equal
        # write one file manually and read it in, check to see it's equal to the read in from the exported file
        for i in range(len(seq_list)):
            seq = SecondaryBias()
            seq.initialize_sec_bias("tester" + str(i), seq_list[i])
            seq.bias_finder()
            seq_objs.append(seq)
        SecondaryBiasFinder.export_sec_bias_files(seq_objs)


class CheckAATests(unittest.TestCase):
    # tests for checkaaentry method
    seq_1 = SecondaryBias()
    seq_1.sequence = "SAQHHFRQTYQYWWTPQLFVPYQDNRQAMNCQKLQAEVQSISQNTQKMPFPNQYQQKMDIKQIQQC"
    seq_2 = SecondaryBias()
    seq_2.sequence = "1"
    seq_3 = SecondaryBias()
    seq_3.sequence = "1QCVWQEGFQEQAHA"
    seq_4 = SecondaryBias()
    seq_4.sequence = "CCLQQQSTLFQQQSERSQEIQM3"
    seq_5 = SecondaryBias()
    seq_5.sequence = "123453F13423"
    seq_6 = SecondaryBias()
    seq_6.sequence = "ADSFEW@ASDF"
    seq_7 = SecondaryBias()
    seq_7.sequence = "WPNVQKECQQVKQDSHCCLQQQSTLFQ*"
    seq_8 = SecondaryBias()
    seq_8.sequence = "%GVMWHDGTWDSAQHHFRQTY"
    seq_9 = SecondaryBias()
    seq_9.sequence = "ASSD SDS"
    seq_10 = SecondaryBias()
    seq_10.sequence = "JJJJJJJJJJJ"
    seq_11 = SecondaryBias()
    seq_11.sequence = "GQNQRWWYVTVQRSNFHQQKIRPQQPLGDKAHLLMQQMGGQQRAFYMPEQTQCFEYRI" \
                      "DQCVWQEGFQEQAHAWPNVQKECQQVKQDSHCCLQQQSTLFQQQSERSQEIQMADIQTQ" \
                      "CIGQNHQGVMWHDGTWDXSAQHHFRQTYQYWWTPQLFVPYQDNRQAMNCQKLQAEVQSIS" \
                      "QNTQKMPFPNQYQQKMDIKQIQQC"

    def test_check_aa_entry_pass(self):
        post_test = SecondaryBias()
        for i in range(10):
            post_test.sequence = BiasFinderTest.seq_list[i]
            self.assertTrue(SecondaryBiasFinder.check_aa_entry(post_test.sequence))

    def test_check_aa_entry_fail(self):
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_2.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_3.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_4.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_5.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_6.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_7.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_8.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_9.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_10.sequence))
        self.assertFalse(SecondaryBiasFinder.check_aa_entry(self.seq_11.sequence))


if __name__ == '__main__':

    unittest.main()

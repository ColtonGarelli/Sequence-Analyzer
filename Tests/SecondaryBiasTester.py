import unittest
import SecondaryBiasFinder
from SecondaryBiasFinder import SecondaryBias, Sequence
from Operation import Director, AnalysisImpl


class InductiveBiasFinderTest(unittest.TestCase):
    # make dictionary - sequence:sec value
    # or try with tuples
    # make sure tests that pass also fail if data is incorrect
    test_sequences_dict = {"LGVQVKG": 2, "GSVQHAW": 1, "LFYQVFL": 1, "DEHQANI": 0, "SVNQGVY": 2, "FEIQDVP": 1,
                           "DVKQKDN": 1, "SLEQEIR": 0, "VEPQRIV": 2, "LAFQNHV": 1, "VKMQCLT": 1, "GKAQSGP": 0,
                           "YAMAFLP": 0, "VKGRTCT": 0}
    test_sequences_list = ["LGVQVKG", "GSVQHAW", "LFYQVFL", "DEHQANI", "SVNQGVY", "FEIQDVP",
                           "DVKQKDN", "VEPQRIV", "LLAQNGV", "VKMQCLT", "GKALSGP", "YAMAFLP", "VKGRTCT"]

    test_sequences_dict_one = {"LGVQVKG": 2, "GSVQHAW": 1, "LFYQVFL": 1, "DEHQANI": 0, "VKGRTCT": 0}
    test_sequences_list_one = ["LGVQVKG", "GSVQHAW", "LFYQVFL", "DEHQANI", "VKGRTCT"]

    test_sequences_dict_two = {"SVNQGVY": 2, "FEIQDVP": 1, "DVKQKDN": 1, "SLEQEIR": 0, "VKGRTCT": 0}
    test_sequences_list_two = ["SVNQGVY", "FEIQDVP", "DVKQKDN", "SLEQEIR", "VKGRTCT"]

    test_sequences_dict_three = {"VEPQRIV": 2, "LAFQNHV": 1, "VKMQCLT": 1, "GKAQSGP": 0, "YAMAFLP": 0, "VKGRTCT": 0}
    test_sequences_list_three = ["VEPQRIV", "LAFQNHV", "VKMQCLT", "GKAQSGP", "YAMAFLP", "VKGRTCT"]

    def test_concat_aa(self):
        for i1 in range(len(self.test_sequences_list)-1):
            if i1 < 3:
                for i2 in range(len(self.test_sequences_dict_one)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_one[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_one[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.one_away[17], self.test_sequences_dict_one[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_one[original_seq])
                        seq_to_scan = SecondaryBias()
                        seq_to_scan.sequence = original_seq + append_sequence[0:i3]
            elif 2 < i1 < 10:
                for i2 in range(len(self.test_sequences_dict_two)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_two[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_two[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.two_away[17], self.test_sequences_dict_two[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_two[original_seq])
                        seq_to_scan = SecondaryBias()
                        seq_to_scan.sequence = original_seq + append_sequence[0:i3]

            else:
                for i2 in range(len(self.test_sequences_dict_three)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_three[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_three[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.three_away[17], self.test_sequences_dict_three[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_three[original_seq])
                        seq_to_scan = SecondaryBias()
                        seq_to_scan.sequence = original_seq + append_sequence[0:i3]

    def test_rev_concat_aa(self):
        for i1 in range(len(self.test_sequences_list)-1):
            if i1 < 3:
                for i2 in range(len(self.test_sequences_dict_one)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_one[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_one[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.one_away[17], self.test_sequences_dict_one[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_one[original_seq])
                        seq_to_scan = SecondaryBias()
                        holder = ""
                        for i in append_sequence[:i3]:
                            holder = i + holder
                        seq_to_scan.sequence = holder + original_seq

            elif 2 < i1 < 10:
                for i2 in range(len(self.test_sequences_dict_two)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_two[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_two[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.two_away[17], self.test_sequences_dict_two[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_two[original_seq])
                        seq_to_scan = SecondaryBias()
                        holder = ""
                        for i in append_sequence[:i3]:
                            holder = i + holder
                        seq_to_scan.sequence = holder + original_seq
            else:
                for i2 in range(len(self.test_sequences_dict_three)-1):
                    seq_to_scan = SecondaryBias()
                    original_seq = self.test_sequences_list_three[i2]
                    seq_to_scan.sequence = original_seq
                    append_sequence = self.test_sequences_list_three[i2 + 1]
                    for i3 in range(len(original_seq)-1):
                        seq_to_scan.bias_finder()
                        self.assertEqual(seq_to_scan.three_away[17], self.test_sequences_dict_three[original_seq])
                        self.assertEqual(int(seq_to_scan.local_sequence[17]), self.test_sequences_dict_three[original_seq])
                        seq_to_scan = SecondaryBias()
                        holder = ""
                        for i in append_sequence[:i3]:
                            holder = i + holder
                        seq_to_scan.sequence = holder + original_seq


    def test_concat_whole_sequences(self):
        seq_to_scan = SecondaryBias()






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

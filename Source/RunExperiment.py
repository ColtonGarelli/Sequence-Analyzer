


def prompt_sequence_input(self):
        """
        Prompts user to enter a sequence manually, and calls Sequence.check_aa_entry to ensure valid entry=

        :return: A valid sequence of natural amino acids as a String object
        """
        sequence_in = input('Enter an amino acid sequence ')
        good_sequence = self.check_aa_entry(sequence_in)
        while not good_sequence:
            sequence_in = input('Enter an amino acid sequence ')
            good_sequence = self.check_aa_entry(sequence_in)
        return sequence_in

    # def calculate_biases(self):
    #     """
    #
    #     :return:
    #     """
    #     # Write to ignore Q @ 0, 1, 2 or seqlen, seqlen-1, seqlen-2
    #     for i in range(0, 19):
    #         self.one_away_avg[i] = (self.one_away[i] / self.sequence_len)
    #         self.two_away_avg[i] = self.two_away[i] / self.sequence_len
    #         self.three_away_avg[i] = self.three_away[i] / self.sequence_len
    #         # only a true local avg if primary bias is always at index 3 or seq_len-3
    #         self.local_avg[i] = (self.local_sequence[i] * 6) / self.sequence_len
    #     # else:
    #     #     for i in range(0, 19):
    #     #         self.one_away_avg[i] = (self.one_away[i] / self.sequence_len)
    #     #         self.two_away_avg[i] = self.two_away[i] / self.sequence_len
    #     #         self.three_away_avg[i] = self.three_away[i] / self.sequence_len



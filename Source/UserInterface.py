import SecondaryBiasFinder


def welcome():
    print("Welcome to the Sequence Analyzer\n")
    print("Please refer to documentation at ")

    in_path = input("\nEnter the full path of the input file")
    out_path = input("\nEnter the full path for the output file")




def print_secondarybias_info(seqbiasobj) -> SecondaryBiasFinder:

    if seqbiasobj.Q_content != 0:
        print("\n\nOne Away\t\t\t\t\t Two Away\t\t\t\t\t Three Away\t\t\t\t\t Local")
        for i in range(0, 19):
            print(seqbiasobj.amino_acids[i],
                  round(seqbiasobj.one_away[i] / seqbiasobj.Q_content, 3), "per", seqbiasobj.primary_bias,
                  "\t\t\t\t", seqbiasobj.amino_acids[i],
                  round(seqbiasobj.two_away[i] / seqbiasobj.Q_content, 3), "per", seqbiasobj.primary_bias,
                  "\t\t\t\t", seqbiasobj.amino_acids[i],
                  round(seqbiasobj.three_away[i] / seqbiasobj.Q_content, 3), "per", seqbiasobj.primary_bias,
                  "\t\t\t\t", seqbiasobj.amino_acids[i],
                  round(seqbiasobj.local_sequence[i] / seqbiasobj.Q_content, 3), "per", seqbiasobj.primary_bias)
    else:
        print("\n\nNo primary bias\n")


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




from Sequence import Sequence
import PrintStuff

'''
This class takes a seq, counts Q total and Q stretch, a.a. occurance around Qs
Could add functions to make compatible w multiseq alignments/genome screens



The bias finder function allows a user to search for a secondary aa bias in a sequence
beyond an entered primary bias

very much work in function

----should break up into smaller pieces

---class vars updated in bias_finder. helper methods return values and they are changed post method call
---choose random sequences from https://web.expasy.org/cgi-bin/randseq/randseq.pl for testing. modify for cases
---change to MVC format and use multiple inheritance to make classes that get seq info from uniprot
'''

# inherts from Sequence


class SequenceBias(Sequence):
    """
    SequenceBias extends the Sequence class. SequenceBias has methods prompt input determines primary
    and secondary sequence biases. Is used primarily to find primary glutamine bias, and secondary
    biases at the +/- 1,2,3, and an average of these 6 positions, for each Q.
    """
    ID = "name"
    primary_bias = "Q"
    sequence_len = 0
    one_away = [0] * 20
    two_away = [0] * 20
    three_away = [0] * 20
    local_sequence = [0] * 20
    Q_index = []
    Q_content = 0
    one_away_avg = [0] * 20
    two_away_avg = [0] * 20
    three_away_avg = [0] * 20
    local_avg = [0] * 20

    # Takes user inputted sequence and ensures only natural amino acids are in seq
    # constructor (built in default)
    # update stuff with docstrings, sequence variables
    # could also write overloaded assignment op
    # change to return true or false, and get called from secondary bias until return true
    # Write docstring below
    # elements of each array represent a single a.a., in alphabetical order (0=A, 1=C, etc)
    # each array will serve as a count for a.a. appearances near primary bias (1-2 aa)
    #  localseq is the aggregate

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

    def choose_primary_bias(self):
        """
        Allows the user to select a primary amino acid to search for secondary biases around.

        :return: A valid amino acid single letter code as a String object
        """
        # have a UI method to interact w user
        input_mode = input('1 for glutamine 2 for other ')
        while (input_mode != '1') and (input_mode != '2'):
            input_mode = input('1 for glutamine 2 for other ')
        input_aa = int(input_mode)
        if input_aa == 2:
            firstbias = input('Please enter a primary bias to search ')
            check_bias_entry = self.check_aa_entry(firstbias)
            while not check_bias_entry:
                check_bias_entry = self.check_aa_entry(firstbias)
        else:
            firstbias = "Q"
        return firstbias

    def calculate_biases(self):
        """

        :return:
        """
        # Write to ignore Q @ 0, 1, 2 or seqlen, seqlen-1, seqlen-2
        for i in range(0, 19):
            self.one_away_avg[i] = (self.one_away[i] / self.sequence_len)
            self.two_away_avg[i] = self.two_away[i] / self.sequence_len
            self.three_away_avg[i] = self.three_away[i] / self.sequence_len
            # only a true local avg if primary bias is always at index 3 or seq_len-3
            self.local_avg[i] = (self.local_sequence[i] * 6) / self.sequence_len
        # else:
        #     for i in range(0, 19):
        #         self.one_away_avg[i] = (self.one_away[i] / self.sequence_len)
        #         self.two_away_avg[i] = self.two_away[i] / self.sequence_len
        #         self.three_away_avg[i] = self.three_away[i] / self.sequence_len

    def print_q_normalized(self):
        # print("One Away:")

        if self.Q_content != 0:
            print("\n\nOne Away\t\t\t\t\t Two Away\t\t\t\t\t Three Away\t\t\t\t\t Local")
            for i in range(0, 19):
                print(self.amino_acids[i],
                      round(self.one_away[i]/self.Q_content, 3), "per", self.primary_bias,
                      "\t\t\t\t", self.amino_acids[i],
                      round(self.two_away[i] / self.Q_content, 3), "per", self.primary_bias,
                      "\t\t\t\t", self.amino_acids[i],
                      round(self.three_away[i] / self.Q_content, 3), "per", self.primary_bias,
                      "\t\t\t\t", self.amino_acids[i],
                      round(self.local_sequence[i] / self.Q_content, 3), "per", self.primary_bias)
        else:
            print("\n\nNo primary bias\n")
            # print("\n\nTwo Away:")
            # print(self.amino_acids[i],
            #       self.two_away[i] / self.Q_content, "per", self.primary_bias)
        # for i in range(0, 19):
        #     print(self.amino_acids[i],
        #           self.two_away[i] / self.Q_content, "per", self.primary_bias)
        # print("\n\nThree Away:")
        # for i in range(0, 19):
        #     print(self.amino_acids[i],
        #           self.three_away[i] / self.Q_content, "per", self.primary_bias)
        # print("\n\nLocal:")
        # for i in range(0, 19):
        #     print(self.amino_acids[i],
        #           self.local_sequence[i] / self.Q_content, "per", self.primary_bias)

    def find_primary_bias(self):
        """
        Finds the primary bias defined by the user. Ignores first and last three aa in seq for primary bias calculation
        :return: updates self.Q_index list (no return)
        """
        if self.primary_bias in self.sequence_in:
            for i in range(len(self.sequence_in)):
                if self.sequence_in[i] == self.primary_bias:
                    # if statement should ignore Q. Could split loops so if isn't read outside
                    # the first three and last three indexes. Range b/t could be very large
                    if 2 < i < self.sequence_len-4:
                        self.Q_index.append(i)
        # else:
        #     print("No" + self.primary_bias + " in the sequence ")
        # print(self.Q_index)

    def secondary_bias_finder(self):
        """

        :return:
        """

        for i in range(self.Q_content):
            # Q_minus1 = the index in sequence_in of the a.a. to the left of the Q_index[i]
            # which refers to the index of this Q
            # in sequence_in
            Q_minus1 = self.Q_index[i] - 1
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_minus1]]
            self.one_away[aa_to_increment] += 1

            Q_plus1 = self.Q_index[i] + 1
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_plus1]]
            self.one_away[aa_to_increment] += 1

            Q_minus2 = self.Q_index[i] - 2
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_minus2]]
            self.two_away[aa_to_increment] += 1

            Q_plus2 = self.Q_index[i] + 2
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_plus2]]
            self.two_away[aa_to_increment] += 1

            Q_minus3 = self.Q_index[i] - 3
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_minus3]]
            self.three_away[aa_to_increment] += 1

            Q_plus3 = self.Q_index[i] + 3
            aa_to_increment = self.amino_acid_dict[self.sequence_in[Q_plus3]]
            self.three_away[aa_to_increment] += 1

            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_minus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_plus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_minus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_plus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_minus3]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence_in[Q_plus3]]] += 1
            #
            # local_aa = self.one_away[i] + self.two_away[i] + self.three_away[i]
            # self.local_sequence[self.amino_acid_dict[self.sequence_in[local_aa]]] += 1

    def setID(self):
        self.ID = input("Input ID:")

    def bias_finder(self):
        """
        Is effectively a constructor for the SequenceBias class.  bias_finder calls UI functions,
        runs bias finders on the sequence input, and updates SequenceBias object.
        :ivar:
        :ivar:
        :ivar:
        :cvar:
        """

        self.primary_bias = self.choose_primary_bias()
        self.sequence_in = self.prompt_sequence_input()
        self.sequence_in = self.sequence_in.upper()
        self.sequence_len = len(self.sequence_in)
        self.find_primary_bias()
        self.Q_content = len(self.Q_index)
        # indices of aa adjacent to q in master seq
        # at the end of if block arrays that count each amino acid one, two, and three positions from q
        # arrays are ordered in single letter code alphabetical order
        self.secondary_bias_finder()
        self.calculate_biases()
        PrintStuff.print_stuff_for_testing(self)

import abc
import SpreadsheetIO
from SpreadsheetIO import write_list_to_file


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


class Sequence:

    def __init__(self):
        self.ID = ""
        self.sequence = ""
        self.amino_acids = "ACDEFGHIKLMNPQRSTVWY"


class SecondaryBias(Sequence):
    """
    SequenceBias extends the Sequence class. SequenceBias has methods prompt input determines primary
    and secondary sequence biases. Is used primarily to find primary glutamine bias, and secondary
    biases at the +/- 1,2,3, and an average of these 6 positions, for each Q.
    """

    def __init__(self):
        super(Sequence).__init__()
        self.ID = ""
        self.sequence = ""
        self.amino_acids = "ACDEFGHIKLMNPQRSTVWY"
        self.amino_acid_dict = dict(A=0, C=1, D=2, E=3, F=4, G=5, H=6, I=7, K=8, L=9,
                                    M=10, N=11, P=12, Q=13, R=14, S=15, T=16, V=17, W=18, Y=19)

        self.primary_bias = "Q"
        self.sequence_len = 0
        self.Q_index = []
        self.Q_content = 0
        self.one_away = [0] * 20
        self.two_away = [0] * 20
        self.three_away = [0] * 20
        self.local_sequence = [0] * 20
        self.one_away_avg = [0] * 20
        self.two_away_avg = [0] * 20
        self.three_away_avg = [0] * 20
        self.local_avg = [0] * 20

    # Takes user inputted sequence and ensures only natural amino acids are in seq
    # update stuff with docstrings, sequence variables
    # could also write overloaded assignment op
    # change to return true or false, and get called from secondary bias until return true
    # Write docstring below
    # elements of each array represent a single a.a., in alphabetical order (0=A, 1=C, etc)
    # each array will serve as a count for a.a. appearances near primary bias (1-2 aa)
    #  localseq is the aggregate

    def initialize_sec_bias(self, seq_name, seq_in):
        self.ID = seq_name
        self.sequence = seq_in

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

    def find_primary_bias(self):
        """
        Finds the primary bias defined by the user. Ignores first and last three aa in seq for primary bias calculation
        :return: updates self.Q_index list (no return)
        """
        if self.primary_bias in self.sequence:
            for i in range(len(self.sequence)):
                if self.sequence[i] == self.primary_bias:
                    # if statement should ignore Q. Could split loops so if isn't read outside
                    # the first three and last three indexes. Range b/t could be very large
                    if 2 < i < self.sequence_len-4:
                        self.Q_index.append(i)

    def secondary_bias_finder(self):
        """
        Finds amino acids adjacent to
        :return:
        """

        for i in range(self.Q_content):
            # Q_minus1 = the index in sequence_in of the a.a. to the left of the Q_index[i]
            # which refers to the index of this Q
            # in sequence_in
            Q_minus1 = self.Q_index[i] - 1
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_minus1]]
            self.one_away[aa_to_increment] += 1

            Q_plus1 = self.Q_index[i] + 1
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_plus1]]
            self.one_away[aa_to_increment] += 1

            Q_minus2 = self.Q_index[i] - 2
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_minus2]]
            self.two_away[aa_to_increment] += 1

            Q_plus2 = self.Q_index[i] + 2
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_plus2]]
            self.two_away[aa_to_increment] += 1

            Q_minus3 = self.Q_index[i] - 3
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_minus3]]
            self.three_away[aa_to_increment] += 1

            Q_plus3 = self.Q_index[i] + 3
            aa_to_increment = self.amino_acid_dict[self.sequence[Q_plus3]]
            self.three_away[aa_to_increment] += 1

            self.local_sequence[self.amino_acid_dict[self.sequence[Q_minus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence[Q_plus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence[Q_minus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence[Q_plus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence[Q_minus3]]] += 1
            self.local_sequence[self.amino_acid_dict[self.sequence[Q_plus3]]] += 1

    def find_avg_occurrence(self):
        if self.Q_content != 0:
            for i in range(0, 19):
                self.one_away_avg[i] = self.one_away[i] / self.Q_content
                self.two_away_avg[i] = self.two_away[i] / self.Q_content
                self.three_away_avg[i] = self.three_away[i] / self.Q_content
                self.local_sequence[i] = self.local_sequence[i] / self.Q_content
        else:
            print("no glutamine")

    def bias_finder(self):
        """
        Is effectively a constructor for the SequenceBias class.  bias_finder calls UI functions,
        runs bias finders on the sequence input, and updates SequenceBias object.
        :ivar:
        :ivar:
        :ivar:
        :cvar:
        """

        # change user in
        # self.primary_bias = self.choose_primary_bias()
        # self.seq_in = self.prompt_sequence_input()
        # self.sequence = self.remove_spaces(self.sequence)
        self.sequence = self.sequence.upper()
        self.sequence_len = len(self.sequence)
        self.find_primary_bias()
        self.Q_content = len(self.Q_index)
        # indices of aa adjacent to q in master seq
        # at the end of if block arrays that count each amino acid one, two, and three positions from q
        # arrays are ordered in single letter code alphabetical order
        self.secondary_bias_finder()
        self.find_avg_occurrence()
        # self.print_q_normalized()
        return True

    #
    # def remove_spaces(self, string_to_check):
    #
    #     if " " in string_to_check:
    #         for i in range(len(string_to_check)-1):
    #             if string_to_check[i] == " " or string_to_check[i]+string_to_check[i+1] == "\n":
    #                 pass
    #             else:
    #                 return_string = string_to_check[i]
    #
    #     return return_string


    def user_set_ID(self):
        self.ID = input("Input ID:")

    def set_ID(self, ID_in):
        self.ID = ID_in

    def get_ID(self):
        return self.ID


def check_aa_entry(sequence_in):
    """`
    Ensures only natural amino acids are entered when user inputs a sequence manually.
    :param sequence_in: String of characters
    :return: True if all characters entered are natural amino acids, otherwise False
    """

    not_aa = "BJOUXZ"
    alpha = sequence_in.isalpha()
    if alpha:
        sequence_in = sequence_in.upper()
        bad_count = 0
        for i in range(0, 6):
            if not_aa[i] in sequence_in:
                bad_count = bad_count + 1
        if bad_count == 0:
            good_entry = True
        else:
            good_entry = False

    else:
        good_entry = False
    return good_entry


def print_q_normalized(secbias_in):
    if secbias_in.Q_content != 0:
        print("\n\nOne Away\t\t\t\t\t Two Away\t\t\t\t\t Three Away\t\t\t\t\t Local")
        for i in range(0, 19):
            print(secbias_in.amino_acids[i],
                  round(secbias_in.one_away_avg[i], 3), "per", secbias_in.primary_bias,
                    "\t\t\t\t", secbias_in.amino_acids[i],
                  round(secbias_in.two_away_avg[i], 3), "per", secbias_in.primary_bias,
                  "\t\t\t\t", secbias_in.amino_acids[i],
                  round(secbias_in.three_away_avg[i], 3), "per", secbias_in.primary_bias,
                  "\t\t\t\t", secbias_in.amino_acids[i],
                  round(secbias_in.local_avg[i], 3), "per", secbias_in.primary_bias)
    else:
        print("\n\nNo primary bias\n")


def create_SeqBias_object(seq_string):
    # 2D string array[i][0] --from reading csv
    # call create obj between each
    seq_object_list = []

    # convert to 2D list of ints (other than first index
    new_seq = SecondaryBias()
    seq_param_list = seq_string.split(",")
    new_seq.initialize_sec_bias(seq_param_list[0], seq_param_list[1])
    seq_object_list.append(new_seq)
    return seq_object_list


def sec_bias_to_string(obj_to_copy, list_to_copy):
    string_to_return = obj_to_copy.ID
    string_to_return += ","
    for i in range(len(list_to_copy)):
        string_to_return += list_to_copy[i]
        string_to_return += ","

    return string_to_return


def export_sec_bias_files(sequence_list):
    path = "/Users/coltongarelli/Desktop/"
    file_name = path + sequence_list[0].ID

    this_file = file_name + "one_away" + ".csv"
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].one_away, this_file)
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].one_away_avg, this_file)

    this_file = file_name + "two_away" + ".csv"
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].two_away, this_file)
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].two_away_avg, this_file)

    this_file = file_name + "three_away" + ".csv"
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].three_away, this_file)
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].three_away_avg, this_file)

    this_file = file_name + "local_seq" + ".csv"
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].local_sequence, this_file)
    for i in range(len(sequence_list)):
        write_list_to_file(sequence_list[i].ID, sequence_list[i].local_avg, this_file)

    return path + file_name


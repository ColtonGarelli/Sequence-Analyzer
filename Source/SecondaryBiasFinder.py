from typing import List

import OutputFunctions
import Representation

import abc
from OutputFunctions import sec_bias_file_o
import os
from Bio.SeqRecord import SeqRecord



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

_NO_SEQRECORD_COMPARISON = "SeqRecord comparison is deliberately not implemented. Explicitly compare the attributes of interest."


class SecondaryBias(SeqRecord):
    """
    SecondaryBias extends the SeqRecord class. SecondaryBias determines primary and secondary sequence biases.
    Is used primarily to find primary glutamine bias, and secondary
    biases at the +/- 1,2,3, and a total of these 6 positions, for each Q.

    Attributes:
        self.primary_bias:
        self.sequence_len:
        self.Q_index:
        self.Q_content:
        self.one_away:
        self.two_away:
        self.three_away:
        self.local_sequence:
        self.one_away_avg:
        self.two_away_avg:
        self.three_away_avg:
        self.local_avg:
        self.amino_acids:

    """

    def __lt__(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __le___(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __eq__(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __ne__(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __gt__(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __ge__(self, other):
        raise NotImplementedError(_NO_SEQRECORD_COMPARISON)

    def __init__(self, *args):
        super().__init__(seq=None)
        if args:
            self.seq = args
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
        self.amino_acids = "ACDEFGHIKLMNPQRSTVWY"

    # Takes user inputted sequence and ensures only natural amino acids are in seq
    # update stuff with docstrings, sequence variables
    # could also write overloaded assignment op
    # change to return true or false, and get called from secondary bias until return true
    # Write docstring below
    # elements of each array represent a single a.a., in alphabetical order (0=A, 1=C, etc)
    # each array will serve as a count for a.a. appearances near primary bias (1-2 aa)
    # localseq is the aggregate

    def update_annotations(self):
        self.annotations.update(primarybias=self.primary_bias, total_primary=self.Q_content, local_bias=self.local_avg,
                                bias_1=self.one_away, bias2=self.two_away, bias3=self.three_away)
        return self.annotations

    def initialize_sec_bias(self, seq_name, seq_in):
        """
        Effectively a constructor to create a SecondaryBias object from an id-sequence pair

        :param:seq_name: a sequence id
        :param seq_in: the sequence

        :returns: List of SecondaryBias
        """

        self.id = seq_name
        self.seq = seq_in

    def find_primary_bias(self):
        """
        Finds the primary bias defined by the user. Ignores first and last three aa in seq for primary bias calculation.
        Stores the index of each primary bias residue in the sequence string in self.primary_bias

        :returns: updates self.Q_index list (no return)
        """

        if self.primary_bias in self.seq:
            for i in range(len(self.seq)):
                if self.seq[i] == self.primary_bias:
                    # if statement should ignore Q. Could split loops so if isn't read outside
                    # the first three and last three indexes. Range b/t could be very large
                    if 2 < i < self.sequence_len-3:
                        self.Q_index.append(i)
            return True

        else:
            return False

    # should split into 5 separate methods
    def secondary_bias_finder(self):
        """
        Finds amino acids at one, two, and three residues from the desired primary bias. A local tally is also computed.

        Modified:
            self.one_away, self.two_away,self.three_away, self.three_away_avg, self.local_sequence: get updated
        """

        for i in range(self.Q_content):
            # Q_minus1 = the index in sequence_in of the a.a. to the left of the Q_index[i]
            # which refers to the index of this Q
            # in sequence_in
            Q_minus1 = self.Q_index[i] - 1
            aa_to_increment = self.amino_acid_dict[self.seq[Q_minus1]]
            self.one_away[aa_to_increment] += 1

            Q_plus1 = self.Q_index[i] + 1
            aa_to_increment = self.amino_acid_dict[self.seq[Q_plus1]]
            self.one_away[aa_to_increment] += 1

            Q_minus2 = self.Q_index[i] - 2
            aa_to_increment = self.amino_acid_dict[self.seq[Q_minus2]]
            self.two_away[aa_to_increment] += 1

            Q_plus2 = self.Q_index[i] + 2
            aa_to_increment = self.amino_acid_dict[self.seq[Q_plus2]]
            self.two_away[aa_to_increment] += 1

            Q_minus3 = self.Q_index[i] - 3
            aa_to_increment = self.amino_acid_dict[self.seq[Q_minus3]]
            self.three_away[aa_to_increment] += 1

            Q_plus3 = self.Q_index[i] + 3
            aa_to_increment = self.amino_acid_dict[self.seq[Q_plus3]]
            self.three_away[aa_to_increment] += 1

            self.local_sequence[self.amino_acid_dict[self.seq[Q_minus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.seq[Q_plus1]]] += 1
            self.local_sequence[self.amino_acid_dict[self.seq[Q_minus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.seq[Q_plus2]]] += 1
            self.local_sequence[self.amino_acid_dict[self.seq[Q_minus3]]] += 1
            self.local_sequence[self.amino_acid_dict[self.seq[Q_plus3]]] += 1

    def find_avg_occurrence(self):
        """
        Divides each index of +/- 1, 2, 3 and local lists by the total primary bias residue content (average)

        Modified:
            updates +/- 1, 2, 3, and local avg lists
        """
        if self.Q_content != 0:
            for i in range(20):
                self.one_away_avg[i] = self.one_away[i] / self.Q_content
                self.two_away_avg[i] = self.two_away[i] / self.Q_content
                self.three_away_avg[i] = self.three_away[i] / self.Q_content
                self.local_avg[i] = self.local_sequence[i] / self.Q_content

    # Consider getting rid of
    def bias_finder(self, primary_bias):
        """
        Runs the bias finding analysis. Capitalizes self.sequence string;
        calls: find_primary_bias(), secondary_bias_finder(), find_avg_occurrence()

        Modified:
            self.sequence: updated with uppercase sequence
            self.Q_content: length of self.Q_index list
            self.sequence_len:
        """

        # change user in
        # self.primary_bias = self.choose_primary_bias()
        # self.seq_in = self.prompt_sequence_input()
        # self.sequence = self.remove_spaces(self.sequence)
        self.primary_bias = primary_bias
        self.seq = self.seq[0].upper()
        self.sequence_len = len(self.seq)
        self.find_primary_bias()
        self.Q_content = len(self.Q_index)
        # indices of aa adjacent to q in master seq
        # at the end of if block arrays that count each amino acid one, two, and three positions from q
        # arrays are ordered in single letter code alphabetical order
        self.secondary_bias_finder()
        self.find_avg_occurrence()
        return True

    def set_primary_bias(self, primary_bias):
        self.primary_bias = primary_bias

    def get_primary_bias(self):
        return self.primary_bias


def seqrecord_to_secbias(seq_record: SeqRecord):
    sec_bias = SecondaryBias()
    sec_bias.features = seq_record.id


def create_SeqBias_object(seq_string):
    """
    Creates SecondaryBias objects from a sequence by splitting an id-sequence pair  (ex. "id,sequence")

    :param seq_string: "id,sequence"

    :returns: a new SecondaryBias object with id and sequence initialized to id and sequence from the in_string
    """
    # 2D string array[i][0] --from reading csv
    # call create obj between each
    # convert to 2D list of ints (other than first index
    new_seq = SecondaryBias()
    seq_param_list = seq_string.split(",")
    new_seq.initialize_sec_bias(seq_param_list[0], seq_param_list[1])
    return new_seq


def processed_data_in(general_path, file_beginning):
    """
    Creates a list of SecondaryBias objects from file.


    :param general_path:
    :param file_beginning:

    :returns: List of SecondaryBias objects
    """
    general_path = general_path + file_beginning
    one_away_list = OutputFunctions.read_file(general_path + "one_away.csv")
    two_away_list = OutputFunctions.read_file(general_path + "two_away.csv")
    three_away_list = OutputFunctions.read_file(general_path + "three_away.csv")
    local_away_list = OutputFunctions.read_file(general_path + "local_seq.csv")
    seq_object_list = []
    # convert to 2D list of ints (other than first index
    for i1 in range(len(one_away_list[0])):
        new_seq = SecondaryBias()
        new_seq.id = one_away_list[0]
        for i2 in range(0, 19):
            new_seq.one_away[i2] = float(one_away_list[i2+1])
            new_seq.two_away[i2] = float(two_away_list[i2+1])
            new_seq.three_away[i2] = float(three_away_list[i2+1])
            new_seq.local_sequence[i2] = float(local_away_list[i2+1])
        seq_object_list.append(new_seq)
    return seq_object_list


# def initialize_processed_sec_bias(id_list, seq_list, one_away, two_away, three_away, local_seq):
#     seq_obj_list = []
#     for i in range(len(seq_list)):
#         create_obj = SecondaryBias()
#         create_obj.id = id_list[i]
#     return seq_obj_list


def sec_bias_to_string(obj_to_copy, list_to_copy):
    string_to_return = obj_to_copy.id
    string_to_return += ","
    for i in range(len(list_to_copy)):
        string_to_return += list_to_copy[i]
        string_to_return += ","

    return string_to_return


def export_sec_bias_files(sequence_list):
    path = "/Users/coltongarelli/Desktop/"
    file_name = sequence_list[1].id

    this_file = file_name + "one_away" + ".csv"
    file = os.path.join(path, this_file)
    this_file = file
    # file_to_write = open(file_path, "x")
    # file_to_write.close()
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].one_away, this_file)
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].one_away_avg, this_file)

    this_file = file_name + "two_away" + ".csv"
    file = os.path.join(path, this_file)
    this_file = file
    # file_to_write = open(os.path.join(path, this_file), "x")
    # file_to_write.close()
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].two_away, this_file)
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].two_away_avg, this_file)

    this_file = file_name + "three_away" + ".csv"
    file = os.path.join(path, this_file)
    this_file = file
    # file_to_write = open(os.path.join(path, this_file), "x")
    # file_to_write.close()
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].three_away, this_file)
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].three_away_avg, this_file)

    this_file = file_name + "local_seq" + ".csv"
    file = os.path.join(path, this_file)
    this_file = file
    # file_to_write = open(os.path.join(path, this_file), "x")
    # file_to_write.close()
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].local_sequence, this_file)
    for i in range(len(sequence_list)):
        sec_bias_file_o(sequence_list[i].id, sequence_list[i].local_avg, this_file)

    return path + file_name

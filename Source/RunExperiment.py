from SecondaryBias import SequenceBias
from SecondaryBias import SequenceGroup
import json


class RunExperiment:
    file_in_path = ""
    file_out_path = ""

    def analyze_group(self, group_in):

        for i in range(len(group_in)):
            group_in[i]

        something = True

        return something

    def output_spreadsheet(self):
        something = True

        return something

    def input_spreadsheet(self, path_in):
        self.file_in_path = path_in
        experiment_list = make_groups_from_file(self.file_in_path)

    def run_experiment(self):
        something = True

        return something

    # implement later
    def fasta_parser(self):
        something = True

        return something


def read_file(path):

    sequence_file = open(path, "r")
    sequence_strings = sequence_file.readlines()
    sequence_file.close()
    print(sequence_strings)
#   sequence_strings is an array of strings. each line is one string, and one spot
#   in the array. the end of each string element is defined by \n
#   Data members are separated by , (hence csv: comma separated values).
#   Each comma notes a new textbox
    return sequence_strings


def convertToInts(string_in):

    if string_in[len(string_in) - 1] == "\n":
        string_in = string_in[len(string_in) - 1]

    return_list = string_in.split(",")
    for i in range(1, len(return_list)-1):
        return_list = int(return_list)

    return return_list


def make_groups_from_file(path):
    # 2D string array[i][0] --from reading csv
    # call create obj between each

    string_in = read_file(path)
    int_vals = []
    for i in range(len(string_in)):
        int_vals.append(convertToInts(string_in[i]))

    new_group = SequenceGroup()
    group_list = []
    for i in range(len(int_vals)):
        x = 0
        new_group.group_ID = int_vals[i][0]
        while int_vals[x][0] == int_vals[x+1][0]:
            new_seq = SequenceBias(int_vals[x][2], int_vals[x][3], int_vals[x][4])
            new_group.populate_group_list(new_seq)
            x += 1
        new_seq = SequenceBias()

        new_group.populate_group_list(new_seq)
        group_list.append(new_group)

    return group_list


def parse_to_json(obj_in):
    new_seq = json.JSONEncoder.encode()


def parse_from_json(obj_in):
    string_data = json.JSONDecoder.decode(obj_in)


def format_for_file(group_list):
    line = ""
    for i in range(len(group_list)):
        group_to_format = group_list[i]
        for i1 in range(len(group_to_format)):
            line = group_to_format.group_ID + ","
            seq_to_format = group_to_format.seq_bias_list[i]
            line += seq_to_format.ID + ","
            line += seq_to_format.primarybias + ","
            # format lists for output
            line += "\n"





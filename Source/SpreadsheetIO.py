from os.path import join


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


def convert_to_ints(string_in):

    if string_in[len(string_in) - 1] == "\n":
        string_in = string_in[len(string_in) - 1]

    return_list = string_in.split(",")
    for i in range(1, len(return_list)-1):
        return_list = int(return_list)

    return return_list


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


def write(filename):

    path = "/Users/coltongarelli/"
    name = filename + '.csv'
    try:
        file = open(join(path, name), 'w')
        file.close()

    except:
        print('Something went wrong! Cannot tell what?')


# implement later
def fasta_parser(self):
    something = True

    return something




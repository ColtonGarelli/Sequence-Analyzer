from os.path import join
from threading import Timer


def read_file(path):
    """
    Reads files in from the given path
    :param path: the full path of the desired file
    :return: a list of id,sequence formatted strings
    """
    sequence_file = open(path, "r")
    sequence_strings = sequence_file.readlines()
    sequence_file.close()
#   sequence_strings is an array of strings. each line is one string, and one spot
#   in the array. the end of each string element is defined by \n
#   Data members are separated by ,
#   Each comma notes a new cell
    return sequence_strings


def parse_to_string_list(file_string):
    """
    Formats file strings to a list of ["id","sequence"] lists (ex. [[id1, sequence1],[id2, sequence2], [id3, sequence3]]
    :param file_string: a list of "id,sequence" strings from a file
    :return: a list formatted as in the example above
    """
    new_list = []
    for i in range(len(file_string)):
        file_string[i] = file_string[i].strip("\n")
        new_list.append(file_string[i].split(","))
    # need something to do add last sequence
    return new_list


def export_sec_bias_helper(ID, copy_list, path):
    """
    Writes the file for exporting secondary bias data.
    :param ID: The id associated with the sequence being processed
    :param copy_list: a list to be written in csv format
    :param path: the file path writing to
    :return: nothing
    """
    file_to_write = open(path, "a+")
    file_to_write.write(str(ID)+",")
    for i in range(len(copy_list)):
        file_to_write.write((str(copy_list[i]) + ","))
    file_to_write.write("\n")
    file_to_write.close()


'''
********************************************************************




Scratch work below




********************************************************************
'''


# def format_for_file(group_list):
#     for i in range(len(group_list)):
#         group_to_format = group_list[i]
#         for i1 in range(len(group_to_format)):
#             line = group_to_format.group_ID + ","
#             seq_to_format = group_to_format.seq_bias_list[i]
#             line += seq_to_format.ID + ","
#             line += seq_to_format.primarybias + ","
#             # format lists for output
#             line += "\n"


# def write(filename):
#
#     path = "/Users/coltongarelli/"
#     name = filename + '.csv'
#     try:
#         file = open(join(path, name), 'w')
#         file.close()
#
#     except:
#         print('Something went wrong! Cannot tell what?')
#

# implement later
def fasta_parser():
    n = 0
    file = join("/Users/coltongarelli/", "SequenceAnalyzer/SequenceAnalyzer2.1/References/SEQUENCEANALYZER_Experiment1_inputfile_ACTUAL.csv")
    new_file =join("/Users/coltongarelli/Desktop/", "SEQUENCEANALYZER_Experiment1_inputfile_fasta.txt")
    fasta_formatted = open(new_file, 'w+')
    with open(file, 'r') as f:
        for line in f:
            split = line.split(',')
            string_to_write = '>' + split[0] + '\n' + split[1]
            fasta_formatted.write(string_to_write)

    f.close()
    fasta_formatted.close()


def convert_to_ints(string_in):

    return_list = string_in.split(",")
    for i in range(1, len(return_list)-1):
        return_list = int(return_list)
    return return_list


def remove_spaces(self, string_to_check):
    if " " in string_to_check:
        for i in range(len(string_to_check)-1):
            if string_to_check[i] == " " or string_to_check[i]+string_to_check[i+1] == "\n":
                pass
            else:
                return_string = string_to_check[i]

    return return_string

# def timer(status, url):
#         t = Timer(10, self.get_update(url))
#         t.run()
#         t.start()
#         while status != "done":
#             t.run()
#             status = t.start()
#             print(status)
#
#         t.cancel()

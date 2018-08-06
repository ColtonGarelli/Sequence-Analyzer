from os.path import join
import SecondaryBiasFinder
from Bio.SeqIO import UniprotIO
from Bio import SeqIO
import csv
import os
import pathlib

"""
Representation.py contains Representation class and UI functions

Responds to Director by:
    * Print prompts and relay responses
    * Print requested data
    * Present available options for databases, processing, viewing

Functions: 
    * Serve as UI prompts and to augment other printed/file representations

"""


# Product in builder pattern for python (see: https://gist.github.com/pazdera/1121157)
class Representation:
    """
    - Runs user interface using the UI class. May move those functions to this module (eliminate class).
    - Handles file-output. Raw data should be output as a csv file. Graphical representations may be implemented later.
    - Runs all interaction with user and computer (display/fileio)

    Attributes:
            'self.file_out_path': file out path to the desired directory
            'self.base_name': base file name to maintain consistency in output

    """
    def __init__(self):

        self.file_out_path = None
        self.base_name = None
        self.print_string = None

    def introduction(self):
        """
        Prints link to documentation and prints welcome message

        Note:
            this function may be moved to a class variable
        """
        welcome()

    def manual_sequence_entry(self):
        """
        Manages file_in entry including providing examples, links to documentation for formatting
        and passing input file path from user to director

        :returns: user inputted path
        """
        # manual_sequence_input provides link to documentation on file_in format
        self.base_name = manual_sequence_input()
        return self.base_name

    # handles calling desired DB, representing responses,
    def db_options(self):
        """
        Relays an ordered tuple to the director containing request information.
        Request information in this tuple contains keywords, query options,
        and response columns (everything needed to send a request)

        :returns: list containing database info defined in the director class

        """
        keyword = keyword_query_uniprot()
        if keyword is "":
            options = data_options()
            return options

        else:
            options = data_options()
            option_list = options.insert(0, keyword)
            return option_list

    # def manage_processed_info(self):
    #     """
    #     Prints prompts for viewing info for user
    #
    #     Returns:
    #         view type (console, file out, graphical at some point)
    #     """
    #     option = database_response_options()
    #     if option == 'file':
    #         self.file_out_path = manual_sequence_input()
    #         return option
    #     else:
    #         return option

    def output_data(self, print_or_out):
        """
        Take the string passed in and prints it or writes it to file.
        In the future, a separate function for graphing

        :param print_or_out(str): a string representing file our view

        :returns: Completion of file_out or printing (T/F)
        """
        if print_or_out == 'file':
            # add here
            return True

        elif print_or_out == 'view':
            print(self.print_string)
            return True
        return False

    def db_file_out(self, seq_list, file_string):
        """
        Handles output of a UniProt formatted xml file. In the future this method should support
        multiple data output syntax

        :param seq_list: a list of SeqRecord objects to be written to file.
        :return: success of file output
        """
        if seq_list == 'up':
            up_parser = write_uniprot_to_file(self.file_out_path)

    def set_print_string(self, new_string):
        self.print_string = new_string

    def get_print_string(self):
        return self.print_string

    def db_query_view(self):
        s = None

    def choose_database(self):
        """
        Relays which database is being accessed so Director can access that database through its builder

        :returns: database choice
        """
        db_choice = access_databases()
        if db_choice != "1":
            print("Sorry! That database hasn't been implemented.")
        else:
            return "up"


def select_fileio_directory():
        # Joins the home directior to the users typed in folder
    home = os.path.expanduser('~')
    folder_name_input = "/" + input("Please input a directory name to see if it exists at: {} ".format(home)
                        + "\nNote that searches are case sensitive\n")
    folder_check = os.path.isdir(folder_name_input)
    while not folder_check:
        print(home + folder_name_input + "  is NOT a valid directory")
        folder_name_input = input("Please input a directory name to see if it exists at: {} ".format(home)
                                  + "\nNote that searches are case sensitive\n")
    folder_path = os.path.join(home, folder_name_input)
    # Checks to see if the folder exsists
    print(folder_path + " is a valid directory.")
    return folder_path


def select_db_format():
    input_type = input("If you would like to simply import IDs and sequences for analysis, enter 1\n\n"
                       "If you would like additional information for viewing, enter 2")
    while input_type != "1" or input_type != "2":
        input_type = input("Please enter a valid response.\n\n\n"
                           "If you would like to simply import IDs and sequences for analysis, enter 1\n"
                           "If you would like additional information for viewing, enter 2")
    if input_type == "1":
        return "fasta"
    elif input_type == "2":
        return "xml"


def prompt_output_dir():
    out_path = input("Please input the full desired path for outputting files: ")


def access_databases():
    """
    Prompts user for database to get info

    Returns:
        string code for database choice
    """
    print("Enter the corresponding number to access a database:\n\n")
    database_choice = input("1. UniProt\n2. EMBL-EBI\n3. Some other one??\n\n0. Return to start")
    return database_choice


def write_uniprot_to_file(seq_record_list):
    """

    :param seq_record_list:
    :return:
    """
    try:
        with open("example.xml", "w") as output_handle:
            SeqIO.write(seq_record_list, output_handle, "xml")
            return True
    except Exception:
        return False


def write_sequence_to_file(ID, copy_list, file_name):
    """

    :param ID:
    :param copy_list:
    :param file_name:
    :return:
    """
    file_to_write = open(file_name, "a+")
    file_to_write.write(str(ID) + ",")
    for i in range(len(copy_list)):
        file_to_write.write((str(copy_list[i]) + ","))
        file_to_write.write("\n")
        file_to_write.close()


def read_file(path):
    """
    Reads files in from the given path

    :param path: the full path of the desired file
    :returns:  a list of id,sequence formatted strings
    """
    sequence_strings = ""
    with open(path, "r") as sequence_file:
        sequence_reader = csv.reader(sequence_file, delimiter=' ')
        for row in sequence_reader:
            sequence_strings = row
    sequence_file.close()
#   sequence_strings is an array of strings. each line is one string, and one spot
#   in the array. the end of each string element is defined by \n
#   Data members are separated by ,
#   Each comma notes a new cell
    return sequence_strings


def sec_bias_file_o(ID, copy_list, path):
    """
    Writes the file for exporting secondary bias data.

    :param ID: The id associated with the sequence being processed
    :param copy_list: a list to be written in csv format
    :param path: the file path writing to

    :returns: nothing
    """
    with open(path, 'w', newline='') as seq_csv_file:
        seq_writer = csv.writer(seq_csv_file, delimiter=' ')
        add_id = [ID]
        copy_list = add_id + copy_list
        for i in range(len(copy_list)):
            seq_writer.writerow(copy_list)


def parse_to_string_list(file_string):
    """
    is done automatically by csv reader. NOT NEEDED
    Formats file strings to a list of ["id","sequence"] lists (ex. [[id1, sequence1],[id2, sequence2], [id3, sequence3]]

    :param file_string: a list of "id,sequence" strings from a file

    :returns: a list formatted as in the example above
    """
    new_list = []
    for i in range(len(file_string)):
        file_string[i] = file_string[i].strip("\n")
        new_list.append(file_string[i].split(","))
    # need something to do add last sequence
    return new_list


def fasta_parser(path):
    """
    Splits fasta formatted sequences in

    Args:
        path(str): path to a csv formatted file to format to fasta

    Yields:
        outputted file in fasta format


    """
    n = 0
    file = join("/Users/coltongarelli/", "SequenceAnalyzer/SequenceAnalyzer2.1/References/SEQUENCEANALYZER_Experiment1_inputfile_ACTUAL.csv")
    new_file =join("/Users/coltongarelli/Desktop/", "SEQUENCEANALYZER_Experiment1_inputfile_fasta.txt")
    fasta_formatted = open(new_file, 'w+')
    with open(file, 'r') as f:
        # can't do for line
        # count number of >
        for line in f:
            split = line.split(',')
            string_to_write = '>' + split[0] + '\n' + split[1]
            fasta_formatted.write(string_to_write)
    f.close()
    fasta_formatted.close()


def convert_to_ints(string_in):
    """
    Converts list of string ints to int objects;

    Args:
        string_in: a string of comma separated ints

    Returns:
        return_list: a list of int objects
    """
    return_list = string_in.split(",")
    for i in range(1, len(return_list)-1):
        return_list = int(return_list)
    return return_list


# def remove_spaces(string_to_check):
#     """
#     Depreciated as manual input no longer allowed
#     :param string_to_check:
#     :return:
#     """
#
#     if " " in string_to_check or "\n" in string_to_check:
#         return_string = None
#         for i in range(len(string_to_check)-1):
#             if string_to_check[i] == " " or (string_to_check[i]+string_to_check[i+1]) == "\n":
#                 pass
#             else:
#                 return_string = string_to_check[i]
#     else:
#         return_string = string_to_check
#
#     return return_string


def welcome():
    print("Welcome to the Sequence Analyzer\n")
    print("Please refer to documentation at https://github.com/ColtonGarelli/Sequence-Analyzer/ before using.\n\n")


def main_page():
    """
    Prompts user for input source

    Returns:
        usage: string value for input source (file or database)

    """
    usage = input("\n\nWould you like to access databases (1)\n"
                  "or input by file/manually (2)\nOf course you could quit as well (0)\n\nEnter:")
    # add options for other uses. main page. should store current info somewhere during session
    # access database, return to homepage, add more from another database
    return usage





def database_response_options():
    """
    Prompts user for what they want to do with the uploaded sequences

    Returns:
        whether user wants to view, process, or output sequences to file
    """
    print("What do you want to do with the information?\n")
    database_option = input("1. View\n2. Process\n3. Output to file\n 0. Return to start")
    return database_option


def view_database_information(prepped_string):
    """
    Displays prepared string data and prompts user for limiting that data in view

    Args:
        prepped_string: a string formatted to print and be parsed for modified printing

    Yields:
        Prints views to screen
    """
    # should clear the console screen before printing
    print("Would you like to view all of the information or a subset?")
    view_option = input("1. All\n2. Some")
    view = True
    while view:

        if view_option == "1":
            print(prepped_string)
        elif view_option == "2":
            print("Sorry! Not implemented yet")
        else:
            print("wrong!")

        keep_viewing = input("Would you like to review data? (y/n)")
        if keep_viewing == "y":
            print("\n\n\n(You may want to clear the window)")
        elif keep_viewing == "n":
            view = False


def keyword_query_uniprot():
    """
    Prompts the user for Uniprot advanced search options

    Returns:
        A tuple with keys for the UniProt url constructor dictionary
    """
    query = input("Enter a keyword search or press enter to continue: ")
    return query


def data_options():
    """
    Column options for Uniprot database. Prompts user for which columns they would like to receive

    Returns:
        list containing the column options for data to be returned from UniProtKB
    """
    print("Available data options:\n")
    reviewed = input("Reviewed? (y/n)")
    print("Select columns to display: (y/n)\n")
    id = input("UniProt ID?")
    entry_names = input("Entry name?")
    protein_names = input("Protein name(s)?")
    genes = input("Genes?")
    absorption = input("Absorption?")
    temp_depend = input("Temperature dependence?")
    ph = input("pH dependence?")
    binding_site = input("Binding site?")
    dna_domain = input("DNA-binding domain?")
    redox_pot = input("Redox potential? (disulfides)")
    subunits = input("Subunits?")
    structure = input("3D structure?")
    domain = input("Domain?")
    comp_bias = input("Compositional bias(es)?")
    sequence = input("Sequence?")
    mass = input("Mass?")
    organism = "Organism?"
    limit_entries = input("Limit the number of sequences returned: ")
    offset_entries = "offset????"

    column_list = [id, protein_names, entry_names, sequence, subunits, reviewed]
    extended_column_list = [ph, mass, domain, absorption, comp_bias, temp_depend, genes,
                            binding_site, dna_domain, structure, redox_pot, organism]

    return column_list


def manual_sequence_input():
    """
    Prompts user to enter file path to upload sequence information

    Returns:
        file path for formatted input file
    """
    # Option to query sequence/id in databases????
    print("Refer to ***documentation_url*** for proper formatting\n\n")
    file_in_path = input("Please enter a file path")
    return file_in_path

    # return a tuple containing answers to options


def gene_options():
    """
    gene options
    :param self:
    :return:
    """
    print("Select the various genetic information to gather:\n")
    input("")

    # return a tuple containing answers to options
    #


def query_by_organism():
    """
    andvanced query by organism
    :return:
    """
    nothing = None


def prediction_options():
    """
    Prompts user for which predictors they would like to use

    Returns:
        Tuple containing predictors to run
    """
    print("Refer to ***Predictor documentation*** for predictor documentation" /
          "and ***local module documentation*** for local modules")
    print("Choose analysis sources: (y/n)\n")
    FELLS = input("FELLS predictor?")
    SODA = input("SODA predictor?")
    bias = input("Primary/Secondary biases?")
    return None
    # return a tuple containing answers to options


def print_secondarybias_info(seqbiasobj):

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


def prompt_sequence_input():
        """
        Prompts user to enter a sequence manually, and calls Sequence.check_aa_entry to ensure valid entry=

        :return: A valid sequence of natural amino acids as a String object
        """
        sequence_in = input('Enter an amino acid sequence ')
        good_sequence = check_aa_entry(sequence_in)
        while not good_sequence:
            sequence_in = input('Enter an amino acid sequence ')
            good_sequence = check_aa_entry(sequence_in)
        return sequence_in

# user interface functions prompts user for necessary info
# sends info to


def prompt_make_a_new_file():
    user_input = input("Enter 1 to convert fasta format to the required format\n"
                       "Enter 2 if the file is already prepared\n"
                       "Enter 0 to quit\n\n")
    while user_input != "1" and user_input != "2" and user_input != "0":
        user_input = input("Enter 1 to convert fasta format to the required format\n"
                           "Enter 2 if the file is already prepared\n"
                           "Enter 0 to quit\n\n")
    if user_input == "1":
        return "string"

    elif user_input == "2":
        return input("input the path")

    elif user_input == "0":
        return "string"

    else:
        return "string"


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


def choose_primary_bias():
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
        check_bias_entry = check_aa_entry(firstbias)
        while not check_bias_entry:
            check_bias_entry = check_aa_entry(firstbias)
    else:
        firstbias = "Q"
    return firstbias


# def print_q_normalized(secbias_in):
#     if secbias_in.Q_content != 0:
#         print("\n\nOne Away\t\t\t\t\t Two Away\t\t\t\t\t Three Away\t\t\t\t\t Local")
#         for i in range(0, 19):
#             print(secbias_in.amino_acids[i],
#                   round(secbias_in.one_away_avg[i], 3), "per", secbias_in.primary_bias,
#                     "\t\t\t\t", secbias_in.amino_acids[i],
#                   round(secbias_in.two_away_avg[i], 3), "per", secbias_in.primary_bias,
#                   "\t\t\t\t", secbias_in.amino_acids[i],
#                   round(secbias_in.three_away_avg[i], 3), "per", secbias_in.primary_bias,
#                   "\t\t\t\t", secbias_in.amino_acids[i],
#                   round(secbias_in.local_avg[i], 3), "per", secbias_in.primary_bias)
#     else:
#         print("\n\nNo primary bias\n")





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

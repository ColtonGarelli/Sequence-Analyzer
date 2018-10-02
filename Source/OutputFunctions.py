import csv
import os
from os.path import join

from Bio import SeqIO


def print_data(print_string):
    print(print_string)


def select_fileio_directory():
    home = os.path.expanduser('~')
    check_dir = home + "/" + input("Please input a directory name for data storage.\n"
                                   "Please include full path beyond: {}\n".format(home))
    folder_check = os.path.isdir(check_dir)
    while not folder_check:
        print(check_dir + "  is NOT a valid directory")
        check_dir = home + "/" + input("Please input a directory name for data storage.\n"
                                       "Please include full path beyond: {}\n".format(home))
        folder_check = os.path.isdir(check_dir)
    print(check_dir + " is a valid directory.\n")
    dir_path = os.path.join(check_dir)
    return dir_path


def select_db_format():
    input_type = input("If you would like to simply import IDs and sequences for analysis, enter 1\n\n"
                       "If you would like additional information for viewing, enter 2")
    while input_type != "1" or input_type != "2":
        input_type = input("*****Please enter a valid response.*****\n\n\n"
                           "If you would like to simply import IDs and sequences for analysis, enter 1\n"
                           "If you would like additional information for viewing, enter 2")
    if input_type == "1":
        return "fasta"
    elif input_type == "2":
        return "xml"


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
                  "or input by file/manually (2)\nOf course you could quit as well (0)\n\nEnter: ")
    # add options for other uses. main page. should store current info somewhere during session
    # access database, return to homepage, add more from another database
    while usage != "1" and usage != "2" and usage != "0":
        usage = input("\n*****Please enter a valid selection*****\n\n\nWould you like to access databases (1)\n"
                      "or input by file/manually (2)\nOf course you could quit as well (0)\n\nEnter: ")
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
        list containing keys for the column options for data to be returned from UniProtKB
        Column options in this list are keys matching the current column option dictionary (below)
        :var column_dict: = {'id': 'id', 'entry': 'entry name', 'Organism': 'organism', 'prot name': "protein name", 'seq': 'sequence', 'mass': 'mass', 'abs': 'comment(ABSORPTION)', 'pH': 'comment(PH DEPENDENCE)', 'domain': 'comment(DOMAIN)', 'comp_bias': 'feature(COMPOSITIONAL BIAS)', 'temp': 'comment(TEMPERATURE DEPENDENCE'}
    """

    print("Available data options:\n")
    print("Select columns to display (y/n)\n")
    columns = dict(ID=None, seq=None, entry_names=None, prot_names=None)
    columns['ID'] = input("UniProt ID? ")
    columns['seq'] = input("Sequence? ")
    columns['entry_names'] = input("Entry name? ")
    columns['prot_names'] = input("Protein name(s)? ")
    extended_options = input("Would you like to import more information? ")
    if extended_options == "y":
        extended_column_dict = dict(genes=None, abs=None, organism=None, mass=None, domain=None, pH=None,
                                    comp_bias=None, temp=None)
        extended_column_dict['genes'] = input("Genes? ")
        extended_column_dict['abs'] = input("Absorption? ")
        extended_column_dict['temp'] = input("Temperature dependence? ")
        extended_column_dict['pH'] = input("pH dependence? ")
        binding_site = input("Binding site? ")
        dna_domain = input("DNA-binding domain? ")
        redox_pot = input("Redox potential? (disulfides) ")
        extended_column_dict['domain'] = input("Subunits? ")
        structure = input("3D structure? ")
        domain = input("Domain? ")
        extended_column_dict['comp_bias'] = input("Compositional bias(es)? ")
        extended_column_dict['mass'] = input("Mass? ")
        extended_column_dict['organism'] = input("Organism? ")
        limit_entries = input("Limit the number of sequences returned: ")
        offset_entries = "offset????"
        columns.update(extended_column_dict)
    column_list = list()
    for i in columns:
        if columns[i] == 'y':
            column_list.append(i)
    return column_list


def manual_sequence_input():
    """
    Prompts user to enter file path to upload sequence information

    Returns:
        file path for formatted input file
    """
    # Option to query sequence/id in databases????
    home = os.path.join(os.path.expanduser('~'))
    file_dir = os.path.join("/", input("Refer to ***documentation_url*** for proper formatting\n\n"
                                       "---> If the file is in the Desktop folder, enter the file name.\n"
                                       "---> Otherwise enter the full file path beyond {}: ".format(home)))
    if "/" in file_dir:
        file_dir = os.path.join(home, "/Desktop", file_dir)
    return file_dir

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


def prompt_viewing_or_analysis():
    view_or_proc = input("Would you like to view or process the uploaded data?\nEnter 1 to view or 2 to process: ")
    while view_or_proc != '1' and view_or_proc != '2':
        view_or_proc = input("Invalid input.\n\n"
                             "Would you like to view or process the uploaded data?\nEnter 1 to view or 2 to process: ")
    if view_or_proc == '1':
        return 'v'
    elif view_or_proc == '2':
        return 'a'


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
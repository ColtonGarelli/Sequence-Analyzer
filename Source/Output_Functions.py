import csv
import os
from os.path import join

from Bio import SeqIO


def select_fileio_directory():
        # Joins the home directior to the users typed in folder
    home = os.path.expanduser('~')
    check_dir = home + "/" + input("Please input a directory name to see if it exists at: {} ".format(home)
                        + "\nNote that searches are case sensitive\n")
    folder_check = os.path.isdir(check_dir)
    while not folder_check:
        print(home + folder_check + "  is NOT a valid directory")
        folder_name_input = input("Please input a directory name to see if it exists at: {} ".format(home)
                                  + "\nNote that searches are case sensitive\n")
    # Checks to see if the folder exsists
    print(folder_check + " is a valid directory.")
    return os.path.join(home, "/" + folder_check)


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
    file_in_name = input("Please enter the file name: ")
    return file_in_name

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
import SecondaryBiasFinder


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


def access_databases():
    print("Enter the corresponding number to access a database:\n\n")
    database_choice = input("1. UniProt\n2. EMBL-EBI\n3. Some other one??\n\n0. Return to start")
    return database_choice


def database_response_options():
    print("What do you want to do with the information?\n")
    database_option = input("1. View\n2. Process\n3. Output to file\n 0. Return to start")


def view_database_information(self, prepped_string):
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


def main_page():
    usage = input("\n\nWould you like to access databases (1)\n"
                  "or input by file/manually (2)\nOf course you could quit as well (0)\n\nEnter:")
    # add options for other uses. main page. should store current info somewhere during session
    # access database, return to homepage, add more from another database
    return usage


def manual_sequence_input():
    # Option to query sequence/id in databases????
    print("Refer to ***documentation_url*** for proper formatting\n\n")
    file_in_path = input("Please enter a file path")
    return file_in_path


def keyword_query_uniprot():
    query = input("Search something: ")
    return query


def data_options(self):
    print("Available data options:\n")
    reviewed = input("Reviewed? (y/n)")
    print("Select columns to display: (y/n)\n")
    id = input("UniProt ID?")
    entry_name = input("Entry name?")
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

    # return a tuple containing answers to options


def gene_options(self):
    print("Select the various genetic information to gather:\n")
    input("")

    # return a tuple containing answers to options
    #


def query_by_organism():
    nothing = None


def prediction_options():
    print("Refer to ***Predictor documentation*** for predictor documentation" /
          "and ***local module documentation*** for local modules")
    print("Choose analysis sources: (y/n)\n")
    FELLS = input("FELLS predictor?")
    SODA = input("SODA predictor?")
    bias = input("Primary/Secondary biases?")
    return None
        # return a tuple containing answers to options


def welcome():
    print("Welcome to the Sequence Analyzer\n")
    print("Please refer to documentation at https://github.com/ColtonGarelli/Sequence-Analyzer/ before using.\n\n")


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

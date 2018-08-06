import Representation
from Builder import AnalysisBuilder, UniprotBuilder, SequenceBiasBuilder
import SecondaryBiasFinder


# room for addition of BLAST, alignment, other tools as run_x_analysis methods
# run_x_analysis methods communicate directly with self.AnalysisBuilder obj and self.DatabaseBuilder
# DatabaseBuilder and AnalysisBuilder communicate with APIs and local modules
# director also manages Representation

class Director:
    """
    The Director class manages file input, analysis, and data outputting and formatting.
        * Contains methods to execute tasks
    """
    file_in_path: str

    def __init__(self):
        """
        Creates 'representation' object to manage user interface and output


        :cvar self.analysis: each director object contains an analysis object that run the desired set of analyses
        :cvar self.representation: each director object contains an representation object to litigate data output
        :cvar self.master_list: master sequence-id list. saved after file is first read in
        :cvar self.file_in_path: path for sequence-id file in csv format
        :cvar self.file_out_path: path for directory where files can be output



        """

        self.analysis = [AnalysisBuilder]
        self.database = None
        # a list of representations
        self.representation = Representation.Representation()
        # the master sequence-id list
        self.master_list = None
        self.file_out_dir = None
        self.file_in_path = None

    def handle_manual_input(self):
        """
        Uses 'representation' to prompt user for file path and prints information to the screen


        :returns:


        """

        self.set_file_in_path(self.representation.manual_sequence_entry())

    def define_file_directory(self):
        """

        :return:
        """
        data_source = Representation.select_fileio_directory()
        return data_source

    def analysis_helper(self):
        """
        Does the work prior to analysis. Handles file-in path, creating file-out path,

        """
        slash_list = self.file_in_path.rsplit("/", 1)
        new_path = str(slash_list[0])
        self.set_file_out_dir(new_path)

    def access_databases(self):
        """

        :return:
        """

        db_choice = self.representation.choose_database()
        self.database = UniprotBuilder()
        db_options = self.representation.db_options()
        response_opts = self.database.construct_column_string(db_options)
        response_format = self.representation.select_fileio_directory()
        request_url = self.database.create_request_url(response_format, response_opts)
        response_info = self.database.make_request_get_response(request_url)
        if response_format == "xml":
            seq_list = self.database.uniprot_xml_to_seqrecord(response_info)
        elif response_format == "fasta":
            seq_list = self.database.uniprot_fasta_to_seqrecord(response_info)
        elif response_format == "tab":
            seq_list = self.database.uniprot_tab_separated_to_file(response_info)
        else:
            seq_list = None
        # database object should contain list of seqrecord objects
        # call database to make list and set master list equal to
        return seq_list

    # if view is selected, run functions that create and functions that display desired info
    def database_presentation(self):
        """

        :return:
        """
        self.representation.set_print_string(self.representation.db_query_view())
    #   print the string

    def create_sequence_objects(self, sequence_info):
        """

        :return:
        """
    # turn string formatted info to SeqRecord objects
    # put SeqRecord obj list in master list

    def run_FELLS_analysis(self):
        """

        :returns:

        """
    #   sends list of seqrecord objects to fells module
    #   while loop to check for updates
    #   director holds onto FELLS, where data is stored
    #   builder objects own data and send translations to director
        s = None

    def run_SODA_analysis(self):
        """

        :returns:
        """
        something = None

    def run_bias_analysis(self):
        """
        Reads file in and creates a master list of id-sequence lists. It then creates SecondaryBias objects and runs the
        analysis using its self.analysis object

        :returns: List of fully processed SecondaryBias objects
        """
        # for csv formatted files only. call

        # select primary bias
        # primary_bias = Representation.choose_primary_bias()
        secondary_analysis = SequenceBiasBuilder(self.master_list)
        secondary_analysis.find_sec_bias("Q")

        # file_string = Representation.read_file(self.file_in_path)
        # self.master_list = Representation.parse_to_string_list(file_string)
        # # each string in string_list represents a sequence
        #
        # sequence_list = self.analysis.build_seq_list(self.master_list)
        # processed = self.analysis.build_sec_bias()
        #
        # return processed

    def get_master_list(self):
        return self.master_list

    def set_master_list(self, new_list):
        self.master_list = new_list

    def get_file_in_path(self):
        return self.file_in_path

    def set_file_in_path(self, new_in_path):
        self.file_in_path = new_in_path

    def get_file_out_dir(self):
        return self.file_out_dir

    def set_file_out_dir(self, new_out_dir):
        self.file_out_dir = new_out_dir


def check_input_method(input):
    if input == 'up' or input == 'file':
        return True
    else:
        return False

import Representation
from Builder import AnalysisBuilder, DatabaseBuilder


# room for addition of BLAST, alignment, other tools as run_x_analysis methods
# run_x_analysis methods communicate directly with self.AnalysisBuilder obj and self.DatabaseBuilder
# DatabaseBuilder and AnalysisBuilder communicate with APIs and local modules
# director also manages Representation

class Director:
    """
    The Director class manages file input, analysis, and data outputting and formatting.
    """
    def __init__(self):
        """
        :var self.analysis: each director object contains an analysis object that run the desired set of analyses
        :var self.representation: each director object contains an representation object to litigate data output
        :var self.master_list: master sequence-id list. saved after file is first read in
        :var self.file_in_path: path for sequence-id file in csv format
        :var self.file_out_path: path for directory where files can be output

        Analysis and representation objects are instantiated and set to self.analysis and self.representation variables.
        """

        self.analysis = AnalysisBuilder()
        self.database = DatabaseBuilder()
        # a list of representations
        self.representation = Representation.Representation()
        # the master sequence-id list
        self.master_list = None
        self.file_out_dir = None
        self.file_in_path = None

    def handle_manual_input(self):
        something = None

    def handle_file_input(self):
        something = None

    def define_input_source(self):
        something = None

    def analysis_helper(self, in_path):
        """
        Does the work prior to analysis. Handles file-in path, creating file-out path,

        """
        self.set_file_in_path(in_path)
        slash_list = self.file_in_path.rsplit("/", 1)
        new_path = str(slash_list[0])
        self.set_file_out_dir(new_path)

    def access_databases(self):
        something = None
    #  call representation methods that ask which DB, what to do with the data and stores that

    # if view is selected, run functions that create and functions that display desired info
    def database_presentation(self):
        something = None

    def create_sequence_objects(self):
        something = None
    # turn string formatted info to SeqRecord objects
    # put SeqRecord obj list in master list

    def run_FELLS_analysis(self):
        something = None

    def run_SODA_analysis(self):
        something = None

    def run_bias_analysis(self):
        """
        Reads file in and creates a master list of id-sequence lists. It then creates SecondaryBias objects and runs the
        analysis using its self.analysis object
        :return: List of fully processed SecondaryBias objects
        """
        file_string = Representation.read_file(self.file_in_path)
        self.master_list = Representation.parse_to_string_list(file_string)
        # each string in string_list represents a sequence

        sequence_list = self.analysis.build_seq_list(self.master_list)
        processed = self.analysis.build_sec_bias()

        return processed

    # for gui stuff
    def create_representation(self):
        """
        Uses the self.representation object to create a graphic representation of the data processed during analysis.
        :return: N/A


        ***Not implemented yet***
        """
        pass

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

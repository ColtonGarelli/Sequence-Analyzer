import Representation
from SecondaryBiasFinder import SequenceImpl, SecondaryBias
import UserInterface
from Builder import AnalysisBuilder


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
        # a list of representations
        self.representation = Representation.Representation()
        # the master sequence-id list
        self.master_list = None
        self.file_out_path = None
        self.file_in_path = None

    def analysis_helper(self, in_path):
        """
        Does the work prior to analysis. Handles file-in path, setting file-out path,

        """
        self.file_in_path = in_path
        slash_list = self.file_in_path.rsplit("/", 1)
        new_path = str(slash_list[0])
        self.file_out_path = new_path

    def run_analysis(self):
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

    def create_representation(self):
        """
        Uses the self.representation object to create a graphic representation of the data processed during analysis.
        :return: N/A


        ***Not implemented yet***
        """
        pass
from SecondaryBiasFinder import SequenceImpl, SecondaryBias
import SecondaryBiasFinder, SpreadsheetIO
import abc
import UserInterface


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

        self.analysis = AnalysisImpl()
        # a list of representations
        self.representation = Representation()
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
        file_string = SpreadsheetIO.read_file(self.file_in_path)
        self.master_list = SpreadsheetIO.parse_to_string_list(file_string)
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


class Representation:
    """
    Handles file-output. Raw data should be output as a csv file. Graphical representations may be implemented later.
    :var self.file_out_path: file out path to the desired directory
    :var self.base_name: base file name to maintain consistency in output
    """
    def __init__(self):
        self.file_out_path = ""
        self.base_name = None

    def write_to_file(self, ID, copy_list, file_name):
        file_to_write = open(file_name, "a+")
        file_to_write.write(str(ID) + ",")
        for i in range(len(copy_list)):
            file_to_write.write((str(copy_list[i]) + ","))
            file_to_write.write("\n")
            file_to_write.close()


class Analysis(abc.ABCMeta):

    @abc.abstractmethod
    def build_list_from_file(self):
        raise NotImplementedError

    @abc.abstractmethod
    def build_sec_bias(self):
        raise NotImplementedError

    @abc.abstractmethod
    def build_prediciton_A(self):
        raise NotImplementedError

    @abc.abstractmethod
    def build_prediction_B(self):
        raise NotImplementedError


class AnalysisImpl:
    def __init__(self):
        """
        :var self.seq_list: a list of Sequence objects instantiated from file
        """
        super(AnalysisImpl, self).__init__()
        self.seq_list = []

    def build_seq_list(self, sequence_list):
        """
        Builds self.seq_list which can then be used to create the other objects
        :param sequence_list:
        :return:
        """
        new_list = []
        for i1 in range(len(sequence_list)):
            new_obj = SequenceImpl()
            temp_str = sequence_list[i1]
            new_obj.initialize_sequence_object(temp_str[0], temp_str[1])
            new_list.append(new_obj)

        self.seq_list = new_list
        return new_list

    def build_list_from_file(self):
        """
        Takes a fasta formatted file, creates csv formatted file with id-sequence info.
        :return:
        """
        pass

    def build_prediciton_A(self):
        """
        For one of the APIs
        :return:
        """
        pass

    def build_prediction_B(self):
        """
        For the other API
        :return:
        """
        pass

    def build_sec_bias(self):
        """
        Creates a list of SecondaryBias objects from self.seq_list. The list of SecondaryBias objects is then processed.
        :return: a list of processed SecondaryBias objects ready for output
        """
        return_list = []
        new_list = []
        for i1 in range(len(self.seq_list)):
            new_obj = SecondaryBias()
            temp_obj = self.seq_list[i1]
            new_obj.initialize_sec_bias(str(temp_obj.get_id()), str(temp_obj.get_sequence()))
            new_list.append(new_obj)

        for i2 in range(len(new_list)):
            finding = new_list[i2]
            done = new_list[i2].bias_finder()
            return_list.append(finding)

        return return_list


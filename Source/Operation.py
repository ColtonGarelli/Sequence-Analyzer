from SecondaryBiasFinder import Sequence, SecondaryBias
import SecondaryBiasFinder, SpreadsheetIO
import abc


class Director:

    def __init__(self):
        self._sequence = None

    def run_analysis(self, analyze):
        self._sequence = analyze
        processed = self._sequence.build_sec_bias()

        return processed


class Representation:

    def __init__(self):
        self.file_out_path = ""

    def write_to_file(self):
        something = 0


class Analysis(abc.ABCMeta):

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
    def __init__(self, path_in):
        super(AnalysisImpl, self).__init__()
        self.file_in = path_in
        self.file_out_path = ""
        self.seq_list = []

    def build_list_from_file(self):
        pass

    def build_prediciton_A(self):
        pass

    def build_prediction_B(self):
        pass

    def build_sec_bias(self):
        file_string = SpreadsheetIO.read_file(self.file_in)
        # each string in string_list represents a sequence
        string_list = SpreadsheetIO.parse_to_string_list(file_string)
        sequence_list = []
        for i in range(len(string_list)):
            sequence_list.extend(SecondaryBiasFinder.create_SeqBias_object(string_list[i]))
        return_list = []
        for i1 in range(len(sequence_list)):
            finding = sequence_list[i1]
            done = finding.bias_finder()
            return_list.append(finding)

        return return_list

# builder class
import abc
from SecondaryBiasFinder import SequenceImpl, SecondaryBias


class Builder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def build_list_from_file(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_sequence_list(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_sequence_list(self, new_list):
        raise NotImplementedError


    # @abc.abstractmethod
    # def build_sec_bias(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def build_prediciton_A(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def build_prediction_B(self):
    #     raise NotImplementedError


class AnalysisBuilder(Builder):
    def __init__(self):
        """
        :var self.seq_list: a list of Sequence objects instantiated from file
        """
        super(AnalysisBuilder, self).__init__()
        self.seq_list = []

    def get_sequence_list(self):
        return self.seq_list

    def set_sequence_list(self, new_list):
        self.seq_list = new_list

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

        self.set_sequence_list(new_list)
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


class DatabaseBuilder(Builder):

    def __init__(self):
        super(DatabaseBuilder, self).__init__()



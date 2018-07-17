# builder class
import abc
from SecondaryBiasFinder import Sequence, SecondaryBias
import SecondaryBiasFinder


class Builder(metaclass=abc.ABCMeta):
    """
    Builder is an abstract class that serves as a template for building database responses and analyses

    """

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


        Variables:
            self.sec_bias_list: a list of Sequence objects instantiated from file


        """
        super(AnalysisBuilder, self).__init__()
        self.sec_bias_list = []

    def get_sequence_list(self):
        return self.sec_bias_list

    def set_sequence_list(self, new_list):
        self.sec_bias_list = new_list

    def build_sec_bias_list(self, sequence_list):
        """
        Builds self.sec_bias_list which can then be used to create the other objects
        Args:

            sequence_list:

        Returns:
            List of SecondaryBias
        """
        new_list = []
        for i1 in range(len(sequence_list)):
            new_obj = SecondaryBias()
            temp_str = sequence_list[i1]
            new_obj.initialize_sequence_object(temp_str[0], temp_str[1])
            new_list.append(new_obj)
        self.set_sequence_list(new_list)
        return new_list

    def build_list_from_file(self):
        """
        Takes a fasta formatted file, creates csv formatted file with id-sequence info.

        Returns:

        """
        pass

    def build_prediciton_A(self):
        """
        For one of the APIs

        Returns:

        """
        pass

    def build_prediction_B(self):
        """
        For the other API

        Returns:

        """
        pass

    def build_sec_bias(self):
        """
        Creates a list of SecondaryBias objects from self.sec_bias_list. The list of SecondaryBias objects is then processed.

        Returns:
            a list of processed SecondaryBias objects ready for output
        """
        s = None


class SequenceBiasBuilder(AnalysisBuilder):

    def __init__(self, seq_record_list):
        """


        """
        super(SequenceBiasBuilder, self).__init__()
        self.sec_bias_list = seq_record_list

    def find_sec_bias(self, primary_bias):

        for i in self.sec_bias_list:
            i.set_primary_bias = primary_bias
            i.bias_finder()


class DatabaseBuilder(Builder):
    """


    """

    def __init__(self):
        """

        Args:

        Returns:
        """
        super(DatabaseBuilder, self).__init__()


# -*- coding: utf-8 -*-
# builder class
import abc
import csv
import json
import os

import requests as r
from Bio import SeqIO

from SecondaryBiasFinder import SecondaryBias


class Builder(metaclass=abc.ABCMeta):
    """
    Builder is an abstract class that serves as a template for building database responses and analyses

    """
    #
    # @abc.abstractmethod
    # def build_list_from_file(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get_sequence_list(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def set_sequence_list(self, new_list):
    #     raise NotImplementedError


class AnalysisBuilder(Builder):

    def __init__(self):
        """


        :param: self.sec_bias_list: a list of Sequence objects instantiated from file
        """
        super(AnalysisBuilder, self).__init__()


class FELLSAnalysisBuilder(AnalysisBuilder):
    _base_url = "http://protein.bio.unipd.it/fellsws"
    _post_url = "http://protein.bio.unipd.it/fellsws/submit"
    _status_url = "http://protein.bio.unipd.it/fellsws/status/"
    _get_url = "http://protein.bio.unipd.it/fellsws/results/"
    _headers = {'Content-Type': 'application/json'}
    _body_beginning = '\nContent-Disposition: application/json; name="sequence"'

    def __init__(self):
        """

        """
        super(FELLSAnalysisBuilder, self).__init__()
        self.job_id: str = None

    def prepare_request_object(self, seq_id_list):
        new_session = r.Session()
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        body = {"sequence": seq_id_list[0]}
        json_body = json.dumps(body).encode('utf-8')
        with open('/Users/coltongarelli/Desktop/uniprotxmltest.fasta', 'rU') as fasta:
            response = new_session.request(method='POST', url=self._post_url, headers=headers, data=body)
        json_obj = json.loads(response.content)
        self.job_id = json_obj.get('jobid')
        print(self.job_id)
        return self.job_id

    def check_request_status(self, ID):
        check_status = r.get(url=self._status_url+ID)
        json_obj = json.loads(check_status.content)
        return json_obj

    def retrieve_response_data(self, ID):

        request_data = r.get(self._get_url+ID)
        return request_data.content

    def prep_for_file_output(self):
        pass

    def prep_for_viewing(self):
        pass


class SODAAnalysisBuilder(AnalysisBuilder):
    """

    """
    _post_url = "http://protein.bio.unipd.it/sodaws/submitsoda"
    _status_url = "http://protein.bio.unipd.it/sodaws/status/"
    _get_url = "http://protein.bio.unipd.it/sodaws/result/"

    def __init__(self):
        """

        """
        super(SODAAnalysisBuilder, self).__init__()
        self.job_id: str = None
        self.file_path = '/Users/coltongarelli/Desktop/uniprotxmltest.fasta'
        self.json_obj = None  # a json dictionary

    def submit_job_request(self, seq_in):
        body = {"sequence": seq_in}
        response = r.request(method='POST', url=self._post_url, data=body)
        json_obj = json.loads(response.content)
        self.job_id = json_obj.get('jobid')
        return self.job_id

    def check_request_status(self, ID):
        check_status = r.get(url=self._status_url+ID)
        json_obj = json.loads(check_status.content)
        return json_obj

    def retrieve_response_data(self, ID):
        request_data = r.get(self._get_url+ID)
        request_str = request_data.content.decode('utf-8')
        json_obj = json.loads(request_str)
        return json_obj

    def prep_for_file_output(self, json_format_obj):
        pass

    def prep_for_viewing(self):
        pass


class SequenceBiasBuilder(AnalysisBuilder):

    def __init__(self, seq_record_list):
        """


        """
        super(SequenceBiasBuilder, self).__init__()
        self.sec_bias_list = []
        for i in range(len(seq_record_list)):
            sec_bias = SecondaryBias()
            sec_bias.id = seq_record_list[i][0]
            sec_bias.seq = seq_record_list[i][1]
            self.sec_bias_list.append(sec_bias)

    def find_sec_bias(self, primary_bias):

        for i in range(len(self.sec_bias_list)):
            self.sec_bias_list[i].set_primary_bias(primary_bias)
            self.sec_bias_list[i].bias_finder(primary_bias)


class DatabaseBuilder(Builder):
    """


    """
    def __init__(self):
        super(DatabaseBuilder, self).__init__()


class UniprotBuilder(DatabaseBuilder):
    """


    """
    _base_url = "https://www.uniprot.org/uniprot/?query="
    url_extension = "&limit=100&format="
    column_dict = {'id': 'id', 'entry': 'entry name', 'Organism': 'organism', 'prot name': "protein name",
                   'seq': 'sequence', 'mass': 'mass', 'abs': 'comment(ABSORPTION)', 'pH': 'comment(PH DEPENDENCE)',
                   'domain': 'comment(DOMAIN)', 'comp bias': 'feature(COMPOSITIONAL BIAS)',
                   'temp': 'comment(TEMPERATURE DEPENDENCE'}

    def __init__(self):
        """

        :param:

        :returns:
        """
        super(UniprotBuilder, self).__init__()
        self.request_url = None
        self.keyword = None

    def get_base_url(self):
        return self._base_url

    def construct_column_string(self, columns):
        column_string = "&columns=reviewed"
        for i in columns:
            if i in self.column_dict:
                column_string += (',' + self.column_dict[i])
        return column_string

    def create_request_url(self, response_format, column_string):
        self.request_url = self.get_base_url() + response_format + column_string + self.url_extension
        return self.request_url

    def make_request_get_response(self, search_url):
        new_request = r.get(search_url)
        return new_request.content.decode('utf-8')

    def uniprot_fasta_to_seqrecord(self, uniprot_fasta):
        seq_record_list = []
        if isinstance(uniprot_fasta, str):
            with open(os.path.join('/Users/coltongarelli/Desktop/uniprotxmltest-fasta.txt'), 'a') as h:
                h.write(uniprot_fasta)
                for record in SeqIO.parse("/Users/coltongarelli/Desktop/uniprotxmltest-fasta.txt", 'fasta'):
                    seq_record_list.append(record)
            return seq_record_list
        else:
            return None

    def uniprot_xml_to_seqrecord(self, uniprot_xml):
        seq_record_list = []
        if isinstance(uniprot_xml, str):
            with open('/Users/coltongarelli/Desktop/uniprotxmltest.xml', 'a') as h:
                h.write(uniprot_xml)
                for record in SeqIO.parse("/Users/coltongarelli/Desktop/uniprotxmltest.xml", 'uniprot-xml'):
                    seq_record_list.append(record)
            h.close()
        else:
            return None
        return seq_record_list

    def uniprot_tab_separated_to_file(self, uniprot_tab):
        with open('/Users/coltongarelli/Desktop/uniprotxmltest.txt', 'a') as f:
            csv.writer(f, delimiter='\t')
            f.write(uniprot_tab)
        return

    def seq_record_to_uniprot_xml(self, seq_record):
        with open('/Users/coltongarelli/Desktop/uniprotxmltest.xml', 'a') as sr_file:
            pass

    def prep_uniprot_output(self, seq_list):
        output_string: str
        SeqIO.write(seq_list, output_string, "xml")
        return output_string

# class Super_TabIO(SeqIO.TabIO):
#     def __init__(self):
#         super(Super_TabIO, self).__init__()
#


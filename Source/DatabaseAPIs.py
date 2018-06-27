import abc
from Bio.SeqIO import UniprotIO
import sys, requests


class DatabaseRequests(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_request_url(self, query, param_list): raise NotImplementedError

    @abc.abstractmethod
    def make_database_query(self): raise NotImplementedError

    @abc.abstractmethod
    def check_for_updates(self): raise NotImplementedError

    @abc.abstractmethod
    def create_sequence_object(self): raise NotImplementedError

#   returns a tuple (ID, sequence)
    def fasta_parser(self, fasta_string):
        split_string = fasta_string.split("\n")
        id_stirng = split_string[0]
        seq_string = split_string[1]
        prot_tuple = (id_stirng, seq_string)
        return prot_tuple


class ebiDatabase(DatabaseRequests):
    def __init__(self):
        super(ebiDatabase, self).__init__()
        self.something = None

    def create_request_url(self, query, param_list):
        self.something = None

    def make_database_query(self):
        self.something = None

    def check_for_updates(self):
        self.something = None

    def create_sequence_object(self):
        self.something = None


class UniProtDatabase(DatabaseRequests):
    base_url = "https://www.uniprot.org/uniprot/?query=reviewed:yes"
    column_options = dict(query="query")

    def __init__(self):
        super(UniProtDatabase, self).__init__()

    def create_request_url(self, query, param_list):
        """
        Creates a URL based on user input for desired sequence parameters.
        :return:
        """
        # to get return as fasta for specific entry


    def make_database_query(self):
        request_parser = UniprotIO.Parser()

    def check_for_updates(self):
        pass

    def create_sequence_object(self):
        pass

    def testthings(self):
        requestURL = "https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&reviewed=true&keywords=keywordsearch&protein=protein%20name&seqLength=10000"

        r = requests.get(requestURL, headers={"Accept": "application/xml"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        responseBody = r.text
        print(responseBody)
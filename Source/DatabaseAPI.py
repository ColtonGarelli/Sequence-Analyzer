from abc import ABCMeta


class DatabaseAPI(ABCMeta):

    @abs
    def create_request_url(cls, query, param_list): raise NotImplementedError

    @abs
    def make_database_query(cls): raise NotImplementedError

    @abs
    def check_for_updates(cls): raise NotImplementedError

    @abs
    def create_sequence_object(cls): raise NotImplementedError

#   returns a tuple (ID, sequence)
    def fasta_parser(self, fasta_string):
        split_string = fasta_string.split("\n")
        id_stirng = split_string[0]
        seq_string = split_string[1]
        prot_tuple = (id_stirng, seq_string)
        return prot_tuple


class UniProtDatabase(DatabaseAPI):
    base_url = "https://www.uniprot.org/uniprot/?query=reviewed:yes"
    column_options = dict(query="query")

    def __init__(self):
        super(UniProtDatabase, self).__init__(self)

    def create_request_url(self, query, param_list):
        """
        Creates a URL based on user input for desired sequence parameters.
        :return:
        """
        # to get return as fasta for specific entry
        as_fasta = "https://www.uniprot.org/uniprot/P12345.fasta"
        base_url = "https://www.uniprot.org/uniprot/?query="
        query_url = {"something": "url text", "something else": "another url"}
        # determines what info is returned in response element
        column_url = {"ID": "a column with useful info"}
        format_url = "&format=fasta"

        example_url = "https://www.uniprot.org/uniprot/?query=insulin&" \
                      "sort=score&columns=id,protein names,length&format=tab"

        another_url = "http://www.uniprot.org/uniprot/?query=arabidopsis%20thaliana&sort=score&" \
                      "columns=id,protein names,&format=tab"

        ebi_url = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&protein=Auxin%20Response%20Factor"

        # this_request = requests.get(another_url)
        # print(this_request.text)
        #
        # url = "https://www.uniprot.org/uniprot/?query=insulin&sort=score&columns=entry name,protein names,length&format=tab"
        # request = requests.get(url)
        # print(request.text)
    def make_database_query(self):
        pass

    def check_for_updates(self):
        pass

    def create_sequence_object(self):
        pass


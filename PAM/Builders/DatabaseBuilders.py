import requests as r
from Bio import SeqIO

from InputOutput import File_IO
import os



class DatabaseBuilder:
    """


    """
    def __init__(self):
        pass


class UniprotBuilder(DatabaseBuilder):
    """


    """
    _base_url = "https://www.uniprot.org/uniprot/?query="
    column_dict = {'ID': 'id', 'entry': 'entry name', 'Organism': 'organism', 'prot name': "protein name",
                   'seq': 'sequence', 'mass': 'mass', 'abs': 'comment(ABSORPTION)', 'pH': 'comment(PH DEPENDENCE)',
                   'domain': 'comment(DOMAIN)', 'comp_bias': 'feature(COMPOSITIONAL BIAS)',
                   'temp': 'comment(TEMPERATURE DEPENDENCE'}

    def __init__(self):
        """

        :param:

        :returns:
        """
        super(UniprotBuilder, self).__init__()
        self.request_url = None
        self.keyword = None
        self.limit = "&limit="
        # TODO: set format = fasta if just for sequence processing, or as xml for more info
        self.format = "&format="

    def get_base_url(self):
        return self._base_url

    def construct_column_string(self, columns):
        column_string = columns[0] + "&columns=reviewed"
        for column in columns:
            if column in self.column_dict.keys():
                column_string += (',' + self.column_dict[column])
        return column_string

    def create_request_url(self, response_format, column_string, limit):
        self.request_url = self.get_base_url() + column_string + ('&limit=' + limit) + ('&format=' + response_format)
        return self.request_url

    def make_request_get_response(self, search_url):
        new_request = r.get(search_url)
        return new_request.content.decode('utf-8')

    def uniprot_to_seqrecord(self, data, storage_dir, data_format):
        if data_format == 'fasta':
            file_extension = '.faa'
        else:
            file_extension = '.xml'
        file_name = File_IO.make_original_file_name(file_out_dir=storage_dir,
                                                    file_name="uniprot_data", file_extension=file_extension)
        with open(file_name, 'w+') as file:
            file.write(data)
        seq_record_list = list()
        with open(file_name, 'rU') as file:
            for sequence in SeqIO.parse(file, data_format):
                seq_record_list.append(sequence)
        return seq_record_list

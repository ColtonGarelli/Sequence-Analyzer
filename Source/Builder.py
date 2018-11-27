# -*- coding: utf-8 -*-
# builder class
import json
import os
import time
import requests as r
from Bio import SeqIO, SeqRecord, Seq
from Bio.Alphabet import IUPAC
from SecondaryBiasFinder import SecondaryBias
import File_IO


class Builder:
    """
    Builder is a class that serves as a template for building database responses and analyses

    """
    @staticmethod
    def create_seqrecord_object_from_csv(seq_string):
        seq_param_list = seq_string.split(",")
        seq_list = []
        for i in range(len(seq_param_list)):
            new_seq = SeqRecord.SeqRecord(seq=seq_param_list[i])
            i += 1
            new_seq.id = seq_param_list[i]
            seq_list.append(new_seq)
        return seq_list


class AnalysisBuilder(Builder):

    def __init__(self):
        """


        :param: self.sec_bias_list: a list of Sequence objects instantiated from file
        """
        super(AnalysisBuilder, self).__init__()

    @staticmethod
    def send_request(post_url, headers, json_body):
        response = r.post(url=post_url, headers=headers, data=json_body)
        json_obj = json.loads(response.content.decode())
        job_id = json_obj.get('jobid')
        return job_id

    @staticmethod
    def get_jobid(response_str):
        json_content = json.loads(response_str.content.decode('utf-8'))
        return json_content['jobid']

    @staticmethod
    def get_data_as_json(response_str):
        return json.loads(response_str.content.decode('utf-8'))


# ***MAX # of sequences = 15000
class FELLSAnalysisBuilder(AnalysisBuilder):
    _base_url = "http://protein.bio.unipd.it/fellsws"
    _post_url = "http://protein.bio.unipd.it/fellsws/submit"
    _status_url = "http://protein.bio.unipd.it/fellsws/status/"
    _get_url = "http://protein.bio.unipd.it/fellsws/result/"
    _headers = {'Content-Type': 'application/json; charset=utf-8'}
    _body_beginning = '\nContent-Disposition: application/json; name="sequence"'

    def __init__(self):
        """

        """
        super(FELLSAnalysisBuilder, self).__init__()
        self.job_id: str = None

    def prepare_request(self, seq_list):
        working_list = self.sequence_list_to_fasta(seq_list)
        formatted = self.format_body_for_processing(working_list)
        json_body = json.dumps({"sequence": formatted}).encode()
        prepped_request = r.Request(method='POST', url=self.get_submission_url(),
                                    headers=self.get_headers(), data=json_body).prepare()
        return prepped_request

    @staticmethod
    def sequence_list_to_fasta(seq_list: list):
        working_list = list()
        if isinstance(seq_list[0], SeqRecord.SeqRecord):
            try:
                for i in range(len(seq_list)):
                    minimal_id = seq_list[i].id.split('|')
                    seq_list[i].id = minimal_id[1]
                    seq_list[i].description = ""
                    working_list.append(seq_list[i].format("fasta"))
            except TypeError as type_e:
                for i in range(len(seq_list)):
                    working_list[i].seq = Seq.Seq(data=working_list[i].seq, alphabet=IUPAC.IUPACProtein())
                    working_list[i] = working_list[i].format("fasta")
        elif isinstance(seq_list[0], str):
            try:
                for record in seq_list:
                    working_list.append(SeqIO.parse(record, "fasta", Seq.Alphabet.generic_protein))
            except:
                pass
            for i in range(len(seq_list)):
                temp_seqrecord = SeqRecord.SeqRecord(description="", id="ID_{}".format(i), seq=Seq.Seq(seq_list[i]))
                working_list.append(temp_seqrecord.format("fasta"))
        return working_list

    @staticmethod
    def format_body_for_processing(fasta_str_list):
        formatted = fasta_str_list[0]
        for i in fasta_str_list[1:]:
            if "\n\n>" not in i:
                if "\n>" in i:
                    formatted = "\n" + formatted + i
                else:
                    formatted = formatted + "\n\n" + i
            else:
                formatted = formatted + i
        return formatted + "\n"

    def check_request_submission(self, jobid):
        check_status = r.get(url=self._status_url+jobid)
        json_obj = json.loads(check_status.content)
        if json_obj.get('status') != 'error':
            while json_obj.get('status') != 'done':
                time.sleep(2.00)
                check_status = r.get(url=self._status_url + jobid)
                json_obj = json.loads(check_status.content)
            return check_status
        else:
            return False

    def check_processing_status(self, ID):
        processing = r.get(self._get_url+ID)
        processing = json.loads(processing.content)
        while processing['status'] == 'running':
            time.sleep(2.00)
            processing = r.get(self._get_url + ID)
            processing = json.loads(processing.content)
        if processing['status'] == 'done':
            return True
        else:
            return False

    def retrieve_response_data(self, id_list):
        return_data = []
        temp_list = list()
        for i in id_list:
            temp_list.append(r.get(self._get_url + i))
        for i in temp_list:
            return_data.append(i.content)
        return return_data

    @staticmethod
    def update_annotations(master_list, data_list):
        # TODO: a more concise method for this operation
        for i in range(len(master_list)):
            all_list = data_list[i]['all']
            comp = all_list["composition"]
            entropy = all_list['entropy']
            hydrophobic = all_list['hyd']
            pos_charge = all_list['pos']
            neg_charge = all_list['neg']
            hydro_cluster = data_list[i]['hca']
            percent_dis = data_list[i]['p_dis']
            percent_helix = data_list[i]['p_h']
            percent_coil = data_list[i]['p_c']
            order_disorder = data_list[i]['state_dis']
            aggregation = data_list[i]['pasta_energy']
            # comp is a list of dictionaries for each domain
            # all the above are lists of per residue

            # complexity
            # for i in master_list:
            #     i.letter_annotations.update({'entropy': entropy})

            master_list[i].annotations.update({'entropy': entropy})
            master_list[i].annotations.update({'pos_charge': pos_charge})
            master_list[i].annotations.update({'neg_charge': neg_charge})
            master_list[i].annotations.update({'hydro_cluster': hydro_cluster})
            master_list[i].annotations.update({'percent_dis': percent_dis})
            master_list[i].annotations.update({'percent_helix': percent_helix})
            master_list[i].annotations.update({'percent_coil': percent_coil})
            master_list[i].annotations.update({'hydro': hydrophobic})
            # comp has to do with at least charge
            master_list[i].annotations.update({'composition': comp})
            master_list[i].annotations.update({'aggregation': aggregation})
            master_list[i].annotations.update({'order_disorder': order_disorder})
            try:
                pfam = data_list[i]['pfam']
                master_list[i].annotations.update({'pfam': pfam})
            except KeyError as e:
                pass
        return master_list

    def prep_for_file_output(self, seq_record_list):

        pass

    def prep_for_viewing(self):
        pass

    def get_submission_url(self):
        return self._post_url

    def get_processed_data_url(self):
        return self._get_url

    def get_status_url(self):
        return self._status_url

    def get_headers(self):
        return self._headers


class SODAAnalysisBuilder(AnalysisBuilder):
    """

    """
    _post_url = "http://protein.bio.unipd.it/sodaws/submitsoda"
    _status_url = "http://protein.bio.unipd.it/sodaws/status/"
    _get_url = "http://protein.bio.unipd.it/sodaws/result/"

    def __init__(self):
        """

        """
        super().__init__()
        self.job_id: str = None
        self.json_obj = None  # a json dictionary

    def prepare_request_object(self, seq):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        body = {"sequence": seq}
        json_body = json.dumps(body)
        prepped_request = r.Request(method='POST', url=self.get_post_url(), headers=headers, data=json_body).prepare()
        return prepped_request

    def check_request_status(self, ID):
        check_status = r.get(url=self._status_url+ID)
        json_obj = json.loads(check_status.content)
        while json_obj.get('status') != 'done':
            time.sleep(3.00)
            check_status = r.get(url=self._status_url + ID)
            json_obj = json.loads(check_status.content)
        return json_obj

    def retrieve_response_data(self, ID):
        filter = "?filter={\"parsed_soda_output\": 1}"
        request_data = r.get(self._get_url+ID+filter)
        request_str = request_data.content.decode('utf-8')
        return request_str

    @staticmethod
    def update_annotations(seqrecord, json_info):
        try:
            json_info = json.loads(json_info)
            if json_info is not dict:
                json_info = json.loads(json_info)
        except TypeError as e:
            pass
        try:
            seq_data = json_info["parsed_soda_output"]["MySequence"]
            seq_data.pop('title')
            seqrecord.annotations.update(seq_data)
            return seqrecord

        except KeyError as key_e:
            print('oopsies! error accessing data from SODA!!\n\n{}'.format(key_e.__cause__))

    def prep_for_file_output(self, json_format_obj):
        pass

    def prep_for_viewing(self):
        pass

    def get_post_url(self):
        return self._post_url


class SequenceBiasBuilder(AnalysisBuilder):

    def __init__(self):
        """


        """
        super().__init__()
        self.id_seq = dict()
        self.prim_indices = dict()
        self.one_away = dict()
        self.two_away = dict()
        self.three_away = dict()
        self.local_sequence = dict()
        self.one_away_avg = dict()
        self.two_away_avg = dict()
        self.three_away_avg = dict()
        self.local_avg = dict()
        self.amino_acid_dict = dict(A=0, C=1, D=2, E=3, F=4, G=5, H=6, I=7, K=8, L=9,
                                    M=10, N=11, P=12, Q=13, R=14, S=15, T=16, V=17, W=18, Y=19)
        self.primary_bias: str
        self.amino_acids = "ACDEFGHIKLMNPQRSTVWY"

    @staticmethod
    def primary_bias_finder(seq, primary_bias='Q'):
        """
        Finds the primary bias defined by the user. Ignores first and last three aa in seq for primary bias calculation.
        Stores the index of each primary bias residue in the sequence string in self.primary_bias

        :returns: updates self.Q_index list (no return)
        """
        primary_indices = list()
        # might have to change this if
        if primary_bias in seq:
            working_sequence = seq[3:-3]
            for i in range(len(working_sequence)):
                if working_sequence[i] == primary_bias:
                    # if statement should ignore Q. Could split loops so if isn't read outside
                    # the first three and last three indexes. Range b/t could be very large
                    primary_indices.append(i)
            return primary_indices

        else:
            return None

    def populate_SequenceBiasBuilder(self, seqrecord_list):
        for i in seqrecord_list:
            self.id_seq.update({i.id: str(i.seq)})
            self.prim_indices.update({i.id: []})
            self.one_away.update({i.id: [0] * 20})
            self.two_away.update({i.id: [0] * 20})
            self.three_away.update({i.id: [0] * 20})
            self.local_sequence.update({i.id: [0] * 20})
            self.one_away_avg.update({i.id: [None] * 20})
            self.two_away_avg.update({i.id: [None] * 20})
            self.three_away_avg.update({i.id: [None] * 20})
            self.local_avg.update({i.id: [None] * 20})

    def secondary_bias_finder(self, sequence, bias_location: int, prim_indices):
        """
        Finds amino acids at one, two, and three residues from the desired primary bias. A local tally is also computed.

        Modified:
            self.one_away, self.two_away,self.three_away, self.three_away_avg, self.local_sequence: get updated
        """
        secbias_list = [0] * 20
        for i in prim_indices:
            prim_minus = i - bias_location
            aa_to_increment = self.amino_acid_dict[sequence[prim_minus]]
            secbias_list[aa_to_increment] += 1
            prim_plus = i + bias_location
            aa_to_increment = self.amino_acid_dict[sequence[prim_plus]]
            secbias_list[aa_to_increment] += 1
        return secbias_list

    def calc_local_bias(self, one_away=None, two_away=None, three_away=None):
        """

        Args:
            one_away:
            two_away:
            three_away:

        Returns:

        """
        if one_away is None:
            one_away = list(self.one_away.values())
        if two_away is None:
            two_away = list(self.two_away.values())
        if three_away is None:
            three_away = list(self.three_away.values())
        local_seq = [0] * 20
        for i in range(20):
            local_seq[i] = one_away[i] + two_away[i] + three_away[i]
        self.local_sequence = local_seq
        return local_seq

    def find_avg_occurrence(self, bias_list, primary_content=None):
        """
        Divides each index of +/- 1, 2, 3 and local lists by the total primary bias residue content (average)

        Modified:
            updates +/- 1, 2, 3, and local avg lists
        """
        if primary_content is None:
            primary_content = len(self.prim_indices)
        bias_avg = list()
        if primary_content != 0:
            for i in range(20):
                bias_avg.append(bias_list[i] / primary_content)
        return bias_avg

    def update_annotations(self, seqrecord_to_update, update_data: dict):
        """

        Args:
            seqrecord_to_update:
            update_data:

        Returns:

        """
        try:
            assert(None not in update_data)
            seqrecord_to_update.annotations.update(update_data)
            return seqrecord_to_update
        except AssertionError as ae:
            print("The average hasn't been calculated!!")
            return seqrecord_to_update


    # @staticmethod
    # def find_sec_bias(primary_bias, seq_record_list):
    #     sec_bias_list = list()
    #     for i in seq_record_list:
    #         sec_bias_list.append(SecondaryBias(i.seq))
    #     for i in sec_bias_list:
    #         i.bias_finder(primary_bias)
    #         i.update_annotations()
    #     return sec_bias_list


class DatabaseBuilder(Builder):
    """


    """
    def __init__(self):
        super(DatabaseBuilder, self).__init__()


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
        file_name = File_IO.make_original_file_name(file_out_dir=storage_dir, file_name="uniprot_data",  file_extension=file_extension)
        with open(file_name, 'w') as file:
            file.write(data)
        seq_record_list = list()
        with open(file_name, 'rU') as file:
            for sequence in SeqIO.parse(file, data_format):
                seq_record_list.append(sequence)
        return seq_record_list

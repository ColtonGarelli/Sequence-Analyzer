# -*- coding: utf-8 -*-
# builder class
import json
import os
import time
import requests as r
from Bio import SeqIO, SeqRecord, Seq
from Bio.Alphabet import generic_protein
from SecondaryBiasFinder import SecondaryBias
import numpy as np
# import datetime
#
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# TODO: Update all docstrings and move static methods to parent classes

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


class SequenceBiasBuilder(AnalysisBuilder):
    """
    In an effort to reduce overhead, going to transition SecondaryBiasFinder to SeqeuenceBiasBuilder. SequenceBiasBuilder
    will
    """
    @staticmethod
    def convert_to_tuple(seqrecord_list):
        return_list = list()
        for i in seqrecord_list:
            return_list.append((i.id, str(i.seq)))
        return return_list

    # To get ID,seq pairs correctly:
    # new_list =[['id1', 'ASDFSDFADSFDS'], ['id2', 'ASDFSDFASDFSD'], ['id3', 'FSDSFSASDFSDDFSDDFDSFWQQWQWQ'], ['id1', 'ASDFSDFADSFDS'], ['id2', 'ASDFSDFASDFSD'], ['id3', 'FSDSFSASDFSDDFSDDFDSFWQQWQWQ']]
    # l = [tuple(new_list[0]), tuple(new_list[1]), tuple(new_list[2])]
    # h = np.array(l, dtype=dtype)

    def __init__(self, seqrecord_list: [SeqRecord.SeqRecord], primary_bias='Q'):
        """


        """
        super().__init__()
        self.amino_acid_dict = dict(A=0, C=1, D=2, E=3, F=4, G=5, H=6, I=7, K=8, L=9,
                                    M=10, N=11, P=12, Q=13, R=14, S=15, T=16, V=17, W=18, Y=19)
        seq_list = self.convert_to_tuple(seqrecord_list)
        self.seq_array = np.array(seq_list, dtype=[('id', 'O'), ('sequence', 'O')])
        self.primary_bias = primary_bias
        # self.sequence_len = 0
        self.prim_bias_indices: np.ndarray     # (dtype=[('id', 'object'), ('prim_indices', 'object')])
        # self.prim_bias_content = np.recarray(shape=(len(self.seqrecord_list), 1),
        #                                      dtype=[('id', 'object'), ('prim_content', '<i4')])

        self.one_away: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.two_away: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])

        self.three_away: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.local_bias: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.one_away_avg: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.two_away_avg: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.three_away_avg: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])
        self.local_avg: np.ndarray  # dtype=[('id', 'object',), ('1_away', 'object')])

    def find_avg_occurances(self, array_to_avg, primary_content, secondary_location: str or int):
        if secondary_location is isinstance(secondary_location, str):
            location = 'local_avg'
        else:
            location = str(secondary_location) + '_avg'
        secondary_avg_array = np.array(array_to_avg['id'], dtype=[('id', 'O'), (location, 'O')])
        for i in range(len(array_to_avg)):
            secondary_avg_array[i][location] = array_to_avg[i][1] / primary_content
        return secondary_avg_array

    def find_a_bias(self, id_seq_array, prim_bias_location, secondary_location: int):
        location = str(secondary_location) + '_away'
        secondary_bias_array = np.array(id_seq_array['id'], dtype=[('id', 'O'), (location, 'O')])

        for i in range(len(id_seq_array)):
            # the sequence being worked on
            current_sequence = id_seq_array[i]['sequence']
            secondary_data_array = np.zeros(dtype=[(location, np.uint32)], shape=[len(id_seq_array), 20])
            for primary in np.nditer(prim_bias_location[i]['prim_indices'], flags=['refs_ok']):
                # find the minus 1 aa
                aa_to_increment = self.amino_acid_dict[current_sequence[primary[0] - secondary_location]]
                # increment the respective aa count
                to_increment = secondary_data_array[i][aa_to_increment]
                to_increment[0] += 1
                secondary_data_array[i, aa_to_increment] = to_increment
                # find the plus 1 aa
                aa_to_increment = self.amino_acid_dict[current_sequence[primary[0] + secondary_location]]
                # increment the respective aa count
                to_increment = secondary_data_array[i][aa_to_increment]
                to_increment[0] += 1
                secondary_data_array[i, aa_to_increment] = to_increment
            secondary_bias_array[location] = secondary_data_array
        return secondary_bias_array

    def sum_secondary_biases(self, one_away: np.recarray, two_away, three_away):
        local_bias = np.recarray(shape=(len(one_away), 1),
                                 dtype=[('id', 'object',), ('local_away', 'object')])
        for i in np.nditer(one_away):
            local_bias[i]['id'] = one_away[i]['id']
            local_data_array = one_away[i]['1_away'] + two_away[i]['2_away'] + three_away[i]['3_away']
            local_bias['local_away'] = local_data_array
        return local_bias

    def find_primary_bias(self, seq_array: np.recarray, primary_bias="Q"):
        """
        Finds the primary bias defined by the user. Ignores first and last three aa in seq for primary bias calculation.
        Stores the index of each primary bias residue in the sequence string in self.primary_bias

        :returns: updates prim_bias_indices list (no return)
        """

        prim_location = np.array(seq_array['id'], dtype=[('id', 'O'), ('prim_indices', 'O')])
        for i in range(seq_array.size):
            current_sequence = seq_array[i]['sequence']
            seq_str = current_sequence[3:-3]
            # seq_to_check = list(seq_str)
            if primary_bias in seq_str:
                location_arr = list([i1 for i1, item in enumerate(seq_str) if primary_bias in item])
                prim_location[i]['prim_indices'] = location_arr
            else:
                prim_location[i]['prim_indices'] = None
        return prim_location

    @staticmethod
    def find_sec_bias(primary_bias, seq_record_list):
        sec_bias_list = list()
        for i in seq_record_list:
            sec_bias_list.append(SecondaryBias(i.seq))
        for i in sec_bias_list:
            i.bias_finder(primary_bias)
            i.update_annotations()
        return sec_bias_list


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
                    working_list.append(seq_list[i].format("fasta"))
            except TypeError as type_e:
                for i in range(len(seq_list)):
                    working_list[i].seq = Seq.Seq(data=working_list[i].seq, alphabet=generic_protein)
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
        formatted = str()
        for i in fasta_str_list:
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

            master_list[i].letter_annotations.update({'entropy': entropy})
            master_list[i].letter_annotations.update({'pos_charge': pos_charge})
            master_list[i].letter_annotations.update({'neg_charge': neg_charge})
            master_list[i].letter_annotations.update({'hydro_cluster': hydro_cluster})
            master_list[i].letter_annotations.update({'percent_dis': percent_dis})
            master_list[i].letter_annotations.update({'percent_helix': percent_helix})
            master_list[i].letter_annotations.update({'percent_coil': percent_coil})
            master_list[i].letter_annotations.update({'hydro': hydrophobic})
            # comp has to do with at least charge
            master_list[i].letter_annotations.update({'composition': comp})
            master_list[i].letter_annotations.update({'aggregation': aggregation})
            master_list[i].letter_annotations.update({'order_disorder': order_disorder})
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

    def create_seqrecord_object(self):
        # create seqrecord objects with annotations
        # consider using **kwargs to pass in different annotation lists
        # if implemented with kwargs, could make class level
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
            time.sleep(1.00)
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


class DatabaseBuilder(Builder):
    """


    """
    def __init__(self):
        super(DatabaseBuilder, self).__init__()


class UniprotBuilder(DatabaseBuilder):
    """


    """
    _base_url = "https://www.uniprot.org/uniprot/?query="
    url_extension = "&limit=5&format="
    column_dict = {'id': 'id', 'entry': 'entry name', 'Organism': 'organism', 'prot name': "protein name",
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

    def get_base_url(self):
        return self._base_url

    def construct_column_string(self, columns):
        column_string = "&columns=reviewed"
        for i in range(len(self.column_dict)):
            if i in columns:
                column_string += (',' + self.column_dict[i])
        return column_string

    def create_request_url(self, response_format, column_string):
        self.request_url = self.get_base_url() + self.url_extension + response_format + column_string
        return self.request_url

    def make_request_get_response(self, search_url):
        new_request = r.get(search_url)
        return new_request.content.decode('utf-8')

    def uniprot_xml_to_seqrecord(self, uniprot_xml, storage_dir):
        file_name = os.path.join(storage_dir, "uniprot_data{}.xml".format(str(time.clock())[2:]))
        if os.path.exists(file_name):
            counter = 0
            os.path.exists(file_name+"_{}".format(counter))
            while os.path.isdir(file_name):
                counter += 1
                if counter < 11:
                    file_name = os.path.join(file_name[:-1] + str(counter))
                elif counter > 10:
                    file_name = os.path.join(file_name[:-2] + str(counter))
                elif counter > 100:
                    file_name = os.path.join(file_name[:-3] + str(counter))
        with open(file_name, 'w') as file:
            file.write(uniprot_xml)
        seq_record_list = list()
        with open(file_name, 'rU') as file:
            for sequence in SeqIO.parse(file, "uniprot-xml"):
                seq_record_list.append(sequence)
        return seq_record_list

# -*- coding: utf-8 -*-
# builder class
import json
import os
import time
import requests as r
from Bio import SeqIO, SeqRecord, Seq
from Bio.Alphabet import IUPAC
from SecondaryBiasFinder import SecondaryBias
import datetime

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

    # @staticmethod
    # def make_original_file_name():
    #     home = os.path.join(os.path.expanduser('~'))
    #     d = 'Desktop'
    #     data_source = os.path.join(home, d)
    #     new_dir_name = os.path.join(data_source, "PAM_Output_{}".format(datetime.date.today()))
    #     counter = 0
    #     if os.path.isdir(new_dir_name):
    #         new_dir_name = new_dir_name + "_{}".format(counter)
    #         while os.path.isdir(new_dir_name):
    #             counter += 1
    #             if counter < 11:
    #                 new_dir_name = new_dir_name[:-1]
    #             elif counter > 10:
    #                 new_dir_name = new_dir_name[:-2]
    #             elif counter > 100:
    #                 new_dir_name = new_dir_name[:-3]
    #             new_dir_name = new_dir_name + str(counter)
    #             os.path.join(new_dir_name)
    #         os.mkdir(new_dir_name)


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
        prepped_request = r.Request(method='POST', url=self.get_post_url(),
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
                    working_list[i].seq = Seq.Seq(data=working_list[i].seq, alphabet=IUPAC.IUPACProtein())
                    working_list[i] = working_list[i].format("fasta")
        elif isinstance(seq_list[0], str):
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
                time.sleep(5.00)
                check_status = r.get(url=self._status_url + jobid)
                json_obj = json.loads(check_status.content)
            return check_status
        else:
            return False

    def check_processing_status(self, ID):
        processing = r.get(self._get_url+ID)
        processing = json.loads(processing.content)
        while processing['status'] == 'running':
            time.sleep(5.00)
            processing = r.get(self._get_url + ID)
            processing = json.loads(processing.content)
        if processing['status'] == 'done':
            return True
        else:
            return False

    def retrieve_response_data(self, id_list):
        return_data = []
        for i in id_list:
            request_data = r.get(self._get_url + i[1]).content.decode()
            return_data.append(json.loads(request_data))
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

    def get_post_url(self):
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
            time.sleep(5.00)
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
            seqrecord.annotations.update(seq_data)
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

    @staticmethod
    def find_sec_bias(primary_bias, seq_record_list):
        sec_bias_list = list()
        for i in seq_record_list:
            sec_bias_list.append(SecondaryBias(i.seq))
        for i in sec_bias_list:
            i.bias_finder(primary_bias)
            i.update_annotations()
        return sec_bias_list


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

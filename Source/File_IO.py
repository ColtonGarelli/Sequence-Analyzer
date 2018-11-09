import json
from jsonpickle import encode as jsonpickle_encode
import csv
import os
from collections import namedtuple as collections_namedtuple
from Bio import SeqIO
from Bio.Alphabet import generic_protein as gen_prot_alaphabet
from Bio.SeqRecord import SeqRecord
from datetime import date

'''
json text files stored with .jtxt extension
'''


def dict_to_seqrecord(seq_dict):
    seqrecord_list = list()
    seq_dict = json.loads(seq_dict)
    for k in seq_dict:
        temp = (collections_namedtuple("SeqRecord", seq_dict.keys())(*seq_dict.values()))
        seqrecord_list.append(SeqRecord(temp))
    return seqrecord_list


def seqrecord_to_dict(seq_list: [SeqRecord]):
    """
    For rich output. Creates a dict where key = SeqRecord.id, value = the rest of the info
    Args:
        seq_list:

    Returns:

    """
    seq_list = SeqIO.to_dict(seq_list)
    return jsonpickle_encode(seq_list)


def export_to_csv(self, seq_dict: dict):
    # TODO: should have an option as to what data to output (from letter annotations and annotations)
    file_o_path = os.path.join(self.file_out_dir + self.make_original_file_name() + ".csv")
    with open(file_o_path, "w") as f:
        csv.DictWriter(f=f, fieldnames=dir(seq_dict.values()))


def write_dict_to_file(write_str, file_out_dir):
    # TODO: consider writing using pickle module (for large dataset data persistence)
    # ****BEFORE WRITING PICKLING FUNCTION**** test this and all other modules.

    file_o_path = os.path.join(make_original_file_name(file_out_dir) + ".jtxt")
    with open(file_o_path, "w") as f:
        json.dump(write_str, f)
        f.close()
    return file_o_path


def make_original_file_name(file_out_dir):
    counter = 0
    if os.path.isdir(file_out_dir):
        new_file_name = "PAM_Output_{}".format(counter)
        new_file_path = os.path.join(file_out_dir, new_file_name)
        while os.path.exists(new_file_path):
            counter += 1
            if counter < 11:
                new_file_path = new_file_path[:-1]
            elif counter > 10:
                new_file_path = new_file_path[:-2]
            elif counter > 100:
                new_file_path = new_file_path[:-3]
            new_file_path = new_file_path + "_" + str(counter)
        return os.path.join(new_file_path)


def create_new_file_dir(desktop_dir):
    new_dir_name = os.path.join(desktop_dir, "PAM_Output_{}".format(date.today()))
    counter = 0
    if os.path.isdir(new_dir_name):
        new_dir_name = new_dir_name + "_{}".format(counter)
        while os.path.isdir(new_dir_name):
            counter += 1
            if counter < 11:
                new_dir_name = new_dir_name[:-1]
            elif counter > 10:
                new_dir_name = new_dir_name[:-2]
            elif counter > 100:
                new_dir_name = new_dir_name[:-3]

            new_dir_name = new_dir_name + str(counter)
            os.path.join(new_dir_name)
        os.mkdir(new_dir_name)
    else:
        os.makedirs(new_dir_name)
    return new_dir_name


def find_desktop_dir():
    """

    :return:
    """
    home = os.path.join(os.path.expanduser('~'))
    d = 'Desktop'
    data_source = os.path.join(home, d)
    if not os.path.isdir(data_source):
        data_source = OutputFunctions.select_fileio_directory()
    return data_source


def file_input(full_file_path: str):
    seqrecord_list = list()
    if ".faa" in full_file_path:
        with open(full_file_path, "rU") as f:
            for record in SeqIO.parse(f, "fasta", gen_prot_alaphabet):
                seqrecord_list.append(record)
    elif ".jtxt" in full_file_path:
        with open(full_file_path, "rU") as f:
            seqrecord_dict = json.load(f)
            seqrecord_list = dict_to_seqrecord(seqrecord_dict)
    else:
        print("Unsupported file-in format!")

    return seqrecord_list

    # def analysis_helper(self, bias_analysis: bool):
    #     """
    #     Does the work prior to analysis. Handles file-in path, creating file-out path,
    #
    #     """
    #     # todo: select primary bias
    #     this = bias_analysis
    #     slash_list = self.file_in_path.rsplit("/", 1)
    #     new_path = str(slash_list[0])
    #     self.set_io_directory(new_path)

    # def store_all_data(self):
    #     file_name = os.path.join(self.file_out_dir, 'data_persistence{}'.format(datetime.date.today()))
    #     counter = 0
    #     if os.path.exists(file_name):
    #         os.path.exists(file_name+"_{}".format(counter))
    #         while os.path.isdir(file_name):
    #             counter += 1
    #             if counter < 11:
    #                 file_name = os.path.join(file_name[:-1] + str(counter))
    #             elif counter > 10:
    #                 file_name = os.path.join(file_name[:-2] + str(counter))
    #             elif counter > 100:
    #                 file_name = os.path.join(file_name[:-3] + str(counter))
    #     file_name = os.path.join(file_name + '.xml')
    #     with open(file_name, 'w') as file:
    #         try:
    #             SeqIO.write(sequences=self.master_list, handle=file, format='seqxml')
    #         except TypeError as type_e:
    #             for i in range(len(self.master_list)):
    #                 seq_obj = Bio.Seq.Seq(data=str(self.master_list[i].seq), alphabet=Alphabet.generic_protein)
    #                 self.master_list[i].seq = seq_obj
    #         except AttributeError as att_err:
    #             for i in range(len(self.master_list)):
    #                 seq_obj = Bio.Seq.Seq(data=str(self.master_list[i].seq), alphabet=Alphabet.generic_protein)
    #                 self.master_list[i].seq = seq_obj
    #             SeqIO.write(sequences=self.master_list, handle=file, format='seqxml')

    # @staticmethod
    # def file_output(sequences: dict or list, file_out_dir):
    #     if isinstance(sequences, list):
    #         file_o_path = os.path.join(file_out_dir + Director.make_original_file_name() + ".faa")
    #         with open(file_o_path, "w") as f:
    #                 SeqIO.write(sequences, f, "fasta")
    #     elif isinstance(sequences, dict):
    #         file_o_path = os.path.join(file_out_dir + Director.make_original_file_name() + ".json")
    #         with open(file_o_path, "w") as f:
    #             json.dump(sequences, f)
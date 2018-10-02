

from PyQt5 import QtWidgets
from threading import Timer
import SecondaryBiasFinder
import Director
import Representation
import Builder
from os.path import join
import requests
import sys
import PyQt5.QtWidgets
# Colton Garelli
from Builder import UniprotBuilder
import pprint
import json
import os
from Bio.SeqRecord import SeqRecord
import time


def analyze_group(self, list_index):
    group_to_analyze = self.group_list[list_index]
    for i in range(len(group_to_analyze)):
        seq_to_analyze = group_to_analyze.seq_bias_list[i]
        updated = seq_to_analyze.bias_finder()
    return True


def __output_spreadsheet():
    something = True

    return something


# check file format function, read in . consider making global functions
def __input_spreadsheet():

    return True


def run_experiment(self, path_in, path_out):
    # create seqgroup and call create groups
    set_in = self.set_file_in_path(path_in)
    set_out = self.set_file_out_path(path_out)
    self.group_list = self.input_spreadsheet()
    for i in range(len(self.group_list)):
        post_analysis = self.analyze_group(i)
    self.output_spreadsheet()
    something = True

    return something


def remove_line_break(sequence):
    new_seq = sequence.replace("\n", "")
    print(new_seq)


def run_database_stuff():
    something = 0
    as_fasta = "https://www.uniprot.org/uniprot/P12345.fasta"
    base_url = "https://www.uniprot.org/uniprot/?query="
    query_url = {"something": "url text", "something else": "another url"}
    # determines what info is returned in response element
    column_url = {"ID": "a column with useful info"}
    format_url = "&format=fasta"
    #
    # example_url = "https://www.uniprot.org/uniprot/?query=insulin&" \
    #               "sort=score&columns=id,protein names,length&format=tab"
    #
    another_url = "http://www.uniprot.org/uniprot/?query=arabidopsis%20thaliana&sort=score&" \
                  "columns=id,protein names,&format=tab"
    #
    # ebi_url = "https://www.ebi.ac.uk/proteins/api/features?offset=0&size=100&protein=Auxin%20Response%20Factor"

    this_request = requests.get(another_url)
    print(this_request.text)

    url = "https://www.uniprot.org/uniprot/?query=insulin&sort=score&columns=entry name,protein names,length&format=tab"
    request = requests.get(url)
    print(request.text)


def function_for_db_fiddling():
    none = None
    #  sequence = ""
    # request = requests.post("https://www.uniprot.org/uniprot/?query=reviewed:yes&random=yes")
    # print(request.status_code)
    # SpreadsheetIO.fasta_parser()
    # path_in = "/Users/coltongarelli/SequenceAnalyzer/PAM/References/SEQUENCEANALYZER_Experiment1_inputfile_ACTUAL.csv"
    # # # file_representation = Representation()
    #
    # director = Director()
    # director.analysis_helper(path_in)
    # processed = director.run_analysis()
    # SecondaryBiasFinder.export_sec_bias_files(processed)
    # request = requests.get()
    # run_database_stuff()


def function_for_experimenting():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    button = QtWidgets.QPushButton("Hello, PyQt!")
    window.setCentralWidget(button)
    window.show()
    app.exec_()


def uniprot_test_request():
    uniprot_builder = UniprotBuilder()
    columns = uniprot_builder.construct_column_string(['id', 'seq'])
    request_url = uniprot_builder.create_request_url('tardigrade', columns)
    data = uniprot_builder.make_request_get_response(request_url)
    record_list = uniprot_builder.uniprot_fasta_to_seqrecord(data)
    print(record_list)


def timer():

    starttime = time.time()
    while True:
        print("tick")
        time.sleep(5.0 - ((time.time() - starttime) % 5.0))


def testing_FELLS_requesting():
    FELLS_builder = Builder.FELLSAnalysisBuilder()
    seq_list = ["\n\n>test\nMVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"]
    seq = SeqRecord(id=">test\n", seq="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR")
    seq2 = SeqRecord(id='>test2\n', seq="ASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD")
    master = [seq, seq2]
    jobid = FELLS_builder.prepare_and_send_request(master)
    json_obj = FELLS_builder.check_request_status(jobid)
    FELLS_builder.check_processing_status(json_obj['names'][0][1])
    data = FELLS_builder.retrieve_response_data(json_obj['names'])
    updated = FELLS_builder.update_annotations(master_list=master, data_list=data)
    return updated


def testing_SODA_requesting():
    SODA_builder = Builder.SODAAnalysisBuilder()
    seq_list = ["MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR", "ASDFSDFASQWERFDSAWQEWSDDFWEQWEDS"]
    jobid = SODA_builder.prepare_request_object(seq_list[0])
    json_obj = SODA_builder.check_request_status(jobid)
    data = SODA_builder.retrieve_response_data(jobid)
    pprint.pprint(data)


def UI_main(director):
    done = False
    input_source = director.start_up()
    first_time = True
    while not done:
        # while loop terminates when done = True
        if first_time:
            # if first time is true, the following options set up input
            if input_source == "1":
                seq_list = director.db_access()
                director.set_master_list(seq_list)
            elif input_source == "2":
                seq_list = director.handle_manual_input()
                director.set_master_list(seq_list)
            elif input_source == "0":
                break
        first_time = False
        choice = director.view_or_process()
        while choice == 'v':
            # interface to view
            # todo: options to change view
            choice = director.view_or_process()

        bias_data = director.run_bias_analysis()
        fells_data = director.run_FELLS_analysis()
        soda_data = director.run_SODA_analysis()
        director.update_seq_data(fells=fells_data, soda=soda_data, sec_bias=bias_data)
        director.view_analysis()
        director.store_all_data()
        done = director.quit_or_continue()


if __name__ == '__main__':
    main_director = Director.Director()
    # main_director.start_up()
    # data = testing_FELLS_requesting()
    # main_director.set_master_list(data)
    # main_director.store_all_data()
    UI_main(main_director)

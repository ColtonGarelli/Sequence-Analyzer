from PyQt5 import QtWidgets

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
    # path_in = "/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzer2.1/References/SEQUENCEANALYZER_Experiment1_inputfile_ACTUAL.csv"
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


def UI_main(director):
    in_source = director.define_input_source()
    if in_source == "up":
        director.access_databases()
    elif in_source == "file":
        director.define_input_source()


def uniprot_test_request():
    uniprot_builder = UniprotBuilder()
    columns = uniprot_builder.construct_column_string(['id', 'seq'])
    request_url = uniprot_builder.create_request_url('tardigrade', columns)
    data = uniprot_builder.make_request_get_response(request_url)
    record_list = uniprot_builder.uniprot_tab_separated_to_file(data)
    print(record_list[0])

def testing_FELLS_requesting():
    FELLS_builder = Builder.FELLSAnalysisBuilder()
    seq_list = ['ASDFGFDSASDFGFDSREWASDFREWQQQQQQWQQWSQ', 'ASDFSDFASQWERFDSAWQEWSDDFWEQWEDS']
    jobid = FELLS_builder.prepare_request_object(seq_list)
    json_obj = FELLS_builder.check_request_status(jobid)
    while json_obj.get('status') != 'done':
        json_obj = FELLS_builder.check_request_status(jobid)
    something = json_obj.get('names')
    analysis_id = something[1]
    something_else = FELLS_builder.retrieve_response_data(analysis_id)
    print(something_else.decode('utf-8'))


if __name__ == '__main__':
    main_director = Director.Director()
    testing_FELLS_requesting()
    # uniprot_test_request()
    # UI_main(main_director)

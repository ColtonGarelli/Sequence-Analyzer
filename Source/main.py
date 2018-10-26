
import PyQt5.QtWidgets as QtWidgets
import Director
import Builder
import sys
import pprint
from Bio.SeqRecord import SeqRecord
import requests as r
import json


def function_for_experimenting():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow(flags=None)
    button = QtWidgets.QPushButton("Hello, PyQt!")
    window.setCentralWidget(button)
    window.show()
    app.exec_()


def testing_FELLS_requesting():
    FELLS_builder = Builder.FELLSAnalysisBuilder()
    seq_list = ["\n\n>test\nMVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"]
    seq = SeqRecord(id=">test\n", seq="MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR")
    seq2 = SeqRecord(id='>test2\n', seq="ASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD")
    master = [seq, seq2]
    prepped_request = FELLS_builder.prepare_request(master)
    s = r.Session()
    response = s.send(request=prepped_request)
    json_content = json.loads(response.content.decode('utf-8'))
    jobid = json_content['jobid']
    json_obj = FELLS_builder.check_request_status(jobid)
    FELLS_builder.check_processing_status(json_obj['names'][0][1])
    data = FELLS_builder.retrieve_response_data(json_obj['names'])
    updated = FELLS_builder.update_annotations(master_list=master, data_list=data)
    return updated


def testing_SODA_requesting():
    SODA_builder = Builder.SODAAnalysisBuilder()
    seq_list = ["MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR", "ASDFSDFASQWERFDSAWQEWSDDFWEQWEDS"]
    prepped_request = SODA_builder.prepare_request_object(seq_list[0])
    s = r.Session()
    response = s.send(request=prepped_request)
    json_content = json.loads(response.content.decode('utf-8'))
    jobid = json_content['jobid']
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
    main_director.start_up()
    data = testing_SODA_requesting()
    # main_director.set_master_list(data)
    # main_director.store_all_data()
    UI_main(main_director)

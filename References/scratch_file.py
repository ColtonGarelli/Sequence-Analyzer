# import numpy as np
# # import matplotlib
# # matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd





# def function_for_experimenting():
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QMainWindow(flags=None)
#     button = QtWidgets.QPushButton("Hello, PyQt!")
#     window.setCentralWidget(button)
#     window.show()
#     app.exec_()


# def testing_FELLS_requesting():
#     FELLS_builder = Builder.FELLSAnalysisBuilder()
#     seq_list = ["\n\n>test\nMVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"]
#     seq = SeqRecord(id="test", seq=Seq.Seq("MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR"))
#     seq2 = SeqRecord(id='test2', seq=Seq.Seq("ASDFASDFSDFASDFAFSDFSDFSDAFSDFFSD"))
#     master = [seq, seq2]
#     prepped_request = FELLS_builder.prepare_request(master)
#     s = r.Session()
#     response = s.send(request=prepped_request)
#     jobid = FELLS_builder.get_jobid(response)
#     submission_response = FELLS_builder.check_request_submission(jobid)
#     json_obj = FELLS_builder.get_data_as_json(submission_response)
#     FELLS_builder.check_processing_status(json_obj['names'][0][1])
#     data = FELLS_builder.retrieve_response_data(json_obj['names'])
#     updated = FELLS_builder.update_annotations(master_list=master, data_list=data)
#     updated = SeqIO.to_dict(updated)
#     print("Yert\n\n" + str(updated))
#     return updated
#
#
# def testing_SODA_requesting():
#     SODA_builder = Builder.SODAAnalysisBuilder()
#     seq_list = ["MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR", "ASDFSDFASQWERFDSAWQEWSDDFWEQWEDS"]
#     prepped_request = SODA_builder.prepare_request_object(seq_list[0])
#     s = r.Session()
#     response = s.send(request=prepped_request)
#     json_content = json.loads(response.content.decode('utf-8'))
#     jobid = json_content['jobid']
#     json_obj = SODA_builder.check_request_status(jobid)
#     data = SODA_builder.retrieve_response_data(jobid)
#     print(data)


# main stuff below

# csv = pd.read_csv('/Users/coltongarelli/Documents/Demographic_Statistics_By_Zip_Code.csv')
# sns.set_style('dark')
# csv["JURISDICTION NAME"] = pd.to_numeric(csv["JURISDICTION NAME"])
# csv["COUNT MALE"] = pd.to_numeric(csv["COUNT MALE"])
# g = sns.lmplot(x="JURISDICTION NAME", y="COUNT MALE", data=csv)
#
# plt.title("title")
#
# plt.show()


# main_director.start_up()
# data = testing_FELLS_requesting()
# typing = data.get('test')
# print(typing)
# print(typing.letter_annotations)

# main_director.set_master_list(data)
# main_director.store_all_data()
import OutputFunctions
import Representation
from Builder import AnalysisBuilder, UniprotBuilder, SequenceBiasBuilder, DatabaseBuilder, FELLSAnalysisBuilder, SODAAnalysisBuilder
import os.path
import datetime
import Bio
from Bio import SeqIO, Seq, Alphabet, SeqRecord
import json
import requests as r
import File_IO
import csv
import collections
import jsonpickle

# room for addition of BLAST, alignment, other tools as run_x_analysis methods
# run_x_analysis methods communicate directly with self.AnalysisBuilder obj and self.DatabaseBuilder
# DatabaseBuilder and AnalysisBuilder communicate with APIs and local modules
# director also manages Representation

# ***IMPORTANT DECISIONS***
# Start by passing only in xml, always pass in file paths, update the master_list at the end of each analysis run



class Director:
    """
    The Director class manages file input, analysis, and data outputting and formatting.
        * Contains methods to execute tasks
    """
    file_in_path: str

    def __init__(self):
        """
        Creates 'representation' object to manage user interface and output


        :cvar self.analysis: each director object contains an analysis object that run the desired set of analyses
        :cvar self.representation: each director object contains an representation object to litigate data output
        :cvar self.master_list: master sequence-id list. saved after file is first read in
              the master list should be updated after analysis
        :cvar self.file_in_path: path for sequence-id file in csv format
        :cvar self.file_out_path: path for directory where files can be output



        """

        self.database: DatabaseBuilder = None
        # a list of representations
        self.representation = Representation.Representation()
        # master list contains seq_record objects. Initially should contain id-seq but
        # annotations and letter annotations should be updated w new values
        self.master_list: list = None
        self.analysis = {"fells": FELLSAnalysisBuilder(), "soda": SODAAnalysisBuilder()}
                         # "sec_bias": SequenceBiasBuilder(seq_list=self.master_list)}
        # directory where input file resides and where output directory will be created
        self.file_out_dir: str = File_IO.find_desktop_dir()
        self.file_in_path: str = None

    def start_up(self):

        return self.representation.introduction()

    def db_access(self):
        """

        :return:
        """

        db_choice = self.representation.choose_database()
        if db_choice == "up":
            self.database = UniprotBuilder()
        else:
            self.database = UniprotBuilder()
        db_options = self.representation.db_options()
        response_opts = self.database.construct_column_string(db_options)
        response_format = "xml"
        request_url = self.database.create_request_url(response_format, response_opts)
        response_info = self.database.make_request_get_response(request_url)
        seq_list = self.database.uniprot_xml_to_seqrecord(response_info, self.file_out_dir)
        # elif response_format == "fasta":
        #     seq_list = self.database.uniprot_data_to_seqrecord(response_info, self.file_in_path, 'fasta')
        # elif response_format == "tab":
        #     seq_list = self.database.uniprot_data_to_seqrecord(response_info, self.file_in_path, 'tab')
        # else:
        #     seq_list = None
        # database object should contain list of seqrecord objects
        # call database to make list and set master list equal to
        return seq_list

    # if view is selected, run functions that create and functions that display desired info
    def view_or_process(self):
        """

        :return:
        """
        choice = input("Would you like to view imported sequence information before processing? (y/n) ")
        if choice == "y":
            choice = self.representation.db_query_view(self.master_list)
            return "v"
        else:
            # todo: implement better viewing and ability to select different views
            return "a"

    def view_analysis(self):
        # TODO: some viewing options other than printing
        print(self.master_list)

    def quit_or_continue(self):
        # TODO: Update to actually provide a choice (after data persistence is supported)
        # TODO: allow option to delete past job and to keep and append new data
        return True

    def run_FELLS_analysis(self):
        # TODO:
        """

        :returns:

        """
    #   sends list of seqrecord objects to fells module
    #   while loop to check for updates
    #   director holds onto FELLS, where data is stored
    #   builder objects own data and send translations to director
    #     fasta_list = []
    #     for i in self.get_master_list():
    #         fasta_list.append(i.format("fasta"))
        prepped_request = self.analysis["fells"].prepare_request(self.get_master_list())
        session = r.Session()
        response = session.send(request=prepped_request)
        jobid = AnalysisBuilder.get_jobid(response)
        response_str = self.analysis["fells"].check_request_submission(jobid)
        json_obj = AnalysisBuilder.get_data_as_json(response_str)
        complete = self.analysis["fells"].check_processing_status(json_obj['names'][0][1])
        if complete:
            id_list = list()
            for i in json_obj["names"]:
                id_list.append(i[1])
            data_list = self.analysis["fells"].retrieve_response_data(id_list)
            json_list = list()
            for data in data_list:
                json_list.append(json.loads(data))
            return json_list
        else:
            return "an error occured"
    # todo: do something with the data (store and plot)

    def run_SODA_analysis(self):
        """

        :returns:
        """
        processed_list = list()
        s = r.Session()
        for i in self.master_list:
            prepped_request = self.analysis['soda'].prepare_request_object(str(i.seq))
            response = s.send(prepped_request)
            jobid = AnalysisBuilder.get_jobid(response)
            json_obj = self.analysis['soda'].check_request_status(jobid)
            jobid = json_obj['jobid']
            data = self.analysis['soda'].retrieve_response_data(jobid)
            data = json.loads(data)
            processed_list.append(data)
        return processed_list
    # todo: do something with the data (store and plot)

    def run_bias_analysis(self):
        """
        Reads file in and creates a master list of id-sequence lists. It then creates SecondaryBias objects and runs the
        analysis using its self.analysis object

        :returns: List of fully processed SecondaryBias objects
        """
        sec_bias_analysis = SequenceBiasBuilder(self.master_list)
        sec_bias_analysis.prim_bias_indices = sec_bias_analysis.find_primary_bias(seq_array=sec_bias_analysis.seq_array,
                                                                                  primary_bias=sec_bias_analysis.primary_bias)
        bias = sec_bias_analysis.find_a_bias(sec_bias_analysis.seq_array, sec_bias_analysis.prim_bias_indices, 1)
        print(bias)
        # updated_list = self.analysis['sec_bias'].find_sec_bias("Q", self.master_list)
        #
        # return updated_list

    def update_seq_data(self, **kwargs):
        if 'fells' in kwargs:
            self.master_list = FELLSAnalysisBuilder.update_annotations(self.master_list, kwargs['fells'])
        if 'soda' in kwargs:
            for i in range(len(self.master_list)):
                self.master_list[i] = SODAAnalysisBuilder.update_annotations(self.master_list[i], kwargs['soda'][i])
        if 'sec_bias' in kwargs:
            pass

    def get_master_list(self):
        return self.master_list

    def set_master_list(self, new_list):
        self.master_list = new_list

    def get_file_in_path(self):
        return self.file_in_path

    def set_file_in_path(self, new_in_path):
        self.file_in_path = new_in_path

    def get_io_directory(self):
        return self.file_out_dir

    def set_io_directory(self, new_out_dir):
        self.file_out_dir = new_out_dir

    # def handle_manual_input(self):
    #     """
    #     Uses 'representation' to prompt user for file path and prints information to the screen
    #
    #
    #     :returns:
    #
    #
    #     """
    #     file_name = self.representation.manual_sequence_entry()
    #     self.set_file_in_path(os.path.join(self.file_out_dir, file_name))
    #     with open(self.file_in_path, 'rU') as file:
    #         lines = []
    #         for line in file:
    #             lines.append(line)
    #     list_in = Builder.create_seqrecord_object_from_csv(lines)
    #     # run function to return master list
    #     return list_in

    # def convert_json_to_seqrecord(self, json_dict: dict):
    #     key_list = json_dict.keys()
    #     attr_list = [attr for attr in dir(SeqRecord.SeqRecord) if not callable(getattr(SeqRecord.SeqRecord, attr)) and not attr.startswith("__") and not attr.startswith("_")]
    #     for k in key_list:
    #         seqrecord_info = json_dict.get(k)



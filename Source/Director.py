import Representation
from Builder import AnalysisBuilder, UniprotBuilder, SequenceBiasBuilder, DatabaseBuilder, FELLSAnalysisBuilder, SODAAnalysisBuilder
import File_IO
import json
import requests as r
from urllib3 import connection as connection


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
        self.analyses = {"fells": FELLSAnalysisBuilder(), "soda": SODAAnalysisBuilder(), "sec_bias": SequenceBiasBuilder()}
        # directory where input file resides and where output directory will be created
        self.file_out_dir = File_IO.create_new_file_dir(File_IO.find_desktop_dir())
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
        response_format = self.representation.extended_information()
        data_format = 'fasta'
        if response_format == 'xml':
            db_options = self.representation.db_options(extended_opts=True)
            data_format = 'uniprot-xml'
        else:
            db_options = self.representation.db_options(extended_opts=False)
        response_opts = self.database.construct_column_string(db_options)
        limit = self.representation.select_db_limit()
        request_url = self.database.create_request_url(response_format=response_format, column_string=response_opts,
                                                       limit=limit)
        response_info = self.database.make_request_get_response(request_url)
        seq_list = self.database.uniprot_to_seqrecord(data=response_info, storage_dir=self.file_out_dir, data_format=data_format)
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
        return True

    def run_FELLS_analysis(self):
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
        prepped_request = self.analyses["fells"].prepare_request(self.get_master_list())
        session = r.Session()
        succesful_connection = True

        try:
            response = session.send(request=prepped_request)
        except Exception:
            print("Could not connect to FELLS server!!")
            succesful_connection = False
        if succesful_connection:
            jobid = AnalysisBuilder.get_jobid(response)
            response_str = self.analyses["fells"].check_request_submission(jobid)
            json_obj = AnalysisBuilder.get_data_as_json(response_str)
            complete = self.analyses["fells"].check_processing_status(json_obj['names'][0][1])
            if complete:
                id_list = list()
                for i in json_obj["names"]:
                    id_list.append(i[1])
                data_list = self.analyses["fells"].retrieve_response_data(id_list)
                json_list = list()
                for data in data_list:
                    json_list.append(json.loads(data))
                return json_list
            else:
                return "an error occurred!!"
        else:
            return "an error occurred!!"
    # todo: do something with the data (store and plot)

    def run_SODA_analysis(self):
        """

        :returns:
        """
        processed_list = list()
        s = r.Session()
        successful_connection = True
        for i in self.master_list:
            if successful_connection:
                prepped_request = self.analyses['soda'].prepare_request_object(str(i.seq))
                try:
                    response = s.send(prepped_request)
                    jobid = AnalysisBuilder.get_jobid(response)
                    json_obj = self.analyses['soda'].check_request_status(jobid)
                    jobid = json_obj['jobid']
                    data = self.analyses['soda'].retrieve_response_data(jobid)
                    data = json.loads(data)
                    processed_list.append(data)
                except Exception:
                    print("Could not connect to SODA server!!")
                    successful_connection = False
            else:
                break
        return processed_list
    # todo: do something with the data (store and plot)

    def run_bias_analysis(self):
        """
        Reads file in and creates a master list of id-sequence lists. It then creates SecondaryBias objects and runs the
        analysis using its self.analysis object

        :returns: List of fully processed SecondaryBias objects
        """
        # TODO: prompt to input a primary bias
        primary_bias = "Q"
        bias_analysis = self.analyses['sec_bias']
        bias_analysis.populate_SequenceBiasBuilder(self.master_list)
        keys = bias_analysis.id_seq.keys()
        for key in keys:
            bias_analysis.prim_indices[key] = bias_analysis.primary_bias_finder(seq=bias_analysis.id_seq[key],
                                                                                aaprimary_bias=primary_bias)
            bias_analysis.one_away[key] = bias_analysis.secondary_bias_finder(sequence=bias_analysis.id_seq[key],
                                                                              bias_location=1,
                                                                              prim_indices=bias_analysis.prim_indices[key])
            bias_analysis.two_away[key] = bias_analysis.secondary_bias_finder(sequence=bias_analysis.id_seq[key],
                                                                              bias_location=2,
                                                                              prim_indices=bias_analysis.prim_indices[key])
            bias_analysis.three_away[key] = bias_analysis.secondary_bias_finder(sequence=bias_analysis.id_seq[key],
                                                                                bias_location=3,
                                                                                prim_indices=
                                                                                bias_analysis.prim_indices[key])

            bias_analysis.local_sequence[key] = bias_analysis.calc_local_bias(one_away=bias_analysis.one_away[key],
                                                                              two_away=bias_analysis.two_away[key],
                                                                              three_away=bias_analysis.three_away[key])
        #         # TODO: prompt about calculating avg occurrences
        avg = True
        if avg:
            for i in bias_analysis.one_away.keys():
                bias_analysis.one_away_avg[i] = bias_analysis.find_avg_occurrence(
                    bias_list=bias_analysis.one_away_avg[i], primary_content=len(bias_analysis.prim_indices))
            for i in bias_analysis.two_away.keys():
                bias_analysis.two_away_avg[i] = bias_analysis.find_avg_occurrence(
                    bias_list=bias_analysis.two_away_avg[i])
            for i in bias_analysis.three_away.keys():
                bias_analysis.three_away_avg[i] = bias_analysis.find_avg_occurrence(
                    bias_list=bias_analysis.three_away_avg[i])
            for i in bias_analysis.local_sequence.keys():
                bias_analysis.local_avg[i] = bias_analysis.find_avg_occurrence(bias_list=bias_analysis.local_avg[i])

        return bias_analysis

    def update_seq_data(self, **kwargs):
        if 'fells' in kwargs:
            fells_analysis = self.analyses['fells']
            self.master_list = self.analyses['fells'].update_annotations(self.master_list, kwargs['fells'])
        if 'soda' in kwargs:
            soda_analysis = self.analyses['soda']
            # for i in range(len(self.master_list)):
            #     self.master_list[i] = soda_analysis.update_annotations(self.master_list[i], kwargs['soda'][i])
        if 'sec_bias' in kwargs:
            bias_analysis = self.analyses['sec_bias']
            for i in self.master_list:
                i = bias_analysis.update_annotations(seqrecord_to_update=i,
                                                     update_data={'one_away': bias_analysis.one_away[i.id],
                                                                  'two_away': bias_analysis.two_away[i.id],
                                                                  'three_away': bias_analysis.three_away[i.id],
                                                                  'local_sequence': bias_analysis.local_sequence[i.id]})
            for i in self.master_list:
                i = bias_analysis.update_annotations(seqrecord_to_update=i,
                                                     update_data={'one_away_avg': bias_analysis.one_away_avg[i.id],
                                                                  'two_away_avg': bias_analysis.two_away_avg[i.id],
                                                                  'three_away_avg': bias_analysis.three_away_avg[i.id],
                                                                  'local_avg': bias_analysis.local_avg[i.id]})



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



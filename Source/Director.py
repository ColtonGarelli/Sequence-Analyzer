import OutputFunctions
import Representation
from Builder import Builder, AnalysisBuilder, UniprotBuilder, SequenceBiasBuilder, DatabaseBuilder, FELLSAnalysisBuilder, SODAAnalysisBuilder
import SecondaryBiasFinder
import os.path
import datetime
import Bio
from Bio import SeqIO, Seq, Alphabet
from Bio.Alphabet import IUPAC

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
        self.analysis = {"fells": FELLSAnalysisBuilder(), "soda": SODAAnalysisBuilder(), "seqbias": SequenceBiasBuilder(self.master_list)}
        # directory where input file resides and where output directory will be created
        self.file_out_dir: str = None
        self.file_in_path: str = None

    def start_up(self):
        new_dir_name = os.path.join(self.find_desktop_dir(), "PAM_Output_{}".format(datetime.date.today()))
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
        self.file_out_dir = new_dir_name
        return self.representation.introduction()

    def handle_manual_input(self):
        """
        Uses 'representation' to prompt user for file path and prints information to the screen


        :returns:


        """
        file_name = self.representation.manual_sequence_entry()
        self.set_file_in_path(os.path.join(self.file_out_dir, file_name))
        with open(self.file_in_path, 'rU') as file:
            lines = []
            for line in file:
                lines.append(line)
        list_in = Builder.create_seqrecord_object_from_csv(lines)
        # run function to return master list
        return list_in

    @staticmethod
    def find_desktop_dir():
        """

        :return:
        """
        home = os.path.join(os.path.expanduser('~'))
        d = os.path.join('Desktop')
        data_source = os.path.join(home, d)
        if not os.path.isdir(data_source):
            data_source = OutputFunctions.select_fileio_directory()
        return data_source

    def analysis_helper(self, bias_analysis: bool):
        """
        Does the work prior to analysis. Handles file-in path, creating file-out path,

        """
        # todo: select primary bias
        this = bias_analysis
        slash_list = self.file_in_path.rsplit("/", 1)
        new_path = str(slash_list[0])
        self.set_io_directory(new_path)

    def db_access(self):
        """

        :return:
        """

        db_choice = self.representation.choose_database()
        if db_choice == "up":
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

    def create_seqrec_objects_from_fasta(self, fasta):
        """

        :return:
        """
    # turn string formatted info to SeqRecord objects
    # put SeqRecord obj list in master list
        pass

    def view_analysis(self):
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
        prepped_list = []
        for i in self.get_master_list():
            prepped_list.append(i.format("fasta"))
    # todo: fill prepped_list with a list of fasta formatted sequences
        jobid = self.analysis["fells"].prepare_and_send_request(prepped_list)
        json_obj = self.analysis["fells"].check_request_status(jobid)
        self.analysis["fells"].check_processing_status(json_obj['names'][0][1])
        data = self.analysis["fells"].retrieve_response_data(json_obj['names'])
        return data
    # todo: do something with the data (store and plot)

    def run_SODA_analysis(self):
        """

        :returns:
        """
        processed_list = list()
        for i in self.master_list:
            jobid = self.analysis['soda'].prepare_request_object(str(i.seq))
            json_obj = self.analysis['soda'].check_request_status(jobid)
            jobid = json_obj['jobid']
            data = self.analysis['soda'].retrieve_response_data(jobid)
            processed_list.append(data)
        return processed_list
    # todo: do something with the data (store and plot)

    def run_bias_analysis(self):
        """
        Reads file in and creates a master list of id-sequence lists. It then creates SecondaryBias objects and runs the
        analysis using its self.analysis object

        :returns: List of fully processed SecondaryBias objects
        """
        # for csv formatted files only. call

        # select primary bias
        # primary_bias = Representation.choose_primary_bias()
        secondary_analysis = SequenceBiasBuilder(self.master_list)
        updated_list = secondary_analysis.find_sec_bias("Q", self.master_list)

        return updated_list
        # file_string = Representation.read_file(self.file_in_path)
        # self.master_list = Representation.parse_to_string_list(file_string)
        # # each string in string_list represents a sequence
        #
        # sequence_list = self.analysis.build_seq_list(self.master_list)
        # processed = self.analysis.build_sec_bias()
        #
        # return processed

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

    def update_seq_data(self, **kwargs):
        if 'fells' in kwargs:
            self.master_list = FELLSAnalysisBuilder.update_annotations(self.master_list, kwargs['fells'])
        if 'soda' in kwargs:
            self.master_list = SODAAnalysisBuilder.update_annotations(self.master_list, kwargs['soda'])
        if 'sec_bias' in kwargs:
            pass

    def store_all_data(self):
        file_name = os.path.join(self.file_out_dir, 'data_persistence{}'.format(datetime.date.today()))
        counter = 0
        if os.path.exists(file_name):
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
            try:
                SeqIO.write(sequences=self.master_list, handle=file, format='seqxml')
            except TypeError as type_e:
                for i in range(len(self.master_list)):
                    seq_obj = Bio.Seq.Seq(data=str(self.master_list[i].seq), alphabet=Alphabet.ProteinAlphabet())
                    self.master_list[i].seq = seq_obj
            except AttributeError as att_err:
                for i in range(len(self.master_list)):
                    seq_obj = Bio.Seq.Seq(data=str(self.master_list[i].seq), alphabet=Alphabet.ProteinAlphabet())
                    self.master_list[i].seq = seq_obj
                SeqIO.write(sequences=self.master_list, handle=file, format='seqxml')


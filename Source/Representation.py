import Output_Functions
"""
Representation.py contains Representation class and UI functions

Responds to Director by:
    * Print prompts and relay responses
    * Print requested data
    * Present available options for databases, processing, viewing

Functions: 
    * Serve as UI prompts and to augment other printed/file representations

"""


# Product in builder pattern for python (see: https://gist.github.com/pazdera/1121157)
class Representation:
    """
    - Runs user interface using the UI class. May move those functions to this module (eliminate class).
    - Handles file-output. Raw data should be output as a csv file. Graphical representations may be implemented later.
    - Runs all interaction with user and computer (display/fileio)

    Attributes:
            'self.file_out_path': file out path to the desired directory
            'self.base_name': base file name to maintain consistency in output

    """
    def __init__(self):

        self.file_out_path = None
        self.base_name = None
        self.print_string = None

    def introduction(self):
        """
        Prints link to documentation and prints welcome message

        Note:
            this function may be moved to a class variable
        """
        Output_Functions.welcome()
        return Output_Functions.main_page()

    def manual_sequence_entry(self):
        """
        Manages file_in entry including providing examples, links to documentation for formatting
        and passing input file path from user to director

        :returns: user inputted path
        """
        # manual_sequence_input provides link to documentation on file_in format
        self.base_name = Output_Functions.manual_sequence_input()
        return self.base_name

    # handles calling desired DB, representing responses,
    def db_options(self):
        """
        Relays an ordered tuple to the director containing request information.
        Request information in this tuple contains keywords, query options,
        and response columns (everything needed to send a request)

        :returns: list containing database info defined in the director class

        """
        keyword = Output_Functions.keyword_query_uniprot()
        if keyword is "":
            options = Output_Functions.data_options()
            return options

        else:
            options = Output_Functions.data_options()
            option_list = options.insert(0, keyword)
            return option_list

    # def manage_processed_info(self):
    #     """
    #     Prints prompts for viewing info for user
    #
    #     Returns:
    #         view type (console, file out, graphical at some point)
    #     """
    #     option = database_response_options()
    #     if option == 'file':
    #         self.file_out_path = manual_sequence_input()
    #         return option
    #     else:
    #         return option

    def output_data(self, print_or_out):
        """
        Take the string passed in and prints it or writes it to file.
        In the future, a separate function for graphing

        :param print_or_out(str): a string representing file our view

        :returns: Completion of file_out or printing (T/F)
        """
        if print_or_out == 'file':
            # add here
            return True

        elif print_or_out == 'view':
            print(self.print_string)
            return True
        return False

    def db_file_out(self, seq_list, file_string):
        """
        Handles output of a UniProt formatted xml file. In the future this method should support
        multiple data output syntax

        :param seq_list: a list of SeqRecord objects to be written to file.
        :return: success of file output
        """
        if seq_list == 'up':
            up_parser = Output_Functions.write_uniprot_to_file(self.file_out_path)

    def set_print_string(self, new_string):
        self.print_string = new_string

    def get_print_string(self):
        return self.print_string

    def db_query_view(self):
        s = None

    def choose_database(self):
        """
        Relays which database is being accessed so Director can access that database through its builder

        :returns: database choice
        """
        db_choice = Output_Functions.access_databases()
        if db_choice != "1":
            print("Sorry! That database hasn't been implemented.")
        else:
            return "up"

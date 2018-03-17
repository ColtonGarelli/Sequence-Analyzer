import SecondaryBias
from Operation import Director, AnalysisImpl, Representation
from os.path import join


# Colton Garelli

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


def main():

    # APIHandler.UniProtAPI()
    # change to test symlink again
    # sequence = SecondaryBias()
    # SecondaryBias.bias_finder(sequence)
    path_in = "/Users/coltongarelli/SequenceAnalyzer/SequenceAnalyzer2.1/Source/csv_key"
    file_representation = Representation()
    analysis = AnalysisImpl(path_in)
    director = Director()
    processed = director.run_analysis(analysis)
    SecondaryBias.export_sec_bias_files(processed)





main()

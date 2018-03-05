from SecondaryBias import SequenceBias
import APIHandler


def main():

    # APIHandler.UniProtAPI()
    # change to test symlink again
    sequence = SequenceBias()
    SequenceBias.bias_finder(sequence)


main()

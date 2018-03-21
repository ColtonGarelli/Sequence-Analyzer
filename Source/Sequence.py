#
#
# class Sequence:
#     """
#     A general Sequence class. Contains parameters for valid amino acids, amino acid dictionary,
#     and a sequence_in variable to store the input sequence.
#     """
#     amino_acids = "ACDEFGHIKLMNPQRSTVWY"
#
#     amino_acid_dict = dict(A=0, C=1, D=2, E=3, F=4, G=5, H=6, I=7, K=8, L=9,
#                             M=10, N=11, P=12, Q=13, R=14, S=15,T=16, V=17, W=18, Y=19)
#     sequence_in = ""
#
#     def check_aa_entry(self, sequence_in):
#         """
#         Ensures only natural amino acids are entered when user inputs a sequence manually.
#
#         :param sequence_in: String of characters
#         :return: True if all characters entered are natural amino acids, otherwise False
#         """
#
#         not_aa = "BJOUXZ"
#         alpha = sequence_in.isalpha()
#         if alpha:
#             sequence_in = sequence_in.upper()
#             bad_count = 0
#             for i in range(0, 6):
#                 if not_aa[i] in sequence_in:
#                     bad_count = bad_count + 1
#             if bad_count == 0:
#                 good_entry = True
#             else:
#                 good_entry = False
#
#         else:
#             good_entry = False
#         return good_entry

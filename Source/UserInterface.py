


def print_biases(self):
    for i in range(0, 19):
        if self.one_away_avg[i] > 0.05:
            print(self.amino_acids[i] + ' ' + str(self.one_away_avg[i]) + " one away")
        else:
            print("No secondary bias 1 location away")

        if self.two_away_avg[i] > 0.05:
            print(self.amino_acids[i] + ' ' + str(self.two_away_avg[i]) + " two away")
        else:
            print("No secondary bias 2 locations away")
        if self.three_away_avg[i] > 0.05:
            print(self.amino_acids[i] + ' ' + str(self.three_away_avg[i]) + " three away")
        else:
            print("No secondary bias 3 locations away")
        if self.local_avg[i] > 0.05:
            print(self.amino_acids[i] + ' ' + str(self.local_avg[i]) + " within 6 residues")
        else:
            print("No secondary bias")
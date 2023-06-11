import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py FILENAME")

    # TODO: Read database file into a variable
    filename = sys.argv[1]
    seq = []
    with open(filename) as f1:
        csvFile = csv.reader(f1)

        for row in csvFile:
            seq.append(row)

    # TODO: Read DNA sequence file into a variable

    dna_sequence = sys.argv[2]
    f2 = open(dna_sequence, 'r')
    dna = f2.read()

    shortTandem = []

    for i in range(1, len(seq[0]), 1):
        shortTandem.append(seq[0][i])

    # TODO: Find longest match of each STR in DNA sequence

    longest_run = {}

    for j in range(0, len(shortTandem)):
        subsequence = shortTandem[j]

        longest_run[subsequence] = longest_match(dna, subsequence)

    longest_run_list = list(longest_run.values())

    # TODO: Check database for matching profiles

    found = False

    for k in range(1, len(seq)):
        seq_val = [int(item) for item in seq[k][1:]]

        if seq_val == longest_run_list:
            print(seq[k][0])
            found = True

    if found != True:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

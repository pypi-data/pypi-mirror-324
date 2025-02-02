import os
import csv
import sys
import time
from io import StringIO
import json
import argparse
import collections
import ahocorasick

def create_encoding(singlechars, multichars):
    """Return a list of 255 strings representing the encoded ngrams"""

    encoding = [""] * 256

    # It's nice to encode the single chars under their ASCII location
    for char in singlechars:
        encoding[ord(char)] = char

    # Let's encode the rest in the order in which they were provided (i.e. found)
    idx = 0
    for ngram in multichars:
        while encoding[idx]:
            idx += 1
        encoding[idx] = ngram
    return encoding

class Compressor():
    def __init__(self, singlechars, multichars):
        self.singlechars = singlechars
        self.multichars = multichars
        self.auto = ahocorasick.Automaton()
        for multichar in self.multichars:
            self.auto.add_word(multichar, multichar)
        if self.multichars:
            self.auto.make_automaton()

    def add_token(self, token):
        self.auto.add_word(token, token)
        self.auto.make_automaton()

    def compress(self, text):
        solution = [0] # the min number of ngrams for the substring of length idx

        if self.multichars:
            matches = list(self.auto.iter(text)) # [(endidx, string), ...]
        else:
            matches = []

        matches_by_endidx = collections.defaultdict(list)
        for endidx, ngram in matches:
            matches_by_endidx[endidx].append(ngram)

        chosen_len = []
        N = len(text)
        for i in range(N):
            all_data = []
            all_data.append( (solution[i], 1) ) # handle single-char (note: this does not check whether the character appears in the list of supported single-chars)
            for ngram in matches_by_endidx[i]:
                ngram_len = len(ngram)
                data = (solution[i-ngram_len+1], ngram_len)
                all_data.append(data)
            all_data.sort()
            solution.append(all_data[0][0] + 1)
            chosen_len.append(all_data[0][1])

        # We have the best length
        # ...we just need to backtrack to find the ngrams that were chosen
        i = len(text) - 1
        num_ngrams = 0
        while i >= 0:
            i -= chosen_len[i]
            num_ngrams += 1
        return num_ngrams

def length_after_compression(smiles, singlechars, multichars):
    compressor = Compressor(singlechars, multichars)
    mlen = 0
    for smi in smiles:
        mlen += compressor.compress(smi)
    return mlen

class NgramManager:
    def __init__(self):
        self.values = {}
        self.counts = None

    def calculate_ngrams(self, smiles):
        max_size = 60
        counts = collections.defaultdict(int) # the number of occurences
        molecule_counts = collections.defaultdict(int) # the number of molecules it occurs in
        for smi in smiles:
            mc = set()
            for start in range(0, len(smi)-2):
                for end in range(start+2, min(len(smi), start+max_size+1)):
                    ngram = smi[start:end]
                    counts[ngram] += 1
                    mc.add(ngram)
            for ngram in mc:
                molecule_counts[ngram] += 1
        self.counts = dict((x, y) for (x, y) in counts.items() if molecule_counts[x] > 1) # N grams must occur in at least 2 molecules

    def set_value(self, ngram, val):
        self.values[ngram] = (val, True)

    def update_estimates(self, latest, singlechars, multichars):
        """Assign or update value estimates

        An estimated value to assigned to any new ngrams. Ngrams whose value has already
        been measured are left unchanged. Over time these values will become over
        optimistic, but this is fine as they will be remeasured.
        Over-optimistic estimates are more of a problem, as all the sequences of a particular
        length will suddenly find themselves top of the pile, and crowd out realistic measured
        values. For this reason, all estimated values are re-estimated if a new token is
        added to the list that might affect its value.
        For example, the estimated value of "c1ccccc1" is 7 (8 ngrams converted to 1) but if "cc"
        is subsequently added to the list of ngrams, then its estimate will be re-evaluated
        as 5 (6 ngrams converted to 1).
        """
        for ngram in self.counts.keys():
            val, is_measured = self.values.get(ngram, (0, False))
            if is_measured:
                continue
            if val == 0 or latest in ngram:
                self.values[ngram] = (length_after_compression([ngram], singlechars, multichars) - 1, False)

    def get_ngrams(self, chosen_ngrams: set):
        """Yield ngrams in order of value"""
        tmp = []
        for ngram, count in self.counts.items():
            if ngram in chosen_ngrams:
                continue
            val, is_measured = self.values[ngram]
            tmp.append( (ngram, val, is_measured, val*count) )
        tmp.sort(reverse=True, key=lambda x:x[3])
        for t in tmp:
            yield t

DEFAULT_LIST = "*%:#()+-./0123456789=@ABCFHIKLMNOPRSTXZ[\\\\]abcegilnoprst"

def parse_args():
    parser = argparse.ArgumentParser(description="Find a set of ngrams that maximally compresses a training set")
    parser.add_argument("-i", "--input", help="Training set file", required=True)
    parser.add_argument("-o", "--output", help="JSON file into which to save the list of 256 ngrams", required=True)
    parser.add_argument("-l", "--log", help="Write the log to a file. Note that it will still be written to stdout.", default=None)
    parser.add_argument("--chars", help=f"A list of all the characters that will be present in the SMILES string to be encoded. A reasonable default is \"{''.join(sorted(DEFAULT_LIST)).replace('%', '%%')}\" but you should check this for yourself, or trim it if it has too many characters. The fewer characters in this list, the more that will be available for n-gram compression.", required=True)
    parser.add_argument("--multigrams", help="Provide a comma-separated list of additional ngrams to include. This is parsed using Python's CSV reader.")
    parser.add_argument("--zero", action="store_true", help="Include \\0 as an ngram")
    parser.add_argument("--tab", action="store_true", help="Include TAB as an ngram")
    parser.add_argument("--space", action="store_true", help="Include SPACE as an ngram")
    parser.add_argument("--lf", action="store_true", help="Include \\n (line-feed) as an ngram")
    parser.add_argument("--non-printable", action="store_true", help="Include all other non-printable characters as ngrams. This is useful (in combination with the --zero and --lf options) to ensure that the generated zipped strings do not contain any control characters or characters outside the ASCII printable set.")
    parser.add_argument("--speed", default="slow", help="Specify one of fast, medium, slow (default). A faster search is less thorough in its testing of n-grams and will result in poor compression")

    args = parser.parse_args()
    return args

def infinite_iterator(fname):
    """Once the file is exhausted, read from the beginning again"""
    while True:
        with open(fname) as inp:
            for line in inp:
                yield line

class Log:
    def __init__(self, filename=None):
        self.output = None
        if filename:
            self.output = open(filename, "w")

    def write(self, text):
        sys.stdout.write(text)
        if self.output:
            self.output.write(text)

def main():
    args = parse_args()

    t = time.time()

    out = Log(args.log)

    multichars = []
    singlechars = set(args.chars)
    if args.lf:
        singlechars.add("\n")
    if args.tab:
        singlechars.add("\t")
    if args.space:
        singlechars.add(" ")
    if args.zero:
        singlechars.add("\0")
    if args.non_printable:
        singlechars.update(list("\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"))
    if args.multigrams:
        f = StringIO(args.multigrams)
        reader = csv.reader(f)
        ngrams = next(reader)
        for ngram in ngrams:
            if len(ngram) == 1:
                singlechars.add(ngram)
            elif len(ngram) > 1:
                multichars.append(ngram)
    out.write(f"The initial list of single-char ngrams is:\n  {repr(''.join(sorted(singlechars)))}\n")
    out.write(f"The initial list of multi-char ngrams is:\n  {multichars}\n")

    orig_num_ngrams = len(singlechars)
    smiles_iter = infinite_iterator(args.input)

    if args.speed == "slow":
        NUM_SMILES_TO_TEST, DELTA_TO_TEST = 1000, 45
        TEST_AT_LEAST_N_MEASURED = 80
        TEST_AT_LEAST_N = 100
        TEST_AT_LEAST_N_SOMETIMES = 1000
        SOMETIMES_INTERVAL = 20
    elif args.speed == "fast":
        NUM_SMILES_TO_TEST, DELTA_TO_TEST = 100, 4.5
        TEST_AT_LEAST_N_MEASURED = 25
        TEST_AT_LEAST_N = 25
        TEST_AT_LEAST_N_SOMETIMES = 30
        SOMETIMES_INTERVAL = 250
    else: # medium
        NUM_SMILES_TO_TEST, DELTA_TO_TEST = 250, 12
        TEST_AT_LEAST_N_MEASURED = 40
        TEST_AT_LEAST_N = 50
        TEST_AT_LEAST_N_SOMETIMES = 200
        SOMETIMES_INTERVAL = 50

    out.write(f"{NUM_SMILES_TO_TEST=}\n{DELTA_TO_TEST=}\n{TEST_AT_LEAST_N_MEASURED=}\n{TEST_AT_LEAST_N=}\n")
    out.write(f"{TEST_AT_LEAST_N_SOMETIMES=}\n{SOMETIMES_INTERVAL=}\n\n")

    # Create holdout set of 10K
    holdout = []
    for i in range(10000):
        holdout.append(next(smiles_iter).split()[0])
    holdoutlen = length_after_compression(holdout, singlechars, multichars)
    out.write(f"Holdout set: {len(holdout)} SMILES with {holdoutlen} chars\n")

    manager = NgramManager()
    chosen = (None, None)
    first_pass = True
    counter = 0

    while len(multichars) + orig_num_ngrams < 256:
        num_smiles_to_test = int(NUM_SMILES_TO_TEST + len(multichars) * DELTA_TO_TEST)

        # At least every 20 iterations, test at least 1000 ngrams
        counter += 1
        if counter == SOMETIMES_INTERVAL:
            counter = 0
            test_at_least_N_ngrams = TEST_AT_LEAST_N_SOMETIMES
        else:
            test_at_least_N_ngrams = TEST_AT_LEAST_N

        out.write(f"Testing {num_smiles_to_test} SMILES\n")
        out.write(f"Going to test at least {test_at_least_N_ngrams} ngrams\n")
        smiles = [next(smiles_iter).split()[0] for i in range(num_smiles_to_test)]
        origlen = length_after_compression(smiles, singlechars, multichars)
        minlen = origlen
        manager.calculate_ngrams(smiles)
        manager.update_estimates(chosen[0], singlechars, multichars)
        num_tested = 0
        for idx, (ngram, val, is_measured, score) in enumerate(manager.get_ngrams(set(multichars)), 1):
            if idx > TEST_AT_LEAST_N_SOMETIMES:
                counter = 0
            if num_tested >= TEST_AT_LEAST_N_MEASURED and idx > test_at_least_N_ngrams:
                break # we require min 100 ngrams and min 80 measured ngrams
            length = length_after_compression(smiles, singlechars, multichars + [ngram])
            new_value = (origlen-length) / manager.counts[ngram]
            out.write(f"  Rank {idx}: {ngram} {val:.1f}{'M' if is_measured else 'E'}->{new_value:.1f} {score:.1f}->{origlen-length} count={manager.counts[ngram]}\n")
            manager.set_value(ngram, new_value)
            if length < minlen:
                chosen = (ngram, idx)
                minlen = length
            if is_measured or first_pass:
                num_tested += 1
        first_pass = False
        multichars.append(chosen[0])
        out.write(f"Ngram {len(multichars)+orig_num_ngrams}: {chosen[0]} Rank {chosen[1]} {origlen}->{minlen}\n")
        nholdoutlen = length_after_compression(holdout, singlechars, multichars)
        out.write(f"Holdout set: {len(holdout)} SMILES with {holdoutlen}->{nholdoutlen} chars ({nholdoutlen/holdoutlen:.1%})\n")

    out.write(f"\nTime: {time.time() - t:.1f}\n")

    encoding = create_encoding(singlechars, multichars)
    metadata = {"num_smiles_to_test": NUM_SMILES_TO_TEST,
                "delta_to_test": DELTA_TO_TEST,
                "filename": os.path.basename(args.input),
                "test_at_least_N": TEST_AT_LEAST_N,
                "test_at_least_N_measured": TEST_AT_LEAST_N_MEASURED,
                "test_at_least_N_sometimes": TEST_AT_LEAST_N_SOMETIMES,
                "sometimes_interval": SOMETIMES_INTERVAL,
                "initial_chars": "".join(sorted(singlechars)), # includes --cr, etc.
                "initial_multigrams": args.multigrams}

    with open(args.output, "w") as out:
        json.dump({"ngrams": encoding, "metadata": metadata}, out)

if __name__ == "__main__":
    main()

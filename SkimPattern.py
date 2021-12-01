# Read pattern... rip first two chars off from each line as I have no
# idea what the + means....

# To shorten the RegEx ... Uppercase is assumed
import re
import pickle
import sys


class SkimmerPattern:

    def __init__(self, pattern_file="junk.lst",
                 master="nonMASTER.SCP"):
        self.calls = {}
        self.skimmer_data = {}
        self._pattern = pattern_file
        self._master = master
        self.load_pattern(pattern_file)
        self.load_master()
        self.process()
        self.save_results()
        self.check_skimmer_rules()
        self.check_master_rules()

    def skim_to_regex(self, skim_expression: str) -> str:
        skim_expression = skim_expression.replace('@', '[A-Z]')
        skim_expression = skim_expression.replace('#', '[0-9]')
        return r"^{0}$".format(skim_expression)

    def load_pattern(self, pattern_file_str:str):
        with open(pattern_file_str, 'rt') as pattern_file:
            patt = [d.upper().strip() for d in pattern_file.read().split()[:-1]]

        for p in patt:
            self.skimmer_data[p] = {}
            self.skimmer_data[p]['matched_count'] = 0
            self.skimmer_data[p]['matched_calls'] = []
        print(f"Patternfile has {len(self.skimmer_data)} records")

    def load_master(self):
        with open(self._master, 'rt') as scp_file:
            for c in scp_file.read().upper().split('\n')[4:]:
                self.calls[c] = {}
                self.calls[c]['matched_count'] = 0
                self.calls[c]['matched_patt'] = []

    def process(self):
        progress = 0
        for s in self.skimmer_data.keys():
            skim_matches = 0
            pattern_re = re.compile(self.skim_to_regex(s))
            for c in self.calls.keys():
                m = pattern_re.match(c)
                if m:
                    self.calls[c]['matched_count'] += 1
                    self.calls[c]['matched_patt'].append(s)
                    self.skimmer_data[s]['matched_count'] += 1
                    self.skimmer_data[s]['matched_calls'].append(c)
                    # print(f"{c} {s}")
            progress += 1
            if progress % 1000 == 0:
                print(f"Done {progress}")
            # if progress>1000:
            #    break

    def save_results(self):
        #
        # now save the results
        #
        with open(self._pattern + ".pkl", 'wb') as ofp:
            pickle.dump([self.skimmer_data, self.calls], ofp)

    def check_skimmer_rules(self):
        #
        # How many un-matched rules are there ?
        #
        unmatch_rule_count = 0
        for s in self.skimmer_data.keys():
            if self.skimmer_data[s]['matched_count'] == 0:
                print(s)
                unmatch_rule_count += 1
        print(f"We have {len(self.skimmer_data)} rules")
        print(f"We have {unmatch_rule_count} unmatched rules")
        print(f"rule match percentage is {(len(self.skimmer_data) -unmatch_rule_count) * 100 /len(self.skimmer_data):5.3f} %")

    def check_master_rules(self):
        #
        # MASTER.SCP how many calls are missing
        #
        unmatched_count = 0
        hasslash = 0
        for c in self.calls.keys():
            if self.calls[c]['matched_count'] == 0:
                # print(c)
                unmatched_count += 1
                if c.find("/") != -1:
                    hasslash += 1
        print(f"We have {unmatched_count} unmatched calls from SCP")
        print(f"call match percentage is {(len(self.calls)-unmatched_count) * 100 / len(self.calls):5.3f}%")
        print(f"of which {hasslash} has a / ")


if __name__ == "__main__":
    pattern = sys.argv[1]
    print(f"Checking pattern file {pattern}")
    check = SkimmerPattern(pattern_file=pattern, master="MASTER.SCP")

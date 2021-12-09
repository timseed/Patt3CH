import pandas as pd


class PatternBuilder:
    def call_to_skimmer_format1(self, call):
        output = []
        for c in call:
            if c.isnumeric():
                output.append("#")
            elif c.isalpha():
                output.append("@")
            else:
                output.append(c)
        return "".join(output)

    def call_to_skimmer_format2(self, call):
        output = [call[0], call[1]]
        for c in call[2:]:
            if c.isnumeric():
                output.append("#")
            elif c.isalpha():
                output.append("@")
            else:
                output.append("/")
        return "".join(output)

    def call_to_skimmer_format3(self, call):
        try:
            output = [call[0], call[1], call[2]]
            for c in call[3:]:
                if c.isnumeric():
                    output.append("#")
                elif c.isalpha():
                    output.append("@")
                else:
                    output.append(c)
            return "".join(output)
        except Exception as err:
            print(f"Error processing call <{call}>")
            return ""

    def __init__(self,master_file="MASTER.SCP"):
        junk = 1
        self.data = []
        self.df = self.load(master_file)
        self.makecolumns()
        self.output("format1.lst", self.df['SKIMMER_FORMAT1'].unique())
        self.output("format2.lst", self.df['SKIMMER_FORMAT2'].unique())
        self.output("format3.lst", self.df['SKIMMER_FORMAT3'].unique())

    def load(self, filename:str ) -> pd.DataFrame:
        print(f"Loading {filename}")
        with open(filename, "rt") as mt:
            self.data = [d for d in mt.read().upper().split("\n")[4:] if len(d) > 0]
        d = pd.DataFrame(self.data)
        d.columns = ["CALLS"]
        return d

    def makecolumns(self):
        self.df["STARTS1"] = self.df.CALLS.apply(lambda x: (x + "  ")[0])
        self.df["STARTS2"] = self.df.CALLS.apply(lambda x: (x + "  ")[0:2])
        self.df["STARTS3"] = self.df.CALLS.apply(lambda x: (x + "  ")[0:3])
        self.df["SKIMMER_FORMAT1"] = self.df.CALLS.apply(
            lambda x: self.call_to_skimmer_format1(x)
        )
        self.df["SKIMMER_FORMAT2"] = self.df.CALLS.apply(
            lambda x: self.call_to_skimmer_format2(x)
        )
        self.df["SKIMMER_FORMAT3"] = self.df.CALLS.apply(
            lambda x: self.call_to_skimmer_format3(x)
        )

    def output(self, filename, data_as_list):
        data_as_list.sort()
        print(f"file {filename} has {len(data_as_list)} records")
        with open(filename, "wt") as ofp:
            for rec in data_as_list:
                ofp.write("  {}\n".format(rec))


if __name__ == "__main__":
    import sys
    print("Running")
    master = sys.argv[1]
    print(f"Checking pattern file {master}")
    pb = PatternBuilder(master_file=master)
    print("Finished")

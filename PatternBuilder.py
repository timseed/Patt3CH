import pandas as pd


class PatternBuilder:

    def call_to_skimmer_format(self, prefix_length:int, call:str) -> str:
        """

        :param prefix_length:
        :param call:
        :return:
        """
        for pos in range(0,len(call)+1):
            output=[]
            for c in call[pos:]:
                if c.isnumeric():
                    output.append("#")
                elif c.isalpha():
                    output.append("@")
                else:
                    output.append(c)
            template_str= "".join(output)
            if template_str.startswith('@#@'):
                #Only the 1st two chars of the original are needed
                return call[:2]+template_str[2:]
            if template_str.startswith('#@@'):
                # need 1st 4 chars of the original are needed
                return call[:4]+template_str[4:]
            else:
                return call[:prefix_length]+template_str[prefix_length:]




    def old_call_to_skimmer_format(self, prefix_length, call):
        if len(call) > prefix_length:
            output = [call[0:prefix_length]]
            for c in call[prefix_length:]:
                if c.isnumeric():
                    output.append("#")
                elif c.isalpha():
                    output.append("@")
                else:
                    output.append(c)
            return "".join(output)
        else:
            return call

    def __init__(self, master_file="MASTER.SCP"):
        junk = 1
        self.data = []
        self.df = self.load(master_file)
        self.makecolumns()
        for n in range(0, 5):
            self.output(f"format{n}.lst", self.df[f"SKIMMER_FORMAT_G{n}"].unique())
        self.current_version = '0.1.0'


    def load(self, filename: str) -> pd.DataFrame:
        print(f"Loading {filename}")
        with open(filename, "rt") as mt:
            self.data = [d for d in mt.read().upper().split("\n")[4:] if len(d) > 0]
        d = pd.DataFrame(self.data)
        d.columns = ["CALLS"]
        return d

    def makecolumns(self):
        for n in range(0, 5):
            self.df[f"STARTS{n}"] = self.df.CALLS.apply(lambda x: (x + "  ")[0:n])
        for n in range(0, 5):
            self.df[f"SKIMMER_FORMAT_G{n}"] = self.df.CALLS.apply(
                lambda x: self.call_to_skimmer_format(n, x)
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

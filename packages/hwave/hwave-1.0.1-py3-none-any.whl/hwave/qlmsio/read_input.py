import logging
import numpy as np
import re
from requests.structures import CaseInsensitiveDict

logger = logging.getLogger("qlms").getChild("read_input")


class QLMSInput():
    valid_namelist = ["trans", "coulombinter", "coulombintra", "pairhop", "hund", "exchange", "ising", "pairlift", "interall", "initial", "onebodyg"]
    def __init__(self, file_name_list, solver_type="UHFr"):
        self.file_names = file_name_list
        self.ham_param = CaseInsensitiveDict()
        self.ham_param["Transfer"] = self._read_ham("trans", value_type="complex")
        self.ham_param["CoulombInter"] = self._read_ham("coulombinter")
        self.ham_param["CoulombIntra"] = self._read_ham("coulombintra")
        self.ham_param["PairHop"] = self._read_ham("pairhop")
        self.ham_param["Hund"] = self._read_ham("hund")
        self.ham_param["Exchange"] = self._read_ham("exchange")
        self.ham_param["Ising"] = self._read_ham("Ising")
        self.ham_param["PairLift"] = self._read_ham("PairLift")
        self.ham_param["Interall"] = self._read_ham("interall", value_type="complex")
        # TODO Check Pair(Hermite or not)
        # TODO Check site is larger than defined lattics size
        # TODO Add validation function (ex.:Check site is smaller than defined lattics size)
        self.green = CaseInsensitiveDict()
        self.green["Initial"] = self._read_ham("initial", value_type="complex")
        self.green["OneBodyG"] = self._read_green("onebodyg")

    def get_param(self, key):
        if key == "mod" or key == "parameter":
            #return self.mod_param
            return None
        elif key == "ham" or key == "hamiltonian":
            return self.ham_param
        elif key == "output" or key == "green":
            return self.green
        else:
            # Add error message
            logger.error("Get_param: key must be mod or ham or output.")
            return None

    def _read_para(self, file_key, start_line=5):
        file_name = self.file_names[file_key]
        value = CaseInsensitiveDict()
        with open(file_name, "r") as f:
            lines = f.readlines()
            match_pattern = r'^\s*(#.*|)$'
            for line in lines[start_line:]:
                match = re.match(match_pattern, line)
                if not match:
                    words = line.split()
                    value[words[0]] = words[1:]
        return value

    def _read_ham(self, file_key, value_type="real"):
        if file_key in self.file_names:
            file_name = self.file_names[file_key]
            return self._load_text(file_name, value_type)
        else:
            return None

    def _read_green(self, file_key):
        if file_key in self.file_names:
            file_name = self.file_names[file_key]
            data = np.loadtxt(file_name, skiprows = 5)
        else:
            return None
        return data

    def _load_text(self, file_name, value_type):
        if value_type == "real":
            value_width = 1
            _make_value = lambda v: float(v[0])
        elif value_type == "complex":
            value_width = 2
            _make_value = lambda v: float(v[0]) + 1j * float(v[1])
        else:
            value_width = 0
            _make_value = lambda v: None

        data = {}
        with open(file_name, "r") as f:
            lines = f.readlines()
            count = int(lines[1].split()[1])
            data = {}
            ndup = 0
            for line in lines[5:]:
                values = line.split()
                list = tuple([int(i) for i in values[:-value_width]])
                value = _make_value(values[-value_width:])
                if list in data:
                    ndup += 1
                    data[list] += value
                else:
                    data[list] = value

        # check
        err = 0
        if len(data) != count:
            logger.error("incorrect number of lines in {}: expected={}, found={}".format(file_name, count, len(data)))
            err += 1
        if ndup > 0:
            logger.error("duplicate items found in {}".format(file_name))
            err += 1
        if err > 0:
            exit(1)

        return data

if __name__ == '__main__':
    qml_input = QLMSInput({"trans": "trans.def"})

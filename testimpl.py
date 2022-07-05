import structs
import sys
from types import SimpleNamespace as ns



# Instantiate gates
NODES = {
    "Ain": structs.IO("input"),
    "Bin": structs.IO("input"),
    "Cin": structs.IO("input"),
    "xor0": structs.Gate("xor"),
    "and0": structs.Gate("and"),
    "xor1": structs.Gate("xor"),
    "and1": structs.Gate("and"),
    "or0": structs.Gate("or"),
    "Sout": structs.IO("output"),
    "Cout": structs.IO("output")
}


# Link (this is what the GUI/TUI would be great for)

NODES["xor0"].io.in0.append(NODES["Ain"])
NODES["xor0"].io.in1.append(NODES["Bin"])

NODES["and0"].io.in0.append(NODES["Ain"])
NODES["and0"].io.in1.append(NODES["Bin"])

NODES["xor1"].io.in0.append(NODES["xor0"])
NODES["xor1"].io.in1.append(NODES["Cin"])

NODES["and1"].io.in0.append(NODES["xor0"])
NODES["and1"].io.in1.append(NODES["Cin"])

NODES["or0"].io.in0.append(NODES["and0"])
NODES["or0"].io.in1.append(NODES["and1"])

NODES["Sout"].io.in0.append(NODES["xor1"])
NODES["Cout"].io.in0.append(NODES["or0"])



NODES["Ain"].state = bool(int(sys.argv[1]))
NODES["Bin"].state = bool(int(sys.argv[2]))
if len(sys.argv) > 3:
    NODES["Cin"].state = bool(int(sys.argv[3]))


def recursivelyEvalLogicTree(out):
    if "in0" in out.io.__dict__.keys():
        for inp in out.io.in0:
            recursivelyEvalLogicTree(inp)
    if "in1" in out.io.__dict__.keys():
        for inp in out.io.in1:
            recursivelyEvalLogicTree(inp)

    if out.type != "input":
        out.evaluate()


def evalAll(nodes):
    outs = []
    for name, node in nodes.items():
        if node.type == "output":
            outs.append(node)

    for out in outs:
        recursivelyEvalLogicTree(out)

sys.setrecursionlimit(65536) # Handle massive simulations
evalAll(NODES)


print("A:", NODES["Ain"].state)
print("B:", NODES["Bin"].state)
print("Cin", NODES["Cin"].state)
print("Sout:", NODES["Sout"].state)
print("Cout:", NODES["Cout"].state)

from types import SimpleNamespace as SNs


class Gate:
    def __init__(self, nodetype):
        gatetypes = ["and", "or", "not", "nand", "nor", "xor", "xnor", "buf"]
        if nodetype in gatetypes:
            self.type = nodetype
        else:
            raise Exception(f"Invalid gate type `{nodetype}'. Must be in {gatetypes}.")
            # Look, I don't bother to memorise all 600 py exceptions

        self.state = False
        io = {
            "in0": []
        }
        if self.type not in ["not", "buf"]:
            io["in1"] = []
        self.io = SNs(**io)

        match self.type:
            case "and":
                def evaluate():
                    in0 = False
                    in1 = False
                    for inp in self.io.in0:
                        if inp.state:
                            in0 = True
                            break
                    for inp in self.io.in1:
                        if inp.state:
                            in1 = True
                            break
                    self.state = in0 & in1

            case "or":
                def evaluate():
                    self.state = any(inp.state for inp in self.io.in0 + self.io.in1)

            case "not":
                def evaluate():
                    self.state = ~any(inp.state for inp in self.io.in0)

            case "nand":
                def evaluate():
                    in0 = True
                    in1 = True
                    for inp in self.io.in0:
                        if inp.state:
                            in0 = False
                            break
                    for inp in self.io.in1:
                        if inp.state:
                            in1 = False
                            break
                    self.state = in0 & in1

            case "nor":
                def evaluate():
                    self.state = True
                    for inp in self.io.in0 + self.io.in1:
                        if inp.state:
                            self.state = False
                            break

            case "xor":
                def evaluate():
                    in0 = False
                    in1 = False
                    for inp in self.io.in0:
                        if inp.state:
                            in0 = True
                            break
                    for inp in self.io.in1:
                        if inp.state:
                            in1 = True
                            break
                    self.state = in0 ^ in1

            case "xnor":
                def evaluate():
                    in0 = True
                    in1 = True
                    for inp in self.io.in0:
                        if inp.state:
                            in0 = False
                            break
                    for inp in self.io.in1:
                        if inp.state:
                            in1 = False
                            break
                    self.state = in0 ^ in1

            case "buf":
                def evaluate():
                    self.state = any(inp.state for inp in self.io.in0)

            case _:
                def evaluate():
                    raise Exception(f"Gate type {self.type} cannot be evaluated.")

        self.evaluate = evaluate


class IO:
    def __init__(self, nodetype):
        if nodetype in ["input", "output"]:
            self.type = nodetype
        else:
            raise Exception(f"Invalid I/O type `{nodetype}'.")

        self.state = False
        io = {}
        if self.type == "output":
            io["in0"] = []
        self.io = SNs(**io)

        if self.type == "output":
            def evaluate():
                if any(inp.state for inp in self.io.in0):
                    self.state = True

            self.evaluate = evaluate

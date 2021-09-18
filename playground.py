class Comm:
    @staticmethod
    def name():
        raise NotImplementedError("Command needs to have a name!")

    def __init__(self):
        pass

class AndComm (Comm):
    @staticmethod
    def name():
        return "and"

    def __init__(self):
        super().__init__()

class OrComm (Comm):

    @staticmethod
    def name():
        return "or"

    def __init__(self):
        super().__init__()


class XorComm (OrComm):
    def __init__(self):
        super().__init__()

for c in Comm.__subclasses__():
    print(str(c))
    print(c.name())

class Command:
    def __init__(self):
        pass

    @staticmethod
    def name():
        raise NotImplementedError("Command needs to have a name!")

    @staticmethod
    def ephemeral():
        return False

    @staticmethod
    def handle():
        raise NotImplementedError("Command needs to return a response!")

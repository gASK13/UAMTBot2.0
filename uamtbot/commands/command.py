class Command:
    @staticmethod
    def generate_reply(text):
        return {
            "content": text,
            "allowed_mentions": {
                "parse": []
            }
        }

    @staticmethod
    def type():
        return 1  # default type is "slash"

    @staticmethod
    def name():
        return None

    @staticmethod
    def ephemeral():
        return False

    @staticmethod
    def handle(body):
        raise NotImplementedError("Command needs to return a response!")

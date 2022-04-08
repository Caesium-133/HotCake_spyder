class NoRespondException(Exception):
    def __init__(self, who):
        self.who = who


class UnableToDealException(Exception):
    def __init__(self, who):
        self.who = who


class WeNeedCheckException(Exception):
    def __init__(self, who):
        self.who= who


class RetryMayWorkException(Exception):
    def __init__(self, who):
        self.who=who
class NoRespondException(Exception):
    def __init__(self, who):
        self.who = who


class UnableToDealException(Exception):
    def __init__(self, who):
        self.who = who


class WeNeedCheckException(Exception):
    def __init__(self, who):
        self.who = who


class RetryMayWorkException(Exception):
    def __init__(self, who):
        self.who = who


class UnWantedGSException(Exception):
    def __init__(self):
        self.describe = "the goodsCode refers to a page that has no item or torism item."

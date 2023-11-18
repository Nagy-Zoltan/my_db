from abc import abstractmethod


class AbstractRequest:

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

from abc import ABC, abstractmethod


class DummyRepositoryABC(ABC):
    @abstractmethod
    async def get(self):
        pass

from abc import abstractmethod

from models.QuoteModel import QuoteModel


class IngestorInterface:

    @classmethod
    @abstractmethod
    def can_ingest(cls, path) -> bool:
        pass

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        pass

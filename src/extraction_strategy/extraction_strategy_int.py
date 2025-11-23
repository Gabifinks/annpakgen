from abc import ABC, abstractmethod
from typing import List


class ExtractionStrategy(ABC):
    @abstractmethod
    def extract_seq(self, strategy: List[str]):
        ...
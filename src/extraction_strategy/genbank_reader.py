#!/usr/bin/python3

# Base imports
from typing import List

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class GenBankReader:
    def __init__(self, strategy: ExtractionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ExtractionStrategy):
        self.strategy = strategy

    def parse_extract(self, genbank_lines: List[str]):
        self.strategy.extract_seq(genbank_lines=genbank_lines)
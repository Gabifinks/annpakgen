#!/usr/bin/python3

from .extraction_strategy_int import ExtractionStrategy


class ProteinExtractionStrategy(ExtractionStrategy):
    def extract_seq(self):
        ...
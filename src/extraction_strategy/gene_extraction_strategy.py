#!/usr/bin/python3

# Base imports
from typing import List

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class GeneExtractionStrategy(ExtractionStrategy):
    def extract_seq(self, genbank_lines: List[str]):
        print("Uhul! Estrutura ok")
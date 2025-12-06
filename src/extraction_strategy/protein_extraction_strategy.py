#!/usr/bin/python3

# Base imports
from typing import List

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class ProteinExtractionStrategy(ExtractionStrategy):
    def extract_seq(self, genbank_lines: List[str], gene: str) -> str:
        print("Protein extraction strategy")

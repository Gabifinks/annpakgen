#!/usr/bin/python3

# Base imports
from typing import List
import re

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class GeneExtractionStrategy(ExtractionStrategy):
    def find_gene(self, genbank_lines: List[str]):
        gene = "rsmI"
        if gene in "".join(genbank_lines):
            return [gene]
        else:
            print("Gene not found")
            return []
        
    def extract_gene(self, genbank_lines: List[str]) -> List[str]:
        for line in genbank_lines:
            if line.startswith("ORIGIN"):
                origin_index = genbank_lines.index(line) + 6
                end_index = genbank_lines.index("//")
                sequence_box = genbank_lines[origin_index:end_index]
    def extract_coordinates(self, genbank_lines: List[str], gene: str = "rsmI") -> List[str]:
        coordinates = []
        for i, line in enumerate(genbank_lines):
            """As coordenadas estão na linha anterior à linha que contém /gene="""
            if line.startswith(f"/gene=\"{gene}\""):
                gene_coord = genbank_lines[i - 1].strip()
                """Extrai a coordenada no formato '123..456'"""
                coord = re.search(r'(\d+\.\.\d+)', gene_coord)
                if coord:
                    coordinates.append(coord.group(1))
        return coordinates                   
    def extract_sequence(self, genbank_lines: List[str], coordinates: str) -> str:
        sequence = """Tenho que extrair a sequência com base nas coordenadas fornecidas anteriormente"""
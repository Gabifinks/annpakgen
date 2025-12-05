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
        
    def find_coordinates(self, genbank_lines: List[str], gene: str = "rsmI") -> List[str]:
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
        
    def find_genome(self, genbank_lines: List[str]) -> List[str]:
        """Extrai a sequência do genoma do bloco entre 'ORIGIN' e '//'."""
        origin_index = None
        end_index = None
    
        for i, line in enumerate(genbank_lines):
            if line.strip().upper().startswith("ORIGIN"):
                origin_index = i + 1
                break
        if origin_index is None:
            return []
    
        for i in range(origin_index, len(genbank_lines)):
            if genbank_lines[i].strip().startswith("//"):
                end_index = i
                break
        if end_index is None:
            return []
    
        sequence_box = genbank_lines[origin_index:end_index]
        return sequence_box
                              
    def extract_sequence(self, genbank_lines: List[str], coordinates: str) -> str:
        """Extrai sequência do genoma e escreve em arquivo de texto."""
        def revcomp(seq: str) -> str:
            tr = str.maketrans("ACGTacgt", "TGCAtgca")
            return seq.translate(tr)[::-1]

        # obter genoma do bloco ORIGIN
        sequence_lines = self.find_genome(genbank_lines)
        genome = "".join(re.sub(r'[^ACGTacgt]', '', ln) for ln in sequence_lines).upper()

        # gene alvo
        gene = "rsmI"

        # coordenadas
        coords_list = self.find_coordinates(genbank_lines, gene)

        # detectar complement
        is_complement = False
        for i, line in enumerate(genbank_lines):
            if line.strip().startswith(f'/gene="{gene}"'):
                j = i - 1
                while j >= 0:
                    prev = genbank_lines[j].strip()
                    if not prev or prev.startswith("/"):
                        j -= 1
                        continue
                    if 'complement' in prev.lower():
                        is_complement = True
                    break
                break

        
        parts = []
        for coord in coords_list:
            m = re.search(r'(\d+)\.\.(\d+)', coord)
            if m:
                start = int(m.group(1)) - 1
                end = int(m.group(2))
                parts.append(genome[start:end])

        seq = "".join(parts)
        if is_complement:
            seq = revcomp(seq)

        # Output file
        out_file = f"{gene}_sequence.txt"
        with open(out_file, "w") as fh:
            fh.write(f">{gene}\n")
            for i in range(0, len(seq), 60):
                fh.write(seq[i:i+60] + "\n")

        return out_file



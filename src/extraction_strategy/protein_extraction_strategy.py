#!/usr/bin/python3

# Base imports
from typing import List
import re
import os

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class ProteinExtractionStrategy(ExtractionStrategy):
    def _find_gene(self, genbank_lines: List[str], gene: str) -> List[str]:
        # gene = "rsmI"
        if gene in "".join(genbank_lines):
            return True
        else:
            print("Gene not found")
            return False

    def _find_gene_block(self, genbank_lines: List[str], gene: str) -> List[str]:
        start_index = 0
        final_index = 0

        for index, line in enumerate(genbank_lines):
            if f'gene="{gene}"' in line:
                start_index = index - 1
                break

        for index, line in enumerate(genbank_lines[start_index+1:]):
            if 'gene     ' in line:
                final_index = index
                break

        return genbank_lines[start_index:start_index+final_index+1]

    def _get_protein_translation(self, gene_block: List[str]) -> str:
        idx = next(i for i, x in enumerate(gene_block) if "translation" in x)
        translation_info = gene_block[idx:]
        match = re.search(r'translation="([^"]+)', translation_info[0])

        if match:
            seq_initial = match.group(1)
        translation_info[0] = seq_initial

        return ''.join(translation_info).replace('\n', '').strip().replace(' ','').replace('"', '').replace('"','')

    def _write_fasta(self, filename: str, sequence: str, gene: str) -> None:
        with open(filename, "w") as f:
            f.write(f'>{gene}\n{sequence}\n')
            print(f"Arquivo FASTA criado: {filename}")
            print(f"Tamanho da sequência: {len(sequence)} bases")
            print(f"Caminho completo: {os.path.abspath(filename)}")

    def extract_seq(self, genbank_lines: List[str], gene: str) -> str:
        print("Protein extraction strategy")
        if self._find_gene(genbank_lines, gene):
            gene_block = self._find_gene_block(genbank_lines, gene)
            sequence = self._get_protein_translation(gene_block)
            if sequence:
                filename = f"{gene}_sequence.fasta"
                try:
                    self._write_fasta(filename, sequence, gene)
                except Exception as e:
                    print(f"Erro ao salvar arquivo: {e}")




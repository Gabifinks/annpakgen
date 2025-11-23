#!/usr/bin/python3

# Base imports
from pathlib import Path
from typing import List
import argparse

# Project imports
from extraction_strategy.gene_extraction_strategy import GeneExtractionStrategy
from extraction_strategy.genbank_reader import GenBankReader

def read_genbank_file(file_path: Path) -> List[str]:
    with open(file_path, 'r') as file_content:
        return file_content.readlines()


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-gf', '--genbank_file', required=True)
    args = parser.parse_args()
    genbank_lines = read_genbank_file(file_path=Path(args.genbank_file))

    gen_reader = GenBankReader(strategy=GeneExtractionStrategy())
    genes = gen_reader.parse_extract(genbank_lines=genbank_lines)

    #chama o modulo so caso queira outra estrategia
    #gen_reader.set_strategy(ProteinExtractionStrategy())
    #proteins = gen_reader.parse(genbank_lines)
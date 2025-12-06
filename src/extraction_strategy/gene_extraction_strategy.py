#!/usr/bin/python3

# Base imports
from typing import List
import re
import os

# Project imports
from .extraction_strategy_int import ExtractionStrategy


class GeneExtractionStrategy(ExtractionStrategy):
    def find_gene(self, genbank_lines: List[str]) -> List[str]:
        gene = "rsmI"
        if gene in "".join(genbank_lines):
            return [gene]
        else:
            print("Gene not found")
            return []
        
    def find_coordinates(self, genbank_lines: List[str], gene: str = "rsmI") -> List[str]:
        """Encontra as coordenadas do gene especificado."""
        coordinates = []
        for i, line in enumerate(genbank_lines):
            if f'/gene="{gene}"' in line:
                # Procura nas linhas anteriores pelo padrão de coordenadas
                for j in range(max(0, i-3), i):
                    # Procura por 'gene' na linha e extrai coordenadas
                    if 'gene' in genbank_lines[j]:
                        match = re.search(r'(\d+\.\.\d+)', genbank_lines[j])
                        if match:
                            coordinates.append(match.group(1))
                            break
        return coordinates
        
    def find_genome(self, genbank_lines: List[str]) -> List[str]:
        """Extrai a sequência do genoma do bloco entre 'ORIGIN' e '//'."""
        for i, line in enumerate(genbank_lines):
            if line.strip().upper().startswith("ORIGIN"):
                origin_index = i + 1
                break
        else:
            return []
        
        for i in range(origin_index, len(genbank_lines)):
            if genbank_lines[i].strip().startswith("//"):
                return genbank_lines[origin_index:i]
        
        return []
    
    def extract_seq(self, genbank_lines: List[str]) -> str:
        """
        Extrai a sequência do gene 'rsmI' e salva em arquivo FASTA.
        """
        # 1. Encontrar o gene
        genes = self.find_gene(genbank_lines)
        if not genes:
            return ""
        gene_name = genes[0]
        
        # 2. Encontrar coordenadas
        coordinates = self.find_coordinates(genbank_lines, gene_name)
        if not coordinates:
            return ""
        
        # 3. Extrair e limpar sequência do genoma
        genome_lines = self.find_genome(genbank_lines)
        if not genome_lines:
            return ""
        
        # Concatena e limpa a sequência completa
        genome = ''.join(re.sub(r'[^A-Za-z]', '', line).upper() for line in genome_lines)
        
        # 4. Extrair a sequência do gene
        match = re.search(r'(\d+)\.\.(\d+)', coordinates[0])
        if not match:
            return ""
        
        start = int(match.group(1)) - 1  # Converter para 0-based
        end = int(match.group(2))
        
        if not (0 <= start < end <= len(genome)):
            return ""
        
        sequence = genome[start:end]
        
        # 5. Verificar se é complementar
        is_complement = any(
            f'/gene="{gene_name}"' in line and any(
                'complement' in genbank_lines[j] 
                for j in range(max(0, i-3), i)
            )
            for i, line in enumerate(genbank_lines)
        )
        
        # 6. Aplicar complemento reverso se necessário
        if is_complement:
            complement_map = str.maketrans("ACGTacgt", "TGCAtgca")
            sequence = sequence.translate(complement_map)[::-1]
        
        # 7. Salvar em arquivo FASTA
        if sequence:
            filename = f"{gene_name}_sequence.fasta"
            try:
                with open(filename, "w") as f:
                    f.write(f">{gene_name} | coordinates: {coordinates[0]}")
                    if is_complement:
                        f.write(" | complement")
                    f.write("\n")
                    
                    for i in range(0, len(sequence), 60):
                        f.write(sequence[i:i+60] + "\n")
                
                print(f"Arquivo FASTA criado: {filename}")
                print(f"Tamanho da sequência: {len(sequence)} bases")
                print(f"Caminho completo: {os.path.abspath(filename)}")
                
            except Exception as e:
                print(f"Erro ao salvar arquivo: {e}")
        
        return sequence
    
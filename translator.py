from Bio.Seq import Seq

print("--- GULBIA V3: Biological Translation Module ---")

# 1. We define a normal snippet of Liver Cell DNA
# (This is just an example sequence that is a multiple of 3)
normal_dna = Seq("ATGCGTACGAAATAG")

# 2. We use Biopython to translate that DNA into a chain of Amino Acids (a Protein)
normal_protein = normal_dna.translate()

print(f"\n[NORMAL CELL]")
print(f"DNA Sequence:     {normal_dna}")
print(f"Resulting Protein: {normal_protein}")

# 3. Now, we simulate the mutation GULBIA found in your VCF file. 
# Let's say the 'A' in the exact middle mutated into a 'T'.
mutated_dna = Seq("ATGCGTTCCAAATAG")

# 4. We translate the mutated cancer DNA
mutated_protein = mutated_dna.translate()

print(f"\n[CANCER CELL]")
print(f"Mutated DNA:       {mutated_dna}")
print(f"Mutant Neoantigen: {mutated_protein}")

print("\n--- Translation Complete ---")
import random

class ANIMA_CFG:
    # Life
    LIFE = 1

    # Codon
    CODON = ["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "J", "K", "L", "M", "N",
             "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]

    # Reproduction
    REPRO_THRESHOLD = 7
        # List of important valus:
        # Max(n)    1       2       3       4       5
        # Sum       1       1.875   2.688   3.469   4.234
        # Max(n)    6       7       8       9       10
        # Sum       4.992   5.746   6.498   7.249   7.9995
    
    
    # Expression
    PROMOTER_BOOST = 0.25
    BASE_EXPRESSION = 1 - PROMOTER_BOOST
    DECAY = 0.5

    # Mutation
    MUTATION_RATE = 0.2    # 20%
    MUTATION_TYPE = ["Substitution", "Insertion", "Deletion", "Inversion", "Duplication"]

    DUPLICATION_START = 1
    DUPLICATION_END = 2

CFG = ANIMA_CFG


class Anima:
    """
    A single anima, the start of the whole cosmos.
    Fiat vita!
    """

    def __init__(self):
        self.uid = 1
        self.parent_uid = 0
        self.generation = 1
        self.genome = {
            "tel_l": "ABCABCABC",       # Telomere_left
            "start": "SSS",             # Start Codon
            "functional": "CCCCCCCCCC", # Functional Area
            "stop": "EEE",              # Stop Codon
            "tel_r": "ABCABCABC"        # Telomere_right
        }
        self.life: int = CFG.LIFE

    def can_reproduce(self) -> bool:
        return self.express().get("C", 0) > CFG.REPRO_THRESHOLD

    def reproduction(self, uid) -> "Anima":
        child = Anima()
        child.genome = self.genome.copy()
        child.uid = uid
        child.parent_uid = self.uid
        child.generation = self.generation + 1

        if random.random() < CFG.MUTATION_RATE:
            child.genome["functional"] = self.mutation(random.choice(CFG.MUTATION_TYPE))

        # TODO: complexer mutation during replication
        return child

    def express(self) -> dict[str, int]:
        seq = self.genome["functional"]
        out = {}
        for n, char in enumerate(seq):
            w = CFG.BASE_EXPRESSION + CFG.PROMOTER_BOOST * (CFG.DECAY ** n)
            out[char] = out.get(char, 0) + w
        return out

    def mutation(self, op) -> str:
        seq = list(self.genome["functional"])

        match op:
            case "Substitution":
                if not seq:
                    return ""

                location = random.randrange(len(seq))
                while True:
                    new_base = random.choice(CFG.CODON)
                    if new_base != seq[location]:
                        seq[location] = new_base
                        break

            case "Insertion":
                location = random.randrange(len(seq) + 1)
                new_base = random.choice(CFG.CODON)
                seq.insert(location, new_base)

            case "Deletion":
                if not seq:
                    return ""

                location = random.randrange(len(seq))
                seq.pop(location)

            case "Inversion":
                if len(seq) < 2:
                    return "".join(seq)

                left, right = sorted(random.sample(range(len(seq)), 2))
                seq[left:right + 1] = seq[left:right + 1][::-1]

            case "Duplication":
                if not seq:
                    return ""

                location = random.randrange(len(seq))
                times = random.randint(
                    CFG.DUPLICATION_START,
                    CFG.DUPLICATION_END
                )

                base = seq[location]
                seq[location:location] = [base] * times
                # TODO: Support segmental duplication in future versions.

            case _:
                raise ValueError(f"Unknown mutation: {op}")

        return "".join(seq)
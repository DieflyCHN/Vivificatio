import random

class ANIMA_CFG:
    # Life
    LIFE = 10

    # Codon
    CODON = ["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "J", "K", "L", "M", "N",
             "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]
    # UYZ: Telomere specific codon
    # C: Copy
    # D: Double reproduction (2 children)
    # H: Higher mutation rate
    # L: Lower mutation rate
    # P: Protect Telomere
    P_EFFECT = -0.05
    # X: "Recessive homozygous pathogenic", 1X = safe, 2X = infertile
    # Q: Quicker reproduction (earlier reproductive age)    # TODO: reproductive age

    # Reproduction
    REPRO_THRESHOLD = 7
        # List of important valus:
        # Max(n)    1       2       3       4       5
        # Sum       1       1.875   2.688   3.469   4.234
        # Max(n)    6       7       8       9       10
        # Sum       4.992   5.746   6.498   7.249   7.9995
    
    # Expression weight
    PROMOTER_BOOST = 0.25
    BASE_EXPRESSION = 1 - PROMOTER_BOOST
    DECAY = 0.5

    # Telemere
    TELEMERE_LOC = ["tel_l", "tel_r"]
    
    # Mutation
    MUTATION_TYPE = ["Substitution", "Insertion", "Deletion", "Inversion", "Duplication"]
    DUPLICATION_START = 1
    DUPLICATION_END = 2
    
    MUTATION_RATE_FUN = 0.2   # 20%
    MUTATION_RATE_TEL = 0.9   # 90%


CFG = ANIMA_CFG

class Anima:
    """
    A single anima, the start of the whole cosmos.
    Fiat vita!
    """

    def __init__(self, *, uid=1, parent_uid=0, generation=1, genome=None):
        self.uid = uid
        self.parent_uid = parent_uid
        self.generation = generation
        self.life: int = CFG.LIFE
        self.genome = genome if genome is not None else{
            "tel_l": "UYZUYZUYZ",       # Telomere_left
            "start": "SSS",             # Start Codon
            "functional": "CCCCCCCCCC", # Functional Area
            "stop": "EEE",              # Stop Codon
            "tel_r": "UYZUYZUYZ"        # Telomere_right
        }
        self.func_expr_by_freq = {}
        self.func_expr_by_weig = {}
        self.telo_length = 0
        self.update_codon_stat()

    def can_reproduce(self) -> bool: 
        if self.telo_length <= 16:
            return False
        if self.func_expr_by_freq.get("X", 0) >= 2:
            return False
        return self.func_expr_by_weig.get("C", 0) > CFG.REPRO_THRESHOLD

    def reproduction(self, uid) -> "Anima":
        genome = self.genome.copy()

        if random.random() < CFG.MUTATION_RATE_FUN:
            genome["functional"] = self.mutation(random.choice(CFG.MUTATION_TYPE), "functional")

        p_expr = self.func_expr_by_weig.get("P", 0)
        tel_rate = CFG.MUTATION_RATE_TEL + p_expr * CFG.P_EFFECT
        if random.random() < tel_rate:
            tele_loc = random.choice(CFG.TELEMERE_LOC)
            genome[tele_loc] = self.mutation("Deletion", tele_loc)

        return Anima(uid=uid, parent_uid=self.uid, generation=self.generation + 1, genome=genome)

    def express_by_frequency(self, genome_char) -> dict[str, int]:
        seq = self.genome[genome_char]
        out = {}
        for n, char in enumerate(seq):
            out[char] = out.get(char, 0) + 1
        return out

    def express_by_weight(self, genome_char) -> dict[str, int]:
        seq = self.genome[genome_char]
        out = {}
        for n, char in enumerate(seq):
            w = CFG.BASE_EXPRESSION + CFG.PROMOTER_BOOST * (CFG.DECAY ** n)
            out[char] = out.get(char, 0) + w
        return out

    def update_codon_stat(self) -> None:
        self.func_expr_by_freq = self.express_by_frequency("functional")
        self.func_expr_by_weig = self.express_by_weight("functional")
        self.telo_length = len(self.genome["tel_l"]) + len(self.genome["tel_r"])

    def mutation(self, op, genome_char) -> str:
        seq = list(self.genome[genome_char])

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
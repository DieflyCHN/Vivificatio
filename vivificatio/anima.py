import random

class ANIMA_CFG:
    # Life
    LIFE = 10
    REPRODUCE_WILLING = 1   # 100%

    # Codon ------------------------------------------------------------------------
    CODON = ["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "J", "K", "L", "M", "N",
             "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]
    # UYZ: Telomere specific codon

    # C: Copy
    # D: Double reproduction (2 children)
    D_THRESHOLD = 1.875
    # H: Higher mutation rate
    H_EFFECT = 0.1
    # L: Lower mutation rate
    L_EFFECT = -0.1
    # P: Protect Telomere
    P_EFFECT = -0.05
    # X: "Recessive homozygous pathogenic", 1X = safe, 2X = infertile
    # Q: Quicker reproduction (earlier reproductive age)    # TODO: reproductive age and following

    # Codon about resource ---------------------------------------------------------
    # E: Faster (more efficient) energy acquisition
    E_EFFECT = 0.25    # +25% aquisition
    # S: (Sleep) Lower energy consum AND less reproduction willing
    S_EFFECT = [-0.2, -0.1]  # -20% daily consum, -10% rep. willing
    """
    [0]: daily consum (usage: 1 + ...[0])\n
    [1]: reproduction willing (usage: 1+ ...[1])
    """
    # R: Greater energy reserves
    R_EFFECT = 0.15 # +15% reserves
    # M: Low metabolism AND less movement (e.g. finding food)
    M_EFFECT = [-0.9, -0.5] # -90% daily consum, -50% aquisition
    """
    [0]: daily consum (usage: 1 + ...[0])\n
    [1]: aquisition (usage: 1 + ...[1])
    """
    # N: Hunger-resistant, hardy
    N_EFFECT = 1    # Survive for 1 tick more under starving
    # F: No confinement (Possible cause: less energy consum by reproduction)
    F_EFFECT = -0.3 # -30%

    # Energy
    ENERGY_AQUI_EFFICIENCY = 2  # 200%, which means that anima every tick can get "2" food
    ENERGY_CONSUM_DAILY = 1     # For each tick need "1" food
    ENERGY_CONSUM_REPRO = 1     # For each child need "1" food
    ENERGY_RESERVE_MAX = 10     # "10" food
    STARVING_MAX = 3        # 3 ticks

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
    
    MUTATION_RATE_FUN = 0.8   # 80%
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
        self.reproduction_willing = CFG.REPRODUCE_WILLING

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

        self.energy_aqui_efficiency = 0
        self.energy_consum_daily = 0
        self.energy_consum_repro = 0
        self.energy_reserve_max = 0
        self.energy_reserve = 0
        self.starving = 0   # False

        self.update_stat()

    def can_reproduce(self) -> bool: 
        if self.telo_length <= 16:
            return False
        if self.func_expr_by_freq.get("X", 0) >= 2:
            return False
        return self.func_expr_by_weig.get("C", 0) > CFG.REPRO_THRESHOLD

    def can_double_reproduce(self) -> bool:
            return self.func_expr_by_weig.get("D", 0) >= CFG.D_THRESHOLD

    def reproduction(self, uid) -> "Anima":
        genome = self.genome.copy()

        fun_rate = min(max(CFG.MUTATION_RATE_FUN +
                           self.func_expr_by_freq.get("H", 0) * CFG.H_EFFECT +
                           self.func_expr_by_freq.get("L", 0) * CFG.L_EFFECT, 0), 1)
        if random.random() < fun_rate:
            genome["functional"] = self.mutation(random.choice(CFG.MUTATION_TYPE), "functional")

        p_expr = self.func_expr_by_weig.get("P", 0)
        tel_rate = CFG.MUTATION_RATE_TEL + p_expr * CFG.P_EFFECT
        if random.random() < tel_rate:
            tele_loc = random.choice(CFG.TELEMERE_LOC)
            genome[tele_loc] = self.mutation("Deletion", tele_loc)

        self.energy_reserve -= self.energy_consum_repro
        # Warning! Possible starving caused by reproduction will in this version
        # take effects for parent_anima in the next tick, instead of instantly,
        # because do_a_tick() is written before reproduction()
        # IT WILL BE FIXED IN NEXT VERSION. PLEASE SEE TODO IN do_a_tick().   
        return Anima(uid=uid, parent_uid=self.uid, generation=self.generation + 1, genome=genome)

    def express_by_frequency(self, genome_char) -> dict[str, int]:
        seq = self.genome[genome_char]
        out = {}
        for n, char in enumerate(seq):
            if char in ("E", "F", "H", "L", "M", "N", "R", "S", "X"):
                out[char] = out.get(char, 0) + 1
        return out

    def express_by_weight(self, genome_char) -> dict[str, int]:
        seq = self.genome[genome_char]
        out = {}
        for n, char in enumerate(seq):
            if char in ("C", "D", "P"):
                w = CFG.BASE_EXPRESSION + CFG.PROMOTER_BOOST * (CFG.DECAY ** n)
                out[char] = out.get(char, 0) + w
        return out

    def update_stat(self) -> None:
        self.func_expr_by_freq = self.express_by_frequency("functional")
        self.func_expr_by_weig = self.express_by_weight("functional")
        self.telo_length = len(self.genome["tel_l"]) + len(self.genome["tel_r"])

        self.reproduction_willing = (CFG.REPRODUCE_WILLING *
                                     (1 + CFG.S_EFFECT[1]) ** self.func_expr_by_freq.get("S", 0))
        self.energy_aqui_efficiency = (CFG.ENERGY_AQUI_EFFICIENCY
                                       * (1 + CFG.E_EFFECT) ** self.func_expr_by_freq.get("E", 0)
                                       * (1 + CFG.M_EFFECT[1]) ** self.func_expr_by_freq.get("M", 0))
        self.energy_consum_daily = (CFG.ENERGY_CONSUM_DAILY
                                    * (1 + CFG.S_EFFECT[0]) ** self.func_expr_by_freq.get("S", 0)
                                    * (1 + CFG.M_EFFECT[0]) ** self.func_expr_by_freq.get("M", 0))
        self.energy_consum_repro = (CFG.ENERGY_CONSUM_REPRO
                                    * (1 + CFG.F_EFFECT) ** self.func_expr_by_freq.get("F", 0))
        self.energy_reserve_max = (CFG.ENERGY_RESERVE_MAX * 
                                   (1 + CFG.R_EFFECT) ** self.func_expr_by_freq.get("R", 0))

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

    def do_a_tick(self) -> None:
        if self.starving >= CFG.STARVING_MAX + self.func_expr_by_freq.get("N", 0) * CFG.N_EFFECT:
            self.life = 0
            return None
        self.energy_reserve = min(self.energy_reserve_max,
                                  self.energy_reserve + self.energy_aqui_efficiency - self.energy_consum_daily)
        if self.energy_reserve <= 0:
            self.starving += 1
        else:
            self.starving = 0

        # TODO: Make do_a_tick() fully functional, instead of still leaving sth. in cosmos() and reproduction()
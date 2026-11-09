from cosmos import cosmos

import random
import argparse
import logging
import statistics as st

def parse_args():
    parser = argparse.ArgumentParser(description="Vivifiacatio")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable debug mode")
    parser.add_argument("-r", "--rounds", type=int, default=10, help="Simulation rounds")
    parser.add_argument("-s", "--seed", type=int, default=None, help="Specify a random seed")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    return args

def main() -> None:
    args = parse_args()

    seed = args.seed
    if seed is None:
        seed = random.randrange(0, 2 ** 63)
    random.seed(seed)
    print(f"Random seed: {seed}")

    max_rounds = args.rounds
    print(f"Set rounds : {max_rounds}")
    stat_valid = []
    stat_super = 0
    try:
        for _ in range(max_rounds):
            c = cosmos()
            if c == -1:
                continue
            if c == -2:
                stat_super += 1
            else:
                stat_valid.append(c)
    except KeyboardInterrupt:
        print("\tInterrupted.")

    if stat_valid:
        print(
            f"Valid cosmos: {len(stat_valid)}\n"
            f"Max Gen. Observed: {max(stat_valid)}\t"
            f"Mean Max Gen.: {st.mean(stat_valid):.2f}\t"
            f"Median: {st.median(stat_valid)}\t"
            f"Std: {st.pstdev(stat_valid):.2f}"
        )
    if stat_super:
        print(
            f"Super cosmos: {stat_super}\n"
        )

if __name__ == "__main__":
    main()
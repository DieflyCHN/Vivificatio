from cosmos import cosmos

import random
import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser(description="Vivifiacatio")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable debug mode")
    parser.add_argument("-r", "--rounds", type=int, default=1, help="Simulation rounds")
    parser.add_argument("--seed", type=int, default=None, help="Specify a random seed")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    return args

def main():
    args = parse_args()

    seed = args.seed
    if seed is None:
        seed = random.randrange(0, 2 ** 63)
    random.seed(seed)
    print(f"Random seed: {seed}")

    max_rounds = args.rounds
    stat = []
    try:
        for _ in range(max_rounds):
            stat.append(cosmos())
    except KeyboardInterrupt:
        print("\tInterrupted.")

    if stat:
        print(
            f"Rounds: {len(stat)}\t"
            f"Max Gen. Observed: {max(stat)}\t"
            f"Mean Max Gen.: {sum(stat) / len(stat)}"
        )

if __name__ == "__main__":
    main()
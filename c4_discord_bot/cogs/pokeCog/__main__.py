import argparse

from .pokebot_evolved import PokebotEvolved

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a new Pokemon entry', epilog='Original Code By: Willow Dennison')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of entries to generate')
    parser.add_argument('-g', '--gemini', action='store_true', help='Use Gemini to generate descriptions (Requires environment variable GEMINI_API_KEY)')

    args = parser.parse_args()

    pb = PokebotEvolved(use_gemini=args.gemini)
    pb.generateMultipleEntries(n_to_generate=args.count, print_to_console=True)

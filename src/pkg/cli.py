import sys
import argparse
from typing import List, Iterator
from mypkg._Charm import harmonic_mean


def parse_numbers_from_stdin() -> Iterator[float]:
    for line in sys.stdin:
        for token in line.strip().split():
            try:
                yield float(token)
            except ValueError:
                raise ValueError(f"Invalid number in stdin: '{token}'")


def parse_numbers_from_file(path: str) -> Iterator[float]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                for token in line.strip().split():
                    try:
                        yield float(token)
                    except ValueError:
                        raise ValueError(f"Invalid number in file '{path}': '{token}'")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")


def validate_positive(numbers: List[float]) -> None:
    if not numbers:
        raise ValueError("No numbers provided")
    if any(x <= 0 for x in numbers):
        invalid = [x for x in numbers if x <= 0]
        raise ValueError(f"Harmonic mean requires positive numbers only. Invalid values: {invalid}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate harmonic mean of positive numbers",
        epilog="Examples:\n"
               "  harmonic 1 2 4\n"
               "  echo '1 2 4' | harmonic\n"
               "  harmonic -f numbers.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "numbers", 
        nargs="*", 
        type=float,
        help="Numbers to compute harmonic mean (must be > 0)"
    )
    parser.add_argument(
        "-f", "--file",
        metavar="PATH",
        help="Read numbers from file (one or more per line)"
    )
    parser.add_argument(
        "-p", "--precision",
        type=int,
        default=6,
        metavar="N",
        help="Decimal precision of output (default: 6)"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="harmonic 0.1.0"
    )

    args = parser.parse_args()

    try:
        if args.numbers:
            numbers = args.numbers
        elif args.file:
            numbers = list(parse_numbers_from_file(args.file))
        elif not sys.stdin.isatty():
            numbers = list(parse_numbers_from_stdin())
        else:
            parser.print_help()
            sys.exit(1)

        validate_positive(numbers)
        result = harmonic_mean(numbers)

        if args.json:
            import json
            output = {
                "count": len(numbers),
                "harmonic_mean": round(result, args.precision),
                "min": min(numbers),
                "max": max(numbers)
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"{result:.{args.precision}f}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
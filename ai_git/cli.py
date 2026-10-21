import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    

    parser.add_argument(
        "command",
        choices=["commit", "pr"]
    )

    parser.add_argument(
    "--model",
    default="gpt-5-mini"
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=500
    )

    parser.add_argument(
        "--safe-mode",
        action="store_true"
    )

    return parser.parse_args()
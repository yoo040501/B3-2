import argparse
import subprocess
import os

def get_git_status():
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )
    return result.stdout


def get_git_diff():
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )
    return result.stdout


def main():
    parser = argparse.ArgumentParser()


    parser.add_argument(
        "command",
        choices=["commit", "pr"]
    )

    parser.add_argument(
    "--model",
    default="gpt-5.5"
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

    api_key = os.getenv("AI_API_KEY")

    if not api_key:
        print("[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.")
        return
    
    args = parser.parse_args()

    status = get_git_status()

    if not status.strip():
        print("[INFO] 변경 사항이 없습니다.")
        return

    diff = get_git_diff()

    print("=== Git Status ===")
    print(status)

    print("=== Git Diff ===")
    print(diff)

    print("선택한 명령:", args.command)
    print("command:", args.command)
    print("model:", args.model)
    print("temperature:", args.temperature)
    print("max_tokens:", args.max_tokens)
    print("safe_mode:", args.safe_mode)


if __name__ == "__main__":
    main()
# test

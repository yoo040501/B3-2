import os

from ai_git.cli import parse_args
from ai_git.git_utils import get_git_diff, get_git_status
from ai_git.api_client import call_ai
from ai_git.prompts import build_commit_prompt, build_pr_prompt


def run():
    args = parse_args()

    api_key = os.getenv("AI_API_KEY")

    if not api_key:
        print("[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    status = get_git_status()

    if not status.strip():
        print("[INFO] 변경 사항이 없습니다.")
        return

    diff = get_git_diff()

     # print("=== Git Status ===")
    # print(status)

    # print("=== Git Diff ===")
    # print(diff)

    # print("선택한 명령:", args.command)
    # print("command:", args.command)
    # print("model:", args.model)
    # print("temperature:", args.temperature)
    # print("max_tokens:", args.max_tokens)
    # print("safe_mode:", args.safe_mode)

    if args.command == "commit":
        prompt = build_commit_prompt(status, diff)
    else:
        prompt = build_pr_prompt(status, diff)

    response = call_ai(
        api_key,
        prompt,
        args.model
    )

    if response is None:
        print("[ERROR] AI API 요청에 실패했습니다.")
        return

    if response.status_code != 200:
        print("[ERROR] AI API 호출 실패")
        print(response.text)
        return

    content = response.json()["choices"][0]["message"]["content"]

    if args.command == "commit":
        print("\n--- Commit Message ---")
        print(content)
        print("----------------------")

    else:
        print("\n--- PR Draft ---")
        print(content)
        print("----------------")
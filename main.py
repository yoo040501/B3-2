import argparse
import requests
import subprocess
import os
import time

def call_ai(api_key, prompt, model):
    url = "https://copa.codyssey.kr/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    for attempt in range(2):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response

            print(
                f"[WARN] AI API 호출 실패 "
                f"({response.status_code}), "
                f"시도 {attempt + 1}/2"
            )

        except requests.exceptions.RequestException as e:
            print(f"[WARN] 네트워크 오류: {e}")

        if attempt == 0:
            time.sleep(1)

    return response

def build_commit_prompt(status, diff):
    return f"""
다음 Git 변경사항을 분석해서 커밋 메시지를 작성해주세요.

규칙:
- 첫 줄은 반드시 커밋 제목
- 제목은 Conventional Commit 형식 사용
  예: Feat:, Fix:, Refactor:, Docs:, Chore:
- 제목은 가능하면 50자 이내, 최대 72자
- 제목 다음에는 빈 줄
- 본문은 핵심 변경사항 1~3개만 bullet로 작성
- 불필요하게 세부 구현을 길게 나열하지 않기
- 결과에는 커밋 메시지만 출력하고 설명은 추가하지 않기

Git Status:
{status}

Git Diff:
{diff}
"""

def build_pr_prompt(status, diff):
    return f"""
다음 Git 변경사항을 바탕으로 PR 초안을 작성해주세요.

규칙:
- 첫 줄은 PR 제목
- 제목은 최대 80자
- 제목 다음에는 빈 줄
- 본문에는 Why, What, How to Test를 순서대로 작성
- 각 항목에는 최소 1개의 bullet 작성
- 다른 설명은 작성하지 않기

출력 형식:

## Why
- 변경 이유

## What
- 주요 변경 내용

## How to Test
- 테스트 방법

Git Status:
{status}

Git Diff:
{diff}
"""

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

    args = parser.parse_args()
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

    # print("prompt length:", len(prompt))
    # print("diff length:", len(diff))
    response = call_ai(
        api_key,
        prompt,
        args.model
    )

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]

        if args.command == "commit":
            print("\n--- Commit Message ---")
            print(content)
            print("----------------------")

        elif args.command == "pr":
            print("\n--- PR Draft ---")
            print(content)
            print("----------------")
    else:
        print("[ERROR] AI API 호출 실패")
        print(response.text)


if __name__ == "__main__":
    main()

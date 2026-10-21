import os

from ai_git.cli import parse_args
from ai_git.git_utils import get_git_diff, get_git_status, limit_diff
from ai_git.api_client import call_ai
from ai_git.prompts import build_commit_prompt, build_pr_prompt
from ai_git.sanitizer import mask_sensitive_info
from ai_git.validator import validate_commit, validate_pr

def run():
    args = parse_args()

    if not 0 <= args.temperature <= 2:
        print("[ERROR] temperature는 0~2 사이여야 합니다.")
        return

    if args.max_tokens <= 0:
        print("[ERROR] max_tokens는 1 이상이어야 합니다.")
        return
    
    api_key = os.getenv("AI_API_KEY")

    ############################################################
    ##                       Git 관련 부분                      ##
    ############################################################
    if not api_key:
        print("[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.")
        return

    try:
        status = get_git_status()
        diff = get_git_diff()

    except RuntimeError as e:
        print(f"[ERROR] {e}")
        return

    if not status.strip():
        print("[INFO] 변경 사항이 없습니다.")
        return

    file_count = len(status.splitlines())

    print(
        f"[INFO] Git status 수집 완료: "
        f"{file_count}개 파일 변경 감지"
    )

    if args.safe_mode:
        diff = mask_sensitive_info(diff)
        diff = limit_diff(diff)
        print("[INFO] Safe Mode 적용: 민감정보 마스킹 및 diff 200줄 제한")

    diff_lines = len(diff.splitlines())

    print(
        f"[INFO] Git diff 수집 완료: "
        f"{diff_lines}줄"
    )
    ############################################################
    ##                       AI Prompt 부분                    ##
    ############################################################

    print("[INFO] AI API 요청 중...")

    if args.command == "commit":
        prompt = build_commit_prompt(status, diff)
    else:
        prompt = build_pr_prompt(status, diff)

    response = call_ai(
        api_key,
        prompt,
        args.model,
        args.temperature,
        args.max_tokens
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
        valid, error = validate_commit(content)
    else:
        valid, error = validate_pr(content)

    if not valid:
        print(f"[WARN] 출력 형식 검증 실패: {error}")
        
    if args.command == "commit":
        print("[DONE] 커밋 메시지 생성 완료")
    else:
        print("[DONE] PR 초안 생성 완료")

    if args.command == "commit":
        print("\n--- Commit Message ---")
        print(content)
        print("----------------------")

    else:
        print("\n--- PR Draft ---")
        print(content)
        print("----------------")
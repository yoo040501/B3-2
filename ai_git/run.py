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
        return 2

    if args.max_tokens <= 0:
        print("[ERROR] max_tokens는 1 이상이어야 합니다.")
        return 2
    
    api_key = os.getenv("AI_API_KEY")

    ############################################################
    ##                       Git 관련 부분                      ##
    ############################################################
    if not api_key:
        print("[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.")
        print('예: export AI_API_KEY="YOUR_KEY"')
        return 1

    try:
        status = get_git_status()
        diff = get_git_diff()

    except RuntimeError as e:
        print(f"[ERROR] {e}")
        return 1

    if not status.strip():
        print("[INFO] 변경 사항이 없습니다.")
        return

    if not diff.strip():
        print("[INFO] 변경 목록은 있지만 요약할 diff가 없습니다.")
        print("[INFO] 새 파일을 요약하려면 git add 후 다시 실행하세요.")
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

    validate = validate_commit if args.command == "commit" else validate_pr
    request_prompt = prompt

    for attempt in range(2):
        response = call_ai(
            api_key, request_prompt, args.model, args.temperature, args.max_tokens
        )

        if response is None or response.status_code >= 500:
            if attempt == 0:
                print("[WARN] 일시적인 요청 실패로 한 번 더 시도합니다.")
                continue
            if response is None:
                print("[ERROR] 네트워크 오류로 AI 응답을 받지 못했습니다.")
            else:
                print(f"[ERROR] AI 서버 오류 (HTTP {response.status_code})")
            return 1

        if response.status_code != 200:
            print(f"[ERROR] AI API 호출 실패 (HTTP {response.status_code})")
            print(response.text)
            return 1

        try:
            content = response.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError):
            print("[ERROR] AI 응답에서 생성된 텍스트를 찾을 수 없습니다.")
            return 1

        if not isinstance(content, str):
            print("[ERROR] AI 응답의 본문이 텍스트 형식이 아닙니다.")
            return 1

        valid, error = validate(content)
        if valid:
            break

        print(f"[WARN] 출력 형식 검증 실패: {error}")
        if attempt == 1:
            print("[ERROR] 두 번째 응답도 형식에 맞지 않습니다.")
            return 2

        print("[INFO] 검증 결과를 반영해 한 번 더 생성합니다.")
        request_prompt = (
            f"{prompt}\n\n"
            f"이전 응답이 다음 규칙을 위반했습니다: {error}\n"
            "위 Git 변경사항을 바탕으로 해당 규칙을 지켜 다시 작성해주세요."
        )
        
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

    print("[INFO] 생성 결과를 검토한 후 사용하세요.")
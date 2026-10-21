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
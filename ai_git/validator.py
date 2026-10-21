def validate_commit(content):
    lines = content.strip().splitlines()

    if not lines:
        return False, "커밋 메시지가 비어 있습니다."

    title = lines[0]

    if len(title) > 72:
        return False, "커밋 제목이 72자를 초과했습니다."

    return True, None

def validate_pr(content):
    lines = content.strip().splitlines()

    if not lines:
        return False, "PR 내용이 비어 있습니다."

    title = lines[0]

    if len(title) > 80:
        return False, "PR 제목이 80자를 초과했습니다."

    required_sections = [
        "## Why",
        "## What",
        "## How to Test"
    ]

    for section in required_sections:
        if section not in content:
            return False, f"{section} 섹션이 없습니다."

    return True, None
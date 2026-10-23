def validate_commit(content):
    lines = content.strip().splitlines()

    if not lines:
        return False, "커밋 메시지가 비어 있습니다."

    title = lines[0]

    if len(title) > 72:
        return False, "커밋 제목이 72자를 초과했습니다."
    body = lines[1:]

    if body:
        has_bullet = any(
            line.strip().startswith("- ")
            for line in body
        )

        if not has_bullet:
            return False, "커밋 본문에 불릿이 없습니다."
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

    for i, section in enumerate(required_sections):
        start = content.find(section) + len(section)

        if i + 1 < len(required_sections):
            end = content.find(required_sections[i + 1])
            section_content = content[start:end]
        else:
            section_content = content[start:]

        has_bullet = any(
            line.strip().startswith("- ")
            for line in section_content.splitlines()
        )

        if not has_bullet:
            return False, f"{section} 섹션에 불릿이 없습니다."

    return True, None
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

    required_sections = ["## Why", "## What", "## How to Test"]
    title = lines[0].strip()

    if title in required_sections:
        return False, "PR 제목이 없습니다. 첫 줄에 제목을 작성해주세요."

    if len(title) > 80:
        return False, "PR 제목이 80자를 초과했습니다."

    body = [line.strip() for line in lines[1:]]
    headers = [line for line in body if line in required_sections]

    for section in required_sections:
        if section not in headers:
            return False, f"{section} 섹션이 없습니다."

    if headers != required_sections:
        return False, "Why, What, How to Test 섹션을 순서대로 한 번씩 작성해주세요."
    
    for index, section in enumerate(required_sections):
        start = body.index(section) + 1
        end = body.index(required_sections[index + 1]) if index + 1 < len(headers) else len(body)
        if not any(line.startswith("- ") for line in body[start:end]):
            return False, f"{section} 섹션에 불릿이 없습니다."

    return True, None
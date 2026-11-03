import subprocess

def get_git_status():
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Git 저장소가 아니거나 git status 실행에 실패했습니다."
        )
    
    return result.stdout


def get_git_diff():
    parts = []
    for label, command in [
        ("스테이징한 변경", ["git", "diff", "--cached"]),
        ("스테이징하지 않은 변경", ["git", "diff"]),
    ]:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"{label}을 수집하지 못했습니다.")

        if result.stdout.strip():
            parts.append(f"[{label}]\n{result.stdout}")

    return "\n\n".join(parts)

def limit_diff(diff, max_lines=200):
    lines = diff.splitlines()

    if len(lines) <= max_lines:
        return diff

    return "\n".join(lines[:max_lines])

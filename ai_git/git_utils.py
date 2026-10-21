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
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "git diff 실행에 실패했습니다."
        )
    
    return result.stdout

def limit_diff(diff, max_lines=200):
    lines = diff.splitlines()

    if len(lines) <= max_lines:
        return diff

    return "\n".join(lines[:max_lines])

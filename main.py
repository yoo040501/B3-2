import subprocess

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


status = get_git_status()
diff = get_git_diff()

print("=== Git Status ===")
print(status)

print("=== Git Diff ===")
print(diff)

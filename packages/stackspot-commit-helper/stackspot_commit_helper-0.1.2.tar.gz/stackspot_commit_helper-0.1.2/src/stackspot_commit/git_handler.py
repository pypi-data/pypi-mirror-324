import subprocess
import sys

class GitHandler:
    def __init__(self):
        self._validate_git_repository()

    def _validate_git_repository(self) -> None:
        try:
            subprocess.check_output(["git", "rev-parse", "--git-dir"], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            sys.stderr.write("[ERROR] Not a git repository\n")
            sys.exit(1)

    def get_diff(self) -> str:
        try:
            return subprocess.check_output(["git", "diff"]).decode("utf-8")
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"[ERROR] Failed to get git diff: {e}\n")
            sys.exit(1)

    def commit(self, message: str) -> None:
        try:
            subprocess.check_call(["git", "commit", "-am", message])
            print("[SUCCESS] Commit successful")
            subprocess.check_call(["git", "push"])
            print("[SUCCESS] Push successful")
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"[ERROR] Commit failed: {e}\n")
            sys.exit(1)
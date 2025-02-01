import subprocess
import sys
import logging

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GitHandler:
    def __init__(self, include_branch_number=False):
        self.include_branch_number = include_branch_number
        self._validate_git_repository()

    def _validate_git_repository(self) -> None:
        """Checks if the current directory is a valid Git repository."""
        try:
            subprocess.check_output(["git", "rev-parse", "--git-dir"], stderr=subprocess.STDOUT)
            logger.info("Valid Git repository.")
        except subprocess.CalledProcessError:
            logger.error("Not a git repository.")
            sys.exit(1)

    def get_diff(self) -> str:
        """Gets the unstaged changes in the repository."""
        try:
            diff = subprocess.check_output(["git", "diff"]).decode("utf-8")
            logger.debug("Git diff retrieved successfully.")
            return diff
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get git diff: {e}")
            sys.exit(1)

    def get_branch_number(self):
        """Gets the branch number (if available)."""
        try:
            branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode("utf-8")
            branch_number = ''.join(filter(str.isdigit, branch_name))
            if branch_number:
                logger.info(f"Branch number found: {branch_number}")
            return branch_number if branch_number else None
        except subprocess.CalledProcessError:
            logger.warning("Failed to get branch number.")
            return None

    def commit(self, message: str) -> None:
        """Commits and pushes the changes with the provided message."""
        try:
            # Add the branch number to the commit message, if necessary
            if self.include_branch_number:
                branch_number = self.get_branch_number()
                if branch_number:
                    message = f"[#{branch_number}] - {message}"

            # Commit and push
            subprocess.check_call(["git", "commit", "-am", message])
            subprocess.check_call(["git", "push"])
            logger.info(f"Commit and push successful with message: '{message}'")
        except subprocess.CalledProcessError as e:
            logger.error(f"Commit failed: {e}")
            sys.exit(1)

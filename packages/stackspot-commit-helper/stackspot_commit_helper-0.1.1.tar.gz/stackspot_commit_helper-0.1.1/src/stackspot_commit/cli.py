from .git_handler import GitHandler
from .stackspot_service import StackspotService
from .commit_tool import CommitTool
from .config import load_stackspot_config

def main():
    config = load_stackspot_config()
    git_handler = GitHandler()
    stackspot_service = StackspotService(config)
    commit_tool = CommitTool(git_handler, stackspot_service)
    commit_tool.auto_commit()

if __name__ == "__main__":
    main()
import sys
from .git_handler import GitHandler 
from .stackspot_service import StackspotService  

class CommitTool:
    def __init__(self, git_handler: GitHandler, stackspot_service: StackspotService):
        self.git_handler = git_handler
        self.stackspot_service = stackspot_service

    def auto_commit(self) -> None:
        print("[INFO] Starting code commit...")
        diff = self.git_handler.get_diff()
        
        if not diff:
            print("[ERROR] No changes to commit")
            sys.exit(1)

        message = self.stackspot_service.generate_commit_message(diff)
        
        if not message:
            print("[ERROR] Could not generate commit message")
            sys.exit(1)

        self.git_handler.commit(message)
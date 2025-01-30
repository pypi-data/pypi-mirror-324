import sys
import re
from stackspot import Stackspot
from .models import StackspotConfig
from .commit_generator import CommitGenerator  

class StackspotService:
    def __init__(self, config: StackspotConfig):
        self.config = config
        self._setup_stackspot()
        self.commit_gen = CommitGenerator() 

    def _setup_stackspot(self) -> None:
        Stackspot.instance().config({
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'realm': self.config.realm,
        })

    def generate_commit_message(self, diff: str) -> str:
        try:
            execution_id = Stackspot.instance().ai.quick_command.create_execution(
                self.config.quick_command,
                diff
            )

            execution = Stackspot.instance().ai.quick_command.poll_execution(
                execution_id,
                { 
                    'delay': 0.5, 
                    'on_callback_response': lambda e: print(f"[INFO] Execution quick command status: {e['progress']['status']}") 
                }
            )
                        
            if execution['progress']['status'] == 'FAILED':
                raise Exception(f"Execution failed: {execution['progress']['error']}") 
             
            return self.commit_gen.extract_code_block(execution['result'])
        except Exception as e:
            sys.stderr.write(f"[ERROR] StackSpot API error: {e}\n")
            sys.exit(1)

    
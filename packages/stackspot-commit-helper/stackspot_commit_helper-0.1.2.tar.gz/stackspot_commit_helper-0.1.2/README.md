# Stackspot Commit
Intelligent Git commit message generator powered by Stackspot AI.

## Features
- Automatic commit message generation using Stackspot AI
- Smart analysis of git diffs
- Easy integration with existing git workflow

## Getting Stackspot Credentials
- Create an account at Stackspot Platform
- Go to Stackspot AI
- Access "Profile" -> "Access Token"
- Create new credentials and copy:
    - Client ID
    - Client Secret
    - Realm

## Installation

```bash
pip install stackspot-commit-helper
```
- Add the environment variables in the system
    - STACKSPOT_CLIENT_ID=your_client_id
    - STACKSPOT_CLIENT_SECRET=your_client_secret
    - STACKSPOT_REALM=your_realm
    - QUICK_COMMAND_COMMIT=your_quick_command_name - This is optional if the quick command generate-git-commit-message exists in your account.

## Run on terminal
```bash
scommit
```
#!/usr/bin/env python3
"""
Git Credentials Setup Script
Helps configure Git credentials for different accounts
"""

import subprocess
import sys
import getpass

def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error: {result.stderr}")
            return False, result.stdout, result.stderr
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print(f"Exception running command: {cmd}")
        print(f"Error: {str(e)}")
        return False, "", str(e)

def setup_git_credentials(username, password):
    """Set up Git credentials for a specific user"""
    print(f"Setting up credentials for {username}...")
    
    # Configure credential helper
    success, _, error = run_command('git config --global credential.helper store')
    if not success:
        print(f"Failed to set credential helper: {error}")
        return False
    
    # Create credential URL
    credential_url = f"https://{username}:{password}@github.com"
    
    # Test authentication
    print("Testing GitHub authentication...")
    success, _, error = run_command(f'git ls-remote {credential_url}/JMBJ2457/frontend2-projet-frontend_iii.git', check=False)
    
    if success:
        print("✓ Authentication successful!")
        
        # Store credentials (this will create/update .git-credentials)
        with open(f"{getpass.getuser()}\\.git-credentials", "w") as f:
            f.write(f"{credential_url}\n")
        
        return True
    else:
        print("✗ Authentication failed!")
        print(f"Error: {error}")
        return False

def main():
    print("=== Git Credentials Setup ===")
    print("This script helps set up GitHub credentials for team members.")
    print("\nAvailable accounts:")
    print("1. Martin Bogarin (JMBJ2457)")
    print("2. Pablo Rosas (PavlovRR)")
    print("3. Manual setup")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        username = "JMBJ2457"
        password = getpass.getpass("Enter password for Martin Bogarin: ")
    elif choice == "2":
        username = "PavlovRR"
        password = getpass.getpass("Enter password for Pablo Rosas: ")
    elif choice == "3":
        username = input("Enter GitHub username: ").strip()
        password = getpass.getpass("Enter password: ")
    else:
        print("Invalid choice")
        sys.exit(1)
    
    if setup_git_credentials(username, password):
        print("\n✓ Credentials configured successfully!")
        print("You can now push/pull from the repository.")
        print("\nNext steps:")
        print("1. Run 'python setup_git_accounts.py' to configure your user identity")
        print("2. Create your branch: 'git checkout -b your-name origin/main'")
        print("3. Push your branch: 'git push --set-upstream origin your-name'")
    else:
        print("\n✗ Failed to configure credentials")
        print("Please check your username and password.")
        sys.exit(1)

if __name__ == "__main__":
    main()

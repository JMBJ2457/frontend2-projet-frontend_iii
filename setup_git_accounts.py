#!/usr/bin/env python3
"""
Git Account Setup Script
Helps configure Git user identity based on selected account
"""

import subprocess
import sys

# Define your accounts
ACCOUNTS = {
    "1": {
        "name": "Eduardo Aispuro",
        "email": "luis.mejiaaispuro@cesun.edu.mx",
        "username": "EduardoAispuro"
    },
    "2": {
        "name": "Martin Bogarin",
        "email": "martin.bogarin@example.com", 
        "username": "JMBJ2457"
    },
    "3": {
        "name": "Pablo Rosas",
        "email": "pablo.rosas@example.com",
        "username": "PavlovRR"
    },
    "4": {
        "name": "Account 4 Name", 
        "email": "account4@example.com",
        "username": "username4"
    }
}

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def configure_git_account(account):
    """Configure Git with the selected account"""
    success, _, error = run_command(f'git config user.name "{account["name"]}"')
    if not success:
        print(f"Error setting name: {error}")
        return False
    
    success, _, error = run_command(f'git config user.email "{account["email"]}"')
    if not success:
        print(f"Error setting email: {error}")
        return False
    
    return True

def main():
    print("=== Git Account Configuration ===")
    print("Select which account to use for commits:")
    
    for key, account in ACCOUNTS.items():
        print(f"{key}. {account['name']} ({account['email']})")
    
    while True:
        choice = input("\nEnter account number (1-4): ").strip()
        if choice in ACCOUNTS:
            break
        print("Invalid choice. Please select 1-4.")
    
    selected_account = ACCOUNTS[choice]
    print(f"\nConfiguring Git for: {selected_account['name']}")
    
    if configure_git_account(selected_account):
        print("✓ Git configuration updated successfully!")
        print(f"  Name: {selected_account['name']}")
        print(f"  Email: {selected_account['email']}")
        
        # Show current configuration
        success, name, _ = run_command("git config user.name")
        success, email, _ = run_command("git config user.email")
        print(f"\nCurrent Git configuration:")
        print(f"  Name: {name}")
        print(f"  Email: {email}")
    else:
        print("✗ Failed to configure Git")
        sys.exit(1)

if __name__ == "__main__":
    main()

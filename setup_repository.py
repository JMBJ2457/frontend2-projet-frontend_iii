#!/usr/bin/env python3
"""
Repository Setup Script
Sets up the new repository remote and creates a branch
"""

import subprocess
import sys
import os

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

def main():
    print("=== Repository Setup ===")
    
    # Repository URL
    repo_url = "https://github.com/JMBJ2457/frontend2-projet-frontend_iii.git"
    
    # Get branch name
    branch_name = input("Enter your branch name (e.g., eduardo-aispuro): ").strip()
    if not branch_name:
        print("Branch name cannot be empty")
        sys.exit(1)
    
    print(f"\nSetting up repository...")
    print(f"Repository: {repo_url}")
    print(f"Branch: {branch_name}")
    
    # Check if we're in a git repository
    success, _, _ = run_command("git rev-parse --git-dir", check=False)
    if not success:
        print("Initializing Git repository...")
        success, _, error = run_command("git init")
        if not success:
            print(f"Failed to initialize git: {error}")
            sys.exit(1)
    
    # Remove existing origin if it exists
    print("\nRemoving existing remote 'origin'...")
    run_command("git remote remove origin", check=False)
    
    # Add new remote
    print("Adding new remote...")
    success, _, error = run_command(f"git remote add origin {repo_url}")
    if not success:
        print(f"Failed to add remote: {error}")
        sys.exit(1)
    
    # Fetch from remote
    print("Fetching from remote...")
    success, _, error = run_command("git fetch origin")
    if not success:
        print(f"Failed to fetch: {error}")
        sys.exit(1)
    
    # Create and checkout new branch
    print(f"Creating and switching to branch '{branch_name}'...")
    success, _, error = run_command(f"git checkout -b {branch_name}")
    if not success:
        # Try to create from main/master if it exists
        print("Trying to create branch from main/master...")
        success, _, error = run_command(f"git checkout -b {branch_name} origin/main", check=False)
        if not success:
            success, _, error = run_command(f"git checkout -b {branch_name} origin/master", check=False)
            if not success:
                print(f"Failed to create branch: {error}")
                sys.exit(1)
    
    # Set upstream branch
    print(f"Setting upstream for branch '{branch_name}'...")
    run_command(f"git push --set-upstream origin {branch_name}", check=False)
    
    # Show current status
    print("\n=== Setup Complete ===")
    success, remotes, _ = run_command("git remote -v")
    success, branch, _ = run_command("git branch --show-current")
    success, config, _ = run_command("git config --list --local")
    
    print(f"Remotes:")
    print(remotes)
    print(f"\nCurrent branch: {branch}")
    print(f"\nLocal configuration:")
    print(config)
    
    print(f"\n✓ Repository setup complete!")
    print(f"Your branch '{branch_name}' is ready for commits.")
    print(f"To push changes: git push origin {branch_name}")

if __name__ == "__main__":
    main()

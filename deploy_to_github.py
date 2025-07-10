#!/usr/bin/env python3
"""
GitHub Deployment Helper Script
This script helps prepare and deploy the European Commuting Zones Explorer to GitHub.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        return False

def check_files_exist():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".streamlit/config.toml",
        ".gitignore"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files exist")
    return True

def initialize_git_repo():
    """Initialize git repository if not already done"""
    if os.path.exists(".git"):
        print("✅ Git repository already initialized")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to initialize git repository: {e}")
        return False

def add_files_to_git():
    """Add all files to git"""
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Files added to git")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to add files to git: {e}")
        return False

def commit_changes():
    """Commit changes to git"""
    try:
        subprocess.run([
            "git", "commit", "-m", 
            "Initial commit: European Commuting Zones Explorer with geographic maps"
        ], check=True)
        print("✅ Changes committed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to commit changes: {e}")
        return False

def create_github_repo():
    """Provide instructions for creating GitHub repository"""
    print("\n📋 Next Steps:")
    print("1. Go to https://github.com/new")
    print("2. Create a new repository named 'european-commuting-zones'")
    print("3. Make it public")
    print("4. Don't initialize with README (we already have one)")
    print("5. Copy the repository URL")
    print("\nAfter creating the repository, run:")
    print("git remote add origin https://github.com/YOUR_USERNAME/european-commuting-zones.git")
    print("git branch -M main")
    print("git push -u origin main")

def setup_streamlit_deployment():
    """Provide instructions for Streamlit Cloud deployment"""
    print("\n🚀 Streamlit Cloud Deployment:")
    print("1. Go to https://streamlit.io/cloud")
    print("2. Sign in with GitHub")
    print("3. Click 'New app'")
    print("4. Select your repository: european-commuting-zones")
    print("5. Set main file path: app.py")
    print("6. Click 'Deploy'")
    print("\nYour app will be available at: https://your-app-name.streamlit.app")

def create_packages_file():
    """Create packages.txt for R dependencies"""
    if not os.path.exists("packages.txt"):
        with open("packages.txt", "w") as f:
            f.write("r-base\n")
        print("✅ Created packages.txt for R dependencies")
    else:
        print("✅ packages.txt already exists")

def main():
    """Main deployment process"""
    print("🚀 European Commuting Zones Explorer - GitHub Deployment Helper")
    print("=" * 60)
    
    # Check prerequisites
    if not check_git_installed():
        return
    
    if not check_files_exist():
        return
    
    # Initialize git
    if not initialize_git_repo():
        return
    
    # Add files
    if not add_files_to_git():
        return
    
    # Commit changes
    if not commit_changes():
        return
    
    # Create packages.txt for R dependencies
    create_packages_file()
    
    # Provide next steps
    create_github_repo()
    setup_streamlit_deployment()
    
    print("\n" + "=" * 60)
    print("🎉 Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Create GitHub repository")
    print("2. Push code to GitHub")
    print("3. Deploy to Streamlit Cloud")
    print("4. Share your app URL!")
    
    print("\n📚 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 
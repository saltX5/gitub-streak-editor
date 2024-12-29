import subprocess
import os
from datetime import datetime, timedelta

def check_git_repo(repo_path):
    try:
        subprocess.check_call(["git", "-C", repo_path, "status"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(f"The directory {repo_path} is not a valid Git repository. Please provide a valid Git repository path.")
        exit(1)

def check_remote(repo_path):
    try:
        remote_url = subprocess.check_output(["git", "-C", repo_path, "remote", "get-url", "origin"]).strip().decode('utf-8')
        print(f"Remote repository URL: {remote_url}")
    except subprocess.CalledProcessError:
        print(f"No remote repository found in {repo_path}. Please set up a remote repository first.")
        exit(1)

def create_custom_streak(repo_path):
    start_date = input("Enter the starting date (YYYY-MM-DD): ").strip()
    end_date = input("Enter the ending date (YYYY-MM-DD): ").strip()
    commits_per_day = input("Enter the number of commits per day: ").strip()

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        commits_per_day = int(commits_per_day)

        if commits_per_day <= 0 or start_date > end_date:
            print("Invalid input. Please check the dates and the number of commits.")
            return

        current_date = start_date
        while current_date <= end_date:
            for _ in range(commits_per_day):
                commit_message = f"Update code {current_date.strftime('%Y-%m-%d')}"
                os.system(f'git -C "{repo_path}" commit --allow-empty -m "{commit_message}"')
            os.system(f'git -C "{repo_path}" push origin main --force')
            current_date += timedelta(days=1)

        print("Custom streak created.")

    except ValueError:
        print("Invalid input. Please enter valid dates and a positive integer for commits per day.")

if __name__ == "__main__":
    repo_path = input("Enter the path to your Git repository: ").strip()

    if not os.path.isdir(repo_path):
        print("The provided path is not a valid directory. Please provide a valid path.")
        exit(1)

    check_git_repo(repo_path)
    check_remote(repo_path)
    create_custom_streak(repo_path)

import subprocess
import os

def remove_commits_from_head():
    commit_hash = input("Enter the commit hash (e.g., HEAD~2 for two commits ago): ").strip()

    if not commit_hash:
        return

    try:
        os.system(f"git reset --hard {commit_hash}")
        os.system("git push origin main --force")
        print(f"Successfully removed all commits after {commit_hash}. Repository reset to the specified commit.")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\nChoose an option:")
        print("1. Reset all commits and start fresh (delete all history).")
        print("2. Remove script-generated commits and retain your legitimate streak.")
        print("3. Create a custom streak of commits.")
        print("4. Remove commits from a specific HEAD.")
        print("5. Exit.")
        
        choice = input("Enter your choice (1/2/3/4/5): ").strip()
        
        if choice == "1":
            reset_all_commits()
        elif choice == "2":
            remove_script_commits()
        elif choice == "3":
            create_custom_streak()
        elif choice == "4":
            remove_commits_from_head()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def reset_all_commits():
    os.system("git reset --hard --root")
    os.system("git push origin --force")

def remove_script_commits():
    first_commit_hash = subprocess.check_output(
        ["git", "log", "--reverse", "--pretty=format:'%H'"], stderr=subprocess.STDOUT
    ).decode('utf-8').strip().split("\n")[0].replace("'", "")
    
    if not first_commit_hash:
        return

    os.system(f"git reset --hard {first_commit_hash}")
    os.system("git push origin --force")

def create_custom_streak():
    days = input("Enter the number of days (e.g., 5 for 5 days): ").strip()
    commit_pattern = input("Enter the commit pattern (e.g., 5,3,4,8,4): ").strip()

    try:
        days = int(days)
        pattern = [int(x) for x in commit_pattern.split(",")]

        if len(pattern) != days:
            return

        for i in range(days):
            for _ in range(pattern[i]):
                os.system(f"git commit --allow-empty -m 'Automated commit for day {i + 1}'")
            os.system("git push origin main --force")

        print("Custom streak created.")

    except ValueError:
        pass

if __name__ == "__main__":
    main()

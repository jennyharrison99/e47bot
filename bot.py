import os
import importlib
import sys
from config import USER_PROFILE

SITE_FOLDER = "site_scripts"


def list_sites():
    sites = [f.replace(".py", "") for f in os.listdir(SITE_FOLDER) if f.endswith(".py")]
    return sites


def select_site():
    sites = list_sites()
    print("\n📋 Available Sites:")
    for idx, site in enumerate(sites, 1):
        print(f"{idx}. {site}")

    choice = input("\nEnter site number to run: ")
    try:
        return sites[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid selection. Try again.")
        return select_site()


def run_site(site_name):
    try:
        print(f"\n🚀 Launching: {site_name}.py")
        sys.path.insert(0, SITE_FOLDER)
        module = importlib.import_module(site_name)
        module.run(USER_PROFILE)
    except Exception as e:
        print(f"❌ Failed to run {site_name}: {e}")
        with open("logs/error_log.txt", "a") as log_file:
            log_file.write(str(e) + "\n")


if __name__ == "__main__":
    selected = select_site()
    run_site(selected)

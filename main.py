import argparse
import os
import re
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import inquirer  # Make sure to install this package


def fetch_go_versions():
    url = 'https://golang.org/dl/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        link_elements = soup.find_all('a', href=True)
        gz_links = [link['href'] for link in link_elements if link['href'].endswith('.tar.gz')]
        
        # Use regular expression to filter versions
        version_pattern = re.compile(r'^go(\d+\.\d+(\.\d+)?).linux-amd64.tar.gz$')
        versions = [version_pattern.match(link.split('/')[-1]).group(1) for link in gz_links if version_pattern.match(link.split('/')[-1])]
        
        return sorted(set(versions), reverse=True)  # Return unique and sorted versions
    except Exception as e:
        print(f"Failed to fetch Go versions: {e}")
        sys.exit(1)


def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.returncode}")
        sys.exit(1)

def add_go_paths():
    try:
        home = os.path.expanduser("~")
        bash_profile = os.path.join(home, ".bash_profile")
        bashrc = os.path.join(home, ".bashrc")
        paths_to_update = []

        # Check which files exist and if both exist, add paths to both
        if os.path.exists(bash_profile):
            paths_to_update.append(bash_profile)
        if os.path.exists(bashrc):
            paths_to_update.append(bashrc)

        # Environment variables to add
        go_paths = """
        # Go environment variables
        export PATH=$PATH:/usr/local/go/bin
        export GOPATH=$HOME/go
        export GOBIN=$GOPATH/bin
        """

        # Append Go paths to the files
        for path in paths_to_update:
            with open(path, "a") as file:
                file.write(go_paths)

        # Note: Sourcing in this manner won't affect the parent shell of the script
        print("Go paths added to shell configuration files. Please restart your terminal or source the files manually.")

    except Exception as e:
        print(f"An error occurred: {e}")

def install_go(go_version):
    # Download Go
    print(f"Downloading Go version {go_version}...")
    download_url = f"https://golang.org/dl/go{go_version}.linux-amd64.tar.gz"
    run_command(f"wget {download_url} -O go.tar.gz")

    # Extract Go and setup paths
    print("Extracting Go...")
    run_command("rm -rf /usr/local/go && tar -C /usr/local -xzf go.tar.gz")
    run_command("rm go.tar.gz")  # Clean up the tarball

    # Set up Go environment variables
    # You might want to add these to your profile or shell rc file for persistence
    os.environ["PATH"] += os.pathsep + "/usr/local/go/bin"
    os.environ["GOPATH"] = os.environ["HOME"] + "/go"
    os.environ["GOBIN"] = os.environ["GOPATH"] + "/bin"

    print("Attempting to add golang to bash automatically")
    print("Go installation is complete.")
    print("Remember to add Go paths to your profile or shell rc file for persistence.")

def main():
    parser = argparse.ArgumentParser(description="Go (Golang) Installer Script")
    parser.add_argument("-v", "--version", type=str, help="Specify the Go version to install", default="1.18")
    parser.add_argument("--versions", action='store_true', help="Display and select available Go versions")
    args = parser.parse_args()

    if args.versions:
        versions = fetch_go_versions()
        questions = [
            inquirer.List('version',
                          message="Select Go version to install",
                          choices=versions,
                          ),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            install_go(answers['version'])
        else:
            print("No version selected.")
            sys.exit(1)
    else:
        install_go(args.version)

if __name__ == "__main__":
    main()

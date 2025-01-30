# RepoRecon

## Overview

🔍 RepoRecon is a Python-based command-line tool designed to simplify searching, downloading, and scanning GitHub repositories. The tool seamlessly integrates with Gitleaks to identify and validate secrets such as API keys, tokens, and credentials, enhancing your workflow and security posture.

## Features

- 🧑‍💻 Search GitHub Repositories: Use the GitHub API to search for repositories by keyword.

- 📥 Download Repositories: Select and download repositories directly from the search results.

- 🔒 Secrets Scanning: Automatically scan downloaded repositories with Gitleaks to detect sensitive information.

- ✅ Validation: Validate credentials such as AWS keys, Azure credentials, GitHub tokens, Slack tokens, and more.

- 🎛️ Interactive or Automated: Choose between manual selection or automated operations for downloading and scanning repositories.

- 📜 Custom Gitleaks Rules: Use a custom rules.toml file for advanced secrets detection.


## Requirements

- 🐍 Python 3.8 or higher

- 🔍 Gitleaks installed on your system (Installation Guide)

## Installation
### The tool can be installed using the Python Package Index (PyPI):
- pip install RepoRecon
### Install it via the source code:
* Step 1: Clone the Repository:
  - git clone <repository_url>
  - cd GitHubSearchTool

- Step 2: Install Dependencies
  - Install the required Python packages:
  -pip install -r requirements.txt

- Step 3: Install the Tool
  - Use the following command to install the tool:
  - python setup.py install

- The installation process will ensure that Gitleaks is installed if it is not already.



## Usage

### Basic Usage

#### RepoRecon <keyword> --token <github_token>

- keyword : The keyword to search for on GitHub.

- <github_token>: Your GitHub personal access token.

### Options

- 📥 --download: Enable manual selection and download of repositories.

- 📂 --download-all: Automatically download all repositories matching the keyword.

- 🔍 --gitleaks: Scan downloaded repositories using Gitleaks.

- 📁 --destination <path>: Specify the directory to save downloaded repositories (default: ./downloaded_repos).

- 📜 --rule-file <path>: Specify the custom Gitleaks rule file to use for scanning.

## Example Workflows

### 1. Search and Display Results

- RepoRecon "tesla" --token <your_github_token>

- This will display a list of repositories related to the keyword "tesla."

### 2. Download All Repositories

- RepoRecon "tesla" --token <your_github_token> --download-all

 - This will automatically download all matching repositories.
### 3. Scan Repositories with Gitleaks

- RepoRecon "tesla" --token <your_github_token> --download-all --gitleaks

- This will download and scan all matching repositories for secrets using Gitleaks.

## Supported Validations

### The tool validates the following credentials:

* 🔑 AWS Credentials

* 🔑 Azure Credentials

* 🔑 Slack Tokens

* 🔑 Stripe API Keys

* 🔑 GitHub Personal Access Tokens

* 🔑 Heroku API Keys

* 🔑 Dropbox API Keys

* 🔑 Twilio API Keys


### Using Custom Gitleaks Rules

 - To enhance the detection capabilities, you can provide a custom *rules.toml* file for Gitleaks. This file allows you to define additional patterns for secrets detection or adjust existing rules.

#### Example of Running Gitleaks with Custom Rules

##### githubsearchtool "security" --token <your_github_token> --download-all --gitleaks --rule-file /path/to/rules.toml

- Ensure that your rules.toml file is correctly configured to meet your detection needs.

### Dependencies

#### The following Python packages are required and listed in requirements.txt:

- boto3

- requests

- rich

- pyfiglet

- stripe

### Notes

#### Ensure Gitleaks is installed and accessible in your system's PATH.

#### Use a GitHub personal access token with appropriate permissions to access the GitHub API.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the creators of Gitleaks and all open-source contributors who make tools like this possible.



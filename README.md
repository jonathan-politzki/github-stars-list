# GitHub Repository Stargazers and Forks Fetcher

This script fetches the list of users who have starred and forked a specific GitHub repository using the GitHub API.

## Features

- Fetches all users who starred a given repository.
- Fetches all users who forked a given repository.
- Saves the results into separate JSON files (`stargazers.json` and `forks.json`).
- Handles GitHub API pagination.
- Includes basic error handling and rate limit consideration.

## Files

- `github_repo_info.py`: The main Python script.
- `requirements.txt`: Lists the required Python packages.
- `stargazers.json`: Output file containing the list of stargazers (username and profile URL).
- `forks.json`: Output file containing the list of users who forked the repo (username and profile URL).

## Setup

1.  **Clone the repository or download the files.**
2.  **Install dependencies:**
    Make sure you have Python 3 installed. Then, install the required package using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Configure Repository (Optional):**
    By default, the script is set to fetch data for `supermemoryai/supermemory`. You can change the `repo_owner` and `repo_name` variables inside the `github_repo_info.py` script if you want to target a different repository.

    ```python
    # Inside github_repo_info.py
    if __name__ == "__main__":
        # Repository details
        repo_owner = "YOUR_REPO_OWNER"  # Change this
        repo_name = "YOUR_REPO_NAME"    # Change this
        # ... rest of the script
    ```

2.  **Run the script:**
    Execute the script from your terminal:
    ```bash
    python github_repo_info.py
    ```

3.  **Output:**
    The script will print progress to the console and save the results in:
    - `stargazers.json`
    - `forks.json`

## GitHub API Rate Limits

- The GitHub API has rate limits. For unauthenticated requests, the limit is typically 60 requests per hour.
- If the target repository has a very large number of stars or forks, you might hit this limit.
- To increase the limit (to 5,000 requests per hour), you can use a GitHub Personal Access Token (PAT).
    - Generate a PAT in your GitHub account settings (developer settings).
    - Uncomment and update the `headers` dictionary in the `get_paged_data` function within `github_repo_info.py`:
      ```python
      # Inside get_paged_data function
      headers = {
          "Accept": "application/vnd.github.v3+json",
          "Authorization": "token YOUR_PERSONAL_ACCESS_TOKEN" # Add your token here
      }
      ```
    - **Important:** Keep your PAT secure and do not commit it directly into your code if you plan to share it. Consider using environment variables or other secure methods to handle tokens.

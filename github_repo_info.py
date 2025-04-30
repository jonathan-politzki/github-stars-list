import requests
import json
import time

def get_paged_data(url_template, repo_owner, repo_name, data_key):
    """
    Generic function to fetch paginated data from GitHub API.

    Args:
        url_template (str): The URL template for the API endpoint (e.g., "stargazers", "forks").
        repo_owner (str): Owner of the repository.
        repo_name (str): Name of the repository.
        data_key (str): The key in the response item containing user info (e.g., 'login', 'owner').

    Returns:
        list: List of dictionaries containing username and profile URL.
    """
    results = []
    page = 1
    per_page = 100  # Maximum allowed by GitHub API

    while True:
        # GitHub API endpoint
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/{url_template}"

        # Parameters for pagination
        params = {
            "page": page,
            "per_page": per_page
        }

        # Headers for API request (GitHub API v3)
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        # Add your personal access token here if you're hitting rate limits
        # headers["Authorization"] = "token YOUR_PERSONAL_ACCESS_TOKEN"

        # Make the request
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

        # Parse the response
        items = response.json()

        # If no more items, break the loop
        if not items:
            break

        # Process items
        for item in items:
            user_info = item
            # Stargazers response has user info directly
            # Forks response has user info nested under 'owner'
            if data_key == 'owner':
                 user_info = item.get('owner', {})

            if user_info and 'login' in user_info and 'html_url' in user_info:
                 results.append({
                    "username": user_info["login"],
                    "profile_url": user_info["html_url"]
                 })
            else:
                 print(f"Warning: Could not extract user info from item: {item}")


        print(f"Processed page {page} for {url_template}, found {len(items)} items")

        # Move to the next page
        page += 1

        # Respect GitHub API rate limits (60 requests/hour unauthenticated)
        # Be cautious with authenticated requests (5000 requests/hour)
        time.sleep(1) # Simple delay; consider more robust rate limit handling for heavy use

    return results

def get_stargazers(repo_owner, repo_name):
    """Fetch all users who starred a GitHub repository"""
    print(f"Fetching stargazers for {repo_owner}/{repo_name}...")
    # For stargazers, the user info is directly in the item
    return get_paged_data("stargazers", repo_owner, repo_name, 'login')

def get_forks(repo_owner, repo_name):
    """Fetch all users who forked a GitHub repository"""
    print(f"Fetching forks for {repo_owner}/{repo_name}...")
    # For forks, the user info is nested under 'owner'
    return get_paged_data("forks", repo_owner, repo_name, 'owner')


def save_to_file(data, filename="output.json"):
    """Save data to a JSON file"""
    try:
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} items to {filename}")
    except IOError as e:
        print(f"Error saving file {filename}: {e}")


if __name__ == "__main__":
    # Repository details
    repo_owner = "supermemoryai"
    repo_name = "supermemory"

    # --- Get Stargazers ---
    stargazers = get_stargazers(repo_owner, repo_name)
    if stargazers:
        save_to_file(stargazers, filename="stargazers.json")
        print(f"Total stargazers: {len(stargazers)}")
        # Print the first few stargazers as example
        print("Sample stargazers:")
        for i, stargazer in enumerate(stargazers[:5]):
            print(f"{i+1}. {stargazer['username']} - {stargazer['profile_url']}")
    else:
        print("Could not retrieve stargazers.")


    # --- Get Forks ---
    forks = get_forks(repo_owner, repo_name)
    if forks:
        save_to_file(forks, filename="forks.json")
        print(f"Total forks: {len(forks)}")
        # Print the first few forks as example
        print("Sample users who forked:")
        for i, fork_user in enumerate(forks[:5]):
            print(f"{i+1}. {fork_user['username']} - {fork_user['profile_url']}")
    else:
        print("Could not retrieve forks.")

    print("Script finished.") 
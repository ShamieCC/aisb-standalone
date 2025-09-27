
# %%

# Ensure the root directory is in the path for imports
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from aisb_utils import report

# Common imports
import requests
from typing import Callable

print("It works!")

from w1d0_test import test_prerequisites

# Run the prerequisite checks only when file is run directly
if __name__ == "__main__":
    # Comment out the prerequisites for now since we're in standalone repo
    # test_prerequisites()
    print("Prerequisites check skipped - working in standalone repository")


# %%

from dataclasses import dataclass


@dataclass
class UserIntel:
    username: str
    name: str | None
    location: str | None
    email: str | None
    repo_names: list[str]


def analyze_user_behavior(username: str = "karpathy") -> UserIntel:
    """
    Analyze a user's GitHub activity patterns.
    This is the kind of profiling attackers might do for social engineering.

    Returns:
        The user's name, location, email, and 5 most recently updated repos.
    """
    # 1. Make a GET request to get user information
    user_url = f"https://api.github.com/users/{username}"
    user_response = requests.get(user_url)
    
    # Check if user exists
    if user_response.status_code != 200:
        return UserIntel(
            username=username,
            name=None,
            location=None,
            email=None,
            repo_names=[]
        )
    
    user_data = user_response.json()
    
    # 2. Extract user information
    name = user_data.get("name")
    location = user_data.get("location")
    email = user_data.get("email")
    
    # 3. Make a GET request to get user's repositories
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"
    repos_response = requests.get(repos_url)
    
    repo_names = []
    if repos_response.status_code == 200:
        repos_data = repos_response.json()
        repo_names = [repo["name"] for repo in repos_data[:5]]
    
    # 4. Return UserIntel object
    return UserIntel(
        username=username,
        name=name,
        location=location,
        email=email,
        repo_names=repo_names
    )

# %%

from w1d0_test import test_analyze_user_behavior

test_analyze_user_behavior(analyze_user_behavior)
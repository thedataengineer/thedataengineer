import os
import github
from datetime import datetime
from jinja2 import Template

# GitHub Authentication
g = github.Github(os.environ["GITHUB_TOKEN"])
user = g.get_user()

# Get repositories data
repositories = []
for repo in user.get_repos():
    if not repo.fork and not repo.archived and repo.owner.login == user.login:
        repositories.append({
            "name": repo.name,
            "url": repo.html_url,
            "description": repo.description or "No description",
            "language": repo.language or "Not specified",
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "updated_at": repo.updated_at.strftime("%Y-%m-%d")
        })

# Sort by last updated
repositories.sort(key=lambda r: r["updated_at"], reverse=True)

# Get recent forks
forks = []
for repo in user.get_repos():
    if repo.fork and repo.owner.login == user.login:
        parent = repo.parent
        forks.append({
            "name": repo.name,
            "url": repo.html_url,
            "parent_name": parent.name,
            "parent_url": parent.html_url,
            "parent_owner": parent.owner.login,
            "description": repo.description or "No description",
            "language": repo.language or "Not specified",
            "created_at": repo.created_at.strftime("%Y-%m-%d")
        })

# Sort by creation date
forks.sort(key=lambda f: f["created_at"], reverse=True)

# Limit to the most recent ones
active_repos = repositories[:8]  # Adjust number as needed
recent_forks = forks[:4]  # Adjust number as needed

# Read template
with open("README.md.template", "r") as file:
    template_content = file.read()

# Process template
template = Template(template_content)
readme_content = template.render(
    active_repositories=active_repos,
    recent_forks=recent_forks,
    last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

# Write updated README
with open("README.md", "w") as file:
    file.write(readme_content)

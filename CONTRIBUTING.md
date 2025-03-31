# Contributing to Greenova

This document outlines the recommended git workflow for integrating feature
branches into the main branch.

## Overview

The process follows these steps:

1. Update main branch to the latest version
2. Squash and merge the feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

- Appropriate permissions to push to the main branch
- Completed and tested feature in a separate branch
- Understanding of git commands and conflict resolution

## Important Notes

- Always ensure your feature is fully tested before merging
- The squash merge creates a single commit from all changes in the feature
  branch
- This workflow keeps the commit history clean and linear
- Make sure the feature branch is no longer needed before deletion

## After Completion

Once completed, the feature's changes will be integrated into the main branch
as a single commit, and the feature branch will be removed from both local and
remote repositories.

We value respect, inclusivity, and a collaborative environment where everyone
feels welcome to contribute.

Thank you for contributing to our project! This document outlines our git
workflow for integrating feature branches into the main branch.

## Project Status

Current release: v0.0.4 Next pre-release branch: pre-release/v0.0.4

1. **Prerequisites**:

For contributors working with a forked repository, follow these steps to avoid
divergent branches and ensure smooth integration:

2. **Clone the repository** (if you're a direct contributor) or fork it first
   (recommended for external contributors):

   ```bash
   git clone https://github.com/enssol/greenova.git
   cd greenova
   ```

3. **Set up a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

The application will be available at
[http://localhost:8000](http://localhost:8000).

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the
   [GitHub Issues](https://github.com/enssol/greenova/issues)
2. If not, [create a new issue](https://github.com/enssol/greenova/issues/new)
   with:
   - A clear, descriptive title
   - Detailed steps to reproduce (for bugs)
   - Expected and actual behavior
   - Screenshots if applicable
   - Your environment details (OS, browser, etc.)

### Feature Requests

For feature requests:

1. Describe the feature in detail
2. Explain the use case and benefits
3. Indicate if you're willing to contribute the feature yourself

### Documentation Updates

Documentation improvements are always welcome:

- Fix typos or clarify existing content
- Add missing information
- Update documentation to reflect current functionality

### Code Contributions

For code contributions, please follow our
[Development Workflow](#development-workflow).

## Development Workflow

We use a fork-based workflow for external contributors and a feature branch
workflow for direct contributors.

### Fork-Based Contribution

For external contributors:

1. **Fork the repository** on GitHub
2. **Clone your fork**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/greenova.git
   cd greenova
   ```

3. **Add upstream remote**:

   ```bash
   git remote add upstream https://github.com/enssol/greenova.git
   ```

4. **Keep your fork updated**:

1. Always sync your fork with upstream before starting new work:

   ```bash
   git fetch upstream
   git checkout main
   git reset --hard upstream/main
   git push origin main
   ```

2. Create a feature branch for your work:

   ```bash
   git checkout -b feature-name
   ```

3. Make your changes and commit frequently with meaningful messages:

   ```bash
   git commit -m "feat: descriptive message about the change"
   ```

4. Keep your branch up to date with upstream:

   ```bash
   git fetch upstream
   git rebase upstream/main
   # Resolve any conflicts
   ```

8. **Push your changes** to your fork:

   ```bash
   git push origin feature-name
   ```

9. **Create a pull request**:
   - Ensure your branch is up to date with upstream
   - Submit the pull request through GitHub

### Git Workflow for Direct Contributors

For direct contributors:

1. **Update your main branch**:

1. Before submitting a PR, ensure your branch is up to date:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Resolve any conflicts and test your changes thoroughly

3. Push your updated branch to your fork:

   ```bash
   git push origin feature-branch --force-with-lease
   ```

4. Create a pull request through GitHub interface

5. Respond to code review feedback by making additional commits to your branch

### After Your PR is Merged

1. Delete your local feature branch:

   ```bash
   git branch -D feature-branch
   ```

2. Delete the remote branch on your fork:

   ```bash
   git push origin --delete feature-branch
   ```

3. Sync your fork with the updated upstream:
   ```bash
   git fetch upstream
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch**:

   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes** and commit with
   [proper commit messages](#commit-message-guidelines)

4. **Squash and merge your feature branch**:

   ```bash
   git checkout main
   git merge --squash feature-name
   git commit -m "feat: squashed commit message"
   ```

5. **Push changes to main**:

   ```bash
   git push origin main
   ```

6. **Delete the feature branch**:

- Sync your fork with upstream at least weekly
- Don't let branches diverge more than 10 commits
- Keep feature branches short-lived (< 2 weeks)
- Use `git pull --rebase` instead of regular `git pull`
- Consider a monthly "deep cleaning":
  ```bash
  git reflog expire --expire=30.days --all
  git gc --aggressive --prune=now
  ```

## Git Workflow Overview (Direct Contributors)

Our integration process follows these key steps:

1. Update your main branch to the latest version
2. Squash and merge your feature branch into main
3. Push the changes to the remote repository
4. Clean up by removing the feature branch

## Prerequisites

Before you begin:

- Ensure you have appropriate permissions to push to the main branch
- Complete and thoroughly test your feature in a separate branch
- Be familiar with git commands and conflict resolution

## Step-by-Step Process

# 1. Switch to main and get latest changes

`git checkout main` `git pull origin main`

# 2. Squash and merge the feature branch (resolve any conflicts if they arise)

`git merge --squash feature-branch`
`git commit -m "feat: squashed commit message"`

# 3. Push changes to main

`git push origin main`

# 4. Delete feature branch locally

`git branch -D feature-branch`

# 5. Delete feature branch remotely

`git push origin --delete feature-branch`

# Note: Ensure the feature branch is no longer needed before deleting it remotely.

## Conflict Resolution Guidelines

If you encounter merge conflicts:

1. Understand both sides of the conflict before resolving
2. When in doubt, consult with team members familiar with the code
3. For complex conflicts, consider using a visual merge tool:
   ```bash
   git branch -D feature-name
   git push origin --delete feature-name
   ```

### Branch Strategy

If you encounter any issues with the git workflow, please reach out to the team
lead or open a discussion on GitHub.

# Creating a GitHub Personal Access Token

## Step 1: Generate a Personal Access Token
1. Go to GitHub.com and log in
2. Click your profile icon in the top right
3. Select "Settings"
4. Scroll down and click "Developer settings" (at the bottom of the left sidebar)
5. Click "Personal access tokens" → "Tokens (classic)"
6. Click "Generate new token" → "Generate new token (classic)"
7. Give your token a name (e.g., "DesiReel Project")
8. Select the "repo" scope (this gives access to your repositories)
9. Click "Generate token"
10. **IMPORTANT**: Copy your token immediately! You won't be able to see it again.

## Step 2: Use the Token
1. Run the `github_push_token.bat` script
2. Enter your GitHub username
3. Enter your repository name
4. Paste your personal access token when prompted

## Alternative: Configure Git Credential Manager
```bash
git config --global credential.helper store
```
Then push once with your token as the password. Git will remember it for future pushes.
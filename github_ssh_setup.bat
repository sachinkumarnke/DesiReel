@echo off
echo Setting up SSH for GitHub...

REM Check if SSH key exists
if not exist "%USERPROFILE%\.ssh\id_ed25519.pub" (
    echo Generating new SSH key...
    ssh-keygen -t ed25519 -C "your_email@example.com"
) else (
    echo SSH key already exists.
)

REM Display the public key
echo.
echo Your public SSH key (copy this to GitHub):
echo.
type "%USERPROFILE%\.ssh\id_ed25519.pub"
echo.

REM Instructions
echo.
echo ===== NEXT STEPS =====
echo 1. Copy the SSH key above
echo 2. Go to GitHub.com → Settings → SSH and GPG keys → New SSH key
echo 3. Paste your key and save
echo 4. Run the following commands to push your code:
echo.
echo    git remote remove origin
echo    git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
echo    git push -u origin main
echo.
echo Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub username and repository name.
echo ========================
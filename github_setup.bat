@echo off
echo Setting up GitHub repository...

REM Initialize Git repository
git init

REM Add all files to staging
git add .

REM Create initial commit
git commit -m "Initial commit"

REM Instructions for connecting to GitHub
echo.
echo ===== NEXT STEPS =====
echo 1. Create a new repository on GitHub (https://github.com/new)
echo 2. Run the following commands to push your code:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual GitHub username and repository name.
echo ========================
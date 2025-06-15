@echo off
echo Pushing to GitHub with Personal Access Token...

REM Get GitHub username
set /p username=Enter your GitHub username: 

REM Get repository name
set /p repo=Enter your repository name: 

REM Get personal access token
set /p token=Enter your GitHub personal access token: 

REM Update remote origin with token authentication
git remote remove origin
git remote add origin https://%username%:%token%@github.com/%username%/%repo%.git

REM Set main branch and push
git branch -M main
git push -u origin main

echo.
echo If successful, your code is now on GitHub!
echo If you see errors, verify your token has proper permissions (repo scope).
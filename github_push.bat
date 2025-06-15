@echo off
echo Pushing to GitHub...

REM Get GitHub username
set /p username=Enter your GitHub username: 

REM Get repository name
set /p repo=Enter your repository name: 

REM Add remote origin
git remote add origin https://github.com/%username%/%repo%.git

REM Set main branch and push
git branch -M main
git push -u origin main

echo.
echo If you see any errors, make sure:
echo 1. You have a GitHub account
echo 2. The repository exists on GitHub
echo 3. You have the correct permissions
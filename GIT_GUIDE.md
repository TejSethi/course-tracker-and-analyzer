# GIT Guide

For the project, when working on different features,
working directly on the `main` branch is not a good practice.

The `main` branch should always have working approved code.

Therefore, feature branches must be used. 
A feature branch is a copy from the main branch.
After starting as a copy, new commits are added for the feature (ahead of main)
When a feature branch is ready, it is pushed to github and
then you'll need to create a Pull Request in order to get approvals 
for merging it into the main branch.

## Step by step flow when working on a new feature

### Step 1: Checkout main
Make sure you're on the main branch, and it is up to date with 
the remote branch
```
git checkout main
git pull
```
- `checkout` means to switch to a specific branch
- `pull` means to retrieve the changes from the remote
down to the local branch

### Step 2: Create a new branch (when starting a new feature)
Always make a branch before working
```
git checkout -b <new-feature>
```
This creates AND switches to the new branch.
- `checkout` means to SWITCH to the given branch name
- `-b` this option means to CREATE a new branch

### Step 3: After working on the feature, check your status (before committing)
See what changed:
```
git status
```
Red = new/changed (not staged)
Green = staged for commit

### Step 4: Add Files to Staging (prepare files for commit)
Add all new/changed files (the ones in red):
```
git add .
```
- `.` means all

Or Add one or multiple specific files:
```
git add filename.py filename2.py ...
```

### Step 5: Commit (save your work locally)
Create a checkpoint and write a short message about what you changed
```
git commit -m "Add base course model and sqlite setup"
```
Note: Good commit message should start with a verb in a present tense


### Step 6: Push your branch (upload to GitHub)
```
git push -u origin <branch name>
```

Now your branch will exist on GitHub.
-  `origin` means GitHub
- `-u` means "upstream": to set the new origin branch to be 
   the upstream branch of the local branch

After you do it once, can use short command
```
git push
```
### Step 7: Create a Pull Request (PR)
On GitHub:
   - Go to the repo
   - Switch to your branch (most of the time, not necessary as GitHub 
     detects the new branch you pushed and will show you a nice 
     alert with "Create new PR button")
   - Click "Open Pull Request"
   - Set _base_ branch to "main" (this is the default already)
   - Add title, description, reviewers, other metadata
   - Submit the PR (can be edited after-wards)
   - All reviewers will receive a notification (email) with link to Pull Request
   - Reviewers then can comment/approve/reject the pull request
   - **Bonus**: GitHub can run "jobs" (CI/CD pipelines) on the code of your 
            pull request's branch, for example running unit tests, 
            and will alert you on failure

Your teammates (including you) can now review it

### Step 8: main branch updates while your PR is open
When main branch is updated with new work (not from your PR),
then you'll need to sync your local main with the remote main
```
git checkout main
git pull
```
- `checkout main`: switch to the local main branch
- `pull`: fetch the latest changes from the remote 

Switch back to your feature branch
```
git checkout <feature branch>
```

Merge main into your branch
```
git merge main
```
- `merge`: bring in the new commits from the `main` branch 
           into your current checked branch

Merge conflicts are common, so you may need to resolve
any conflicts and then commit.

Push new local changes to the remote feature 
branch (automatically reflecting in the open PR)
```
git push
```

### Step 9: Merge the Pull Request (after review and approval)
On GitHub, merge the PR.
This will merge the feature branch of the PR into
the base branch (usually origin `main`).

### Step 10: Pull Again (sync your machine)
After merging, repeat step 1 (sync your local main) and follow the steps
to work on the next new feature.

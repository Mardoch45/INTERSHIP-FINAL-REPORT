# Publishing to GitHub

The local repository uses branch `main` and is linked to [Mardoch45/INTERSHIP-FINAL-REPORT](https://github.com/Mardoch45/INTERSHIP-FINAL-REPORT). No files were uploaded by the preparation environment, whose GitHub DNS resolution and recorded authentication were unavailable.

Run from the local repository root:

```bash
git status
git ls-files
python3 -m unittest discover -s tests -v
gh auth login --hostname github.com --git-protocol https --web
gh auth status
git remote -v
git fetch origin
git branch -r
git log --oneline --graph --all
git push -u origin main
```

If the remote branch already has commits and the push is rejected, inspect and integrate that history before retrying. Do not force-replace remote content that has not been reviewed.

The complete confidential report remains in the workspace's `rapport_final/` folder, outside this public repository. Local commits use a GitHub noreply author address.

After editing public documents:

```bash
git add README.md docs evidence COMMANDS.md
git commit -m "Update the English report and evidence"
git push
```

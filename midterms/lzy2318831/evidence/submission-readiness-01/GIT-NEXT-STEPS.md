# Safe next Git steps (Windows PowerShell)

No commands below have been used to stage, commit or push. Work from the repository
root. The read-only block can run now; it includes untracked files, which a normal
git diff does not show.

```powershell
Set-Location C:\Users\lzy21\Documents\game-dev-f26
git branch --show-current
git status --short --untracked-files=all
git diff --check
git diff --cached --check
git add --dry-run -- midterms/lzy2318831/ .github/workflows/midterm-lzy2318831.yml
```

After explicitly approving staging, run the following block. It does not commit
or push. Never use git add ., -A or -f here; ignored caches/private files must stay
excluded. Stop if Git reports a failure or an unexpected path.

```powershell
git add -- midterms/lzy2318831/ .github/workflows/midterm-lzy2318831.yml
if ($LASTEXITCODE -ne 0) { throw 'Staging failed; inspect before continuing.' }
$unexpectedMidtermPaths = @(git diff --cached --name-only | Where-Object {
    $_ -notlike 'midterms/lzy2318831/*' -and
    $_ -ne '.github/workflows/midterm-lzy2318831.yml'
})
if ($unexpectedMidtermPaths.Count -gt 0) {
    $unexpectedMidtermPaths
    throw 'Unexpected staged paths; stop without committing.'
}
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Inspect whitespace findings; do not blindly rewrite frozen files.' }
git diff --cached --stat
git diff --cached --name-status
git diff --cached -- midterms/lzy2318831/ .github/workflows/midterm-lzy2318831.yml
```

Review that complete staged diff and pending evidence before authorizing a commit.
No commit, push, PR-creation or CourseWorks command is part of this preparation.
Keep the recording marked pending until the actual video exists. After a separately
approved push, check both CI matrix jobs for the exact submitted commit and retain
the actual green-run URL; never claim local checks are remote CI.

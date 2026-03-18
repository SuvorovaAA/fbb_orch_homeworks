# intro1
git commit
git commit
# intro2
git checkout -b bugFix
# intro3
git checkout -b bugFix
git commit
git checkout main
git commit
git merge bugFix
# intro4
git checkout -b bugFix
git commit
git checkout main
git commit
git checkout bugFix
git rebase main
# rampup1
git checkout C4
# rampup2
git checkout bugFix^
# rampup3
git branch -f main C6
git branch -f bugFix HEAD~2
git checkout HEAD^
# rampup4
git reset HEAD^
git checkout pushed
git revert HEAD
# move1
git cherry-pick C3 C4 C7
# move2
git rebase -i overHere
# mixed1
git checkout main
git cherry-pick C4
# mixed2
git rebase -i main
git commit --amend
git rebase -i main
git branch -f main HEAD
# mixed3
git checkout main
git cherry-pick C2
git commit --amend
git cherry-pick C3
# mixed4
git tag v0 C1
git tag v1 C2
git checkout v1
# mixed5
git rebase -i main
git rebase -i main
git commit
# advanced1
git rebase main bugFix
git rebase bugFix side
git rebase side another
git branch -f main HEAD
# advanced2
git branch bugWork HEAD~1^2~1
# advanced3
git checkout one
git cherry-pick C4 C3 C2
git checkout two
git cherry-pick C5 C4' C3' C2'
git branch -f three C2
# remote1
git clone
# remote2
git commit
git checkout o/main
git commit
# remote3
git fetch
# remote4
git pull
# remote5
git clone
git fakeTeamwork main 2
git commit
git pull
# remote6
git commit
git commit
git push
# remote7
git clone
git fakeTeamwork main 1
git commit
git pull --rebase
git push
# remote8
git checkout -b feature
git push
git branch -f main HEAD^
# remoteAdvanced1
git fetch
git rebase o/main side1
git rebase side1 side2
git rebase side2 side3
git branch -f main HEAD
git checkout main
git push
# remoteAdvanced2
git fetch
git branch -f main o/main
git checkout main
git merge side1
git merge side2
git merge side3
git push
# remoteAdvanced3
git checkout -b side o/main
git commit
git pull --rebase
git push
# remoteAdvanced4
git push origin main
git push origin foo
# remoteAdvanced5
git push origin foo:main
git push origin main^:foo
# remoteAdvanced6
git fetch origin C6:main
git fetch origin C3:foo
git checkout foo
git merge main
# remoteAdvanced7
git push origin :foo
git fetch origin :bar

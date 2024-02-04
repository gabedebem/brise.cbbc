#!/bin/sh
cd ~/brise.cbbc
git rm --cache db/brise.db
git gc
git add db/brise.db
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
# git commit --amend -m "Regular auto-commit ammend DB $(timestamp)"
# git push --force-with-lease
git commit -am "Regular auto-commit $(timestamp)"
git push

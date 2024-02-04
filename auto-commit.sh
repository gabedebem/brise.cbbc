#!/bin/sh
cd ~/brise.cbbc
git rm --cache db/brise.db
git rm --cache logs/logs_sistema.log
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch db/brise.db' --prune-empty --tag-name-filter cat -- --all
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch logs/logs_sistema.log' --prune-empty --tag-name-filter cat -- --all

git add db/brise.db
git add logs/logs_sistema.log
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
# git commit --amend -m "Regular auto-commit ammend DB $(timestamp)"
# git push --force-with-lease
git commit -am "Regular auto-commit $(timestamp)"
git push

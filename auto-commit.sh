#!/bin/sh
cd ~/brise.cbbc
git rm --cache db/brise.db
git gc
#git add db/brise.db
git add -A
# git add db/brise.db
git add -A
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
git commit -am "Regular auto-commit $(timestamp)"
git push

# git rm --cache logs/logs_sistema.log
# git add logs/logs_sistema.log

# git commit --amend -m "Regular auto-commit ammend DB $(timestamp)"
# git push --force-with-lease

# python3 git-filter-repo.py --invert-paths --path 'db/brise.db'
# python3 git-filter-repo.py --invert-paths --path 'logs/logs_sistema.log'

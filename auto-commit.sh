#!/bin/sh
cd ~/brise.cbbc
git add --all
timestamp() {
  date +"at %H:%M:%S on %d/%m/%Y"
}
# git commit -am "Regular auto-commit $(timestamp)"
git commit --amend -m "Regular auto-commit $(timestamp)"
git push --force-with-lease
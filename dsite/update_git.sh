git status
git add *
git commit -a -m "update:$1"
git push
git status
echo "First arg: $0"
echo "Second arg: $1"

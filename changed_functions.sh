git show $1^..HEAD  |
grep -E '^(@@)'     |
grep -v 'import '   |
sed 's/@@.*@@//'    |
sed 's/def //'      |
sed 's/://'         |
sed 's/ //'         |
sed '/^$/d'         |
sort                |
uniq